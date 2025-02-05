from datetime import datetime
import requests
import json
from bs4 import BeautifulSoup
from impl.hebece.src.signer import *
from impl.hebece.src.utils import *
from impl.hebece.src.const import *

session = requests.Session()
certificate, fingerprint, private_key = generate_key_pair()

def getDebugInfo(data):
    data = json.loads(data)
    status = data.get("Status", {})
    code = status.get("Code")
    message = status.get("Message")
    return code, message

def makeRequest(url):
    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body=None, full_url=url, timestamp=datetime.now())

    headers = makeHeader(signature, canonical_url)

    response = requests.get(url, headers=headers)
    content = response.text

    dinfo = getDebugInfo(content)
    return content, dinfo

def APILogin(login, password):
    
    url = "https://eduvulcan.pl/"
    response1 = session.get(url)

    url = "https://eduvulcan.pl/logowanie"
    response2 = session.get(url)

    soup = BeautifulSoup(response2.text, 'html.parser')
    token_input = soup.find('input', {'name': '__RequestVerificationToken'})
    token = {"__RequestVerificationToken": token_input['value']}

    cookies = {**response1.cookies.get_dict(), **response2.cookies.get_dict()}
    cookies_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    cookies_str += f"; __RequestVerificationToken={token_input['value']}"

    # Prometheus
    url = "https://eduvulcan.pl/logowanie?ReturnUrl=%2fapi%2fap"
    headers = makeLoginHeader(cookies_str)

    data = {
        "Alias": login,
        "Password": password,
        "captchaUser": "",
        "__RequestVerificationToken": token_input['value'],
    }

    response = session.post(url, headers=headers, data=data)
    content = response.text
    cookie_jar = response.cookies.get_dict()

    try:
        soup = BeautifulSoup(content, "html.parser")
        input_element = soup.find("input", {"id": "ap"})
        value = input_element["value"]
        parsed_json = json.loads(value)

        tokens = parsed_json.get("Tokens", [])
        token = " ".join(tokens)

        return token
    except TypeError:
        pass

def JWTLogin(token, debug=False): 
    tenant = get_tenant_from_jwt(token)
    
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}{JWT}"
    
    RequestId = getRandomIdentifier() 
    SelfIdentifier = getRandomIdentifier() 
    
    Certificate = certificate
    CertificateThumbprint = fingerprint
    Tokens = token

    digest, canonical_url, signature = get_signature_values(fingerprint, private_key, body=None, full_url=url, timestamp=datetime.now())
    
    headers = makeHeader(signature, canonical_url)

    timestamp = datetime.now()
    date = getDate()
    
    body = {
        "AppName": "DzienniczekPlus 3.0",
        "AppVersion": "24.11.07 (G)",
        "NotificationToken": None,
        "API": 1,
        "RequestId": str(RequestId), 
        "Timestamp": getTimestamp(),
        "TimestampFormatted": str(date),
        "Envelope": {
            "OS": DEVICE_OS,
            "Certificate": Certificate,
            "CertificateType": "X509",
            "DeviceModel": DEVICE,
            "SelfIdentifier": str(SelfIdentifier),
            "CertificateThumbprint": CertificateThumbprint,
            "Tokens": [Tokens]
        }
    }

    body_json = json.dumps(body, indent=4)

    response = session.post(url, headers=headers, data=body_json)
    content = response.text

    if debug:
        dinfo = getDebugInfo(content)
        return content, dinfo
    
    return content

def HEBELogin(tenant, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}{HEBE}?mode=2&lastSyncDate=1970-01-01%2001%3A00%3A00"
    content, dinfo = makeRequest(url)
    return content, dinfo

def getLuckyNumber(tenant, schoolid, pupilid, constituentid, debug=False):
    timestamp = datetime.now()
    date = timestamp.strftime("%Y-%m-%d")
    
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}{LUCKY}?pupilId={pupilid}&constituentId={constituentid}&day={date}"
    content, dinfo = makeRequest(url)
    return content, dinfo

def getGrades(tenant, schoolid, pupilid, unitid, periodid, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/grade/byPupil?unitId={unitid}&pupilId={pupilid}&periodId={periodid}&lastSyncDate=1970-01-01%2001%3A00%3A00&lastId=-2147483648&pageSize=500"

    content, dinfo = makeRequest(url)
    return content, dinfo

def getTimetable(tenant, schoolid, pupilid, start_date, end_date, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/schedule/withchanges/byPupil?pupilId={pupilid}&dateFrom={start_date}&dateTo={end_date}&lastId=-2147483648&pageSize=500&lastSyncDate=1970-01-01%2001%3A00%3A00"
    
    content, dinfo = makeRequest(url)
    return content, dinfo

def getExams(tenant, schoolid, pupilid, start_date, end_date, debug=False):
    url = f"https://lekcjaplus.vulcan.net.pl/{tenant}/{schoolid}/api/mobile/exam/byPupil?pupilId={pupilid}&dateFrom={start_date}&dateTo={end_date}&lastId=-2147483648&pageSize=500&lastSyncDate=1970-01-01%2001%3A00%3A00"
    
    content, dinfo = makeRequest(url)
    return content, dinfo
