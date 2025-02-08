from pydantic import BaseModel

from sdk.src.apis.hebe import HebeCertificate
from sdk.src.apis.hebe.student import HebeStudent
from sdk.src.interfaces.prometheus.utils import get_context_periods_from_hebe_periods


class PrometheusStudentContext(BaseModel):
    student_id: int
    unit_id: int
    constituent_id: int
    periods: dict[int, int]
    register_id: int
    hebe_url: str
    symbol: str
    messagebox_key: str
    messagebox_name: str

    @staticmethod
    def create(hebe_student: HebeStudent):
        return PrometheusStudentContext(
            student_id=hebe_student.id,
            unit_id=hebe_student.unit_id,
            constituent_id=hebe_student.constituent_id,
            periods=get_context_periods_from_hebe_periods(hebe_student.periods),
            register_id=hebe_student.register_id,
            hebe_url=hebe_student.rest_url,
            symbol=hebe_student.symbol,
            messagebox_key=hebe_student.messagebox_key,
            messagebox_name=hebe_student.messagebox_name,
        )


class PrometheusWebCredentials(BaseModel):
    username: str
    password: str


class PrometheusAuthContext(BaseModel):
    prometheus_web_credentials: PrometheusWebCredentials
    symbols: list[str] | None = None
    hebe_certificate: HebeCertificate | None = None
    prometheus_web_cookies: dict[str, str] | None = None
    efeb_web_cookies: dict[str, dict[str, str] | None] | None = None
