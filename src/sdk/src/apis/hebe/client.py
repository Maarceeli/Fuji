from datetime import date, datetime
import json
import uuid
import requests

from sdk.src.apis.hebe.certificate import Certificate
from sdk.src.apis.hebe.constants import (
    API_VERSION,
    APP_HEBE_NAME,
    APP_HEBECE_NAME,
    APP_VERSION,
    APP_VERSION_CODE,
    DEVICE_NAME,
    DEVICE_OS,
    ENDPOINT_EXAM_BYPUPIL,
    ENDPOINT_GRADE_BYPUPIL,
    ENDPOINT_HEARTBEAT,
    ENDPOINT_NOTE_BYPUPIL,
    ENDPOINT_REGISTER_HEBE,
    ENDPOINT_REGISTER_JWT,
    ENDPOINT_REGISTER_TOKEN,
    ENDPOINT_SCHOOL_LUCKY,
    ENDPOINT_SCHEDULE_WITHCHANGES_BYPUPIL,
    USER_AGENT,
)
from sdk.src.apis.hebe.exceptions import (
    ExpiredTokenException,
    HebeClientException,
    InvalidPINException,
    InvalidRequestEnvelopeStructure,
    InvalidRequestHeadersStructure,
    NoPermissionsException,
    NoUnitSymbolException,
    NotFoundEntityException,
    UnauthorizedCertificateException,
    UsedTokenException,
)
from sdk.src.apis.hebe.student import HebeStudent
from sdk.src.apis.hebe.signer import get_signature_values
from sdk.src.models.exam import Exam
from sdk.src.models.grade import Grade
from sdk.src.models.note import Note
from sdk.src.models.lesson import Lesson


class HebeClient:
    def __init__(
        self, certificate: Certificate, rest_url: str | None = None, is_ce: bool = True
    ):
        self._session = requests.Session()
        self._certificate = certificate
        self._rest_url = rest_url
        self._is_ce = is_ce

    def set_rest_url(self, new_value: str):
        self._rest_url = new_value

    def _send_request(self, method: str, endpoint: str, envelope: any = None, **kwargs):
        if not self._rest_url:
            raise Exception("No rest_url!")

        date = datetime.now()

        url = f"{self._rest_url}/{endpoint}"
        body = json.dumps(self._build_body(date, envelope)) if envelope else None
        headers = self._build_headers(date, url, body)
        response = self._session.request(
            method, url, data=body, headers=headers, **kwargs
        )

        data = response.json()
        self._check_response_status_code(data["Status"]["Code"])

        return data["Envelope"]

    def _build_headers(self, date: datetime, url: str, body: any):
        digest, canonical_url, signature = get_signature_values(
            self._certificate.fingerprint,
            self._certificate.private_key,
            body,
            url,
            date,
        )

        headers = {
            "signature": signature,
            "vcanonicalurl": canonical_url,
            "vos": DEVICE_OS,
            "vdate": date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            "vapi": API_VERSION,
            "vversioncode": APP_VERSION_CODE,
            "user-agent": USER_AGENT,
        }
        if digest:
            headers["digest"] = digest
            headers["content-type"] = "application/json"

        return headers

    def _build_body(self, date: datetime, envelope: any):
        return {
            "AppName": APP_HEBECE_NAME if self._is_ce else APP_HEBE_NAME,
            "AppVersion": APP_VERSION,
            "NotificationToken": "",
            "API": int(API_VERSION),
            "RequestId": str(uuid.uuid4()),
            "Timestamp": int(date.timestamp()),
            "TimestampFormatted": date.strftime("%Y-%m-%d %H:%M:%S"),
            "Envelope": envelope,
        }

    @staticmethod
    def _check_response_status_code(status_code: int):
        if status_code == 0:
            return
        if status_code == 100:
            raise NoPermissionsException()
        if status_code == 101:
            raise InvalidRequestEnvelopeStructure()
        if status_code == 102:
            raise InvalidRequestHeadersStructure()
        if status_code == 104:
            raise NoUnitSymbolException()
        if status_code == 108:
            raise UnauthorizedCertificateException()
        if status_code == 200:
            raise NotFoundEntityException()
        if status_code == 201:
            raise UsedTokenException()
        if status_code == 203:
            raise InvalidPINException()
        if status_code == 204:
            raise ExpiredTokenException()
        raise HebeClientException(status_code)

    def register_jwt(self, tokens: list[str]):
        envelope = {
            "OS": DEVICE_OS,
            "Certificate": self._certificate.certificate,
            "CertificateType": self._certificate.type,
            "DeviceModel": DEVICE_NAME,
            "SelfIdentifier": str(uuid.uuid4()),
            "CertificateThumbprint": self._certificate.fingerprint,
            "Tokens": tokens,
        }
        return self._send_request("POST", ENDPOINT_REGISTER_JWT, envelope)

    def register_token(self, token: str, pin: str):
        # For hebe interface
        envelope = {
            "OS": DEVICE_OS,
            "Certificate": self._certificate.certificate,
            "CertificateType": self._certificate.type,
            "DeviceModel": DEVICE_NAME,
            "SelfIdentifier": str(uuid.uuid4()),
            "CertificateThumbprint": self._certificate.fingerprint,
            "SecurityToken": token,
            "PIN": pin,
        }
        return self._send_request("POST", ENDPOINT_REGISTER_TOKEN, envelope)

    def get_students(self, mode: int = 2):
        envelope = self._send_request(
            "GET", ENDPOINT_REGISTER_HEBE, params={"mode": mode}
        )
        return map(HebeStudent.from_dict, envelope)

    def heartbeat(self):
        self._send_request("GET", ENDPOINT_HEARTBEAT)

    def get_lucky_number(self, student_id: int, constituent_id: int, day: date):
        envelope = self._send_request(
            "GET",
            ENDPOINT_SCHOOL_LUCKY,
            params={
                "pupilId": student_id,
                "constituentId": constituent_id,
                "day": day.strftime("%Y-%m-%d"),
            },
        )
        return envelope["Number"]

    def get_grades(self, student_id: int, unit_id: int, period_id: int):
        envelope = self._send_request(
            "GET",
            ENDPOINT_GRADE_BYPUPIL,
            params={
                "pupilId": student_id,
                "unitId": unit_id,
                "periodId": period_id,
            },
        )
        return list(map(Grade.from_hebe_dict, envelope))

    def get_exams(self, student_id: int, from_: date, to: date):
        envelope = self._send_request(
            "GET",
            ENDPOINT_EXAM_BYPUPIL,
            params={
                "pupilId": student_id,
                "dateFrom": from_,
                "dateTo": to,
            },
        )
        return list(map(Exam.from_hebe_dict, envelope))

    def get_notes(self, student_id: int):
        envelope = self._send_request(
            "GET", ENDPOINT_NOTE_BYPUPIL, params={"pupilId": student_id}
        )
        return list(map(Note.from_hebe_dict, envelope))
    
    def get_timetablle(self, student_id: int, from_: date, to: date):
        envelope = self._send_request(
            "GET", 
            ENDPOINT_SCHEDULE_WITHCHANGES_BYPUPIL, 
            params={
                "pupilId": student_id, 
                "dateFrom": from_, 
                "dateTo": to, 
                "lastId": "-2147483648",
                "pageSize": 500,
                "lastSyncDate": "1970-01-01%2001%3A00%3A00",
            },
                    
        )
        return list(map(Lesson.from_hebe_dict, envelope))
