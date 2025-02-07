from datetime import date, datetime
from sdk.src.apis.common.models import FsLsQuery
from sdk.src.apis.efeb.client import EfebClient
from sdk.src.apis.hebe import HebeClient, HebeCertificate
from sdk.src.apis.prometheus_web.client import PrometheusWebClient
from sdk.src.apis.prometheus_web.exceptions import (
    InvalidCredentialsException,
    NoLoggedInException as PrometheusWebNoLoggedInException,
)
from sdk.src.interfaces.core.interface import CoreInterface
from sdk.src.interfaces.prometheus.context import (
    PrometheusStudentContext,
    PrometheusAuthContext,
)
from sdk.src.interfaces.prometheus.exceptions import (
    NoLoggedInException,
    NoStudentSelectedException,
)
from sdk.src.interfaces.prometheus.utils import (
    flat_map,
    get_hebe_url,
    parse_jwt_payload,
)
from sdk.src.models.student import Student


class PrometheusInterface(CoreInterface):
    def __init__(
        self,
        auth_context: PrometheusAuthContext,
        student_context: PrometheusStudentContext | None = None,
    ):
        self._auth_context = auth_context
        self._student_context = student_context

        self._prometheus_web_client = PrometheusWebClient(
            self._auth_context.prometheus_web_cookies
        )
        self._hebe_client = (
            HebeClient(
                certificate=self._auth_context.hebe_certificate,
                rest_url=(
                    self._student_context.hebe_url if self._student_context else None
                ),
                is_ce=True,
            )
            if self._auth_context.hebe_certificate
            else None
        )
        self._efeb_clients = {}
        if self._auth_context.symbols:
            for symbol in self._auth_context.symbols:
                if (
                    self._auth_context.efeb_web_cookies
                    and self._auth_context.efeb_web_cookies.get(symbol)
                ):
                    self._efeb_clients[symbol] = EfebClient(
                        cookies=self._auth_context.efeb_web_cookies[symbol],
                        symbol=symbol,
                        is_ce=True,
                    )
        self._efeb_student_vars = {}
        self._efeb_messages_vars = {}

    def select_student(self, context: PrometheusStudentContext):
        self._student_context = context
        self._hebe_client.set_rest_url(context.hebe_url)
        self._hebe_client.heartbeat()

    def get_auth_context(self):
        return self._auth_context

    def login(self, captcha: str | None = None):
        if not self._prometheus_web_client.is_logged():
            result = self._login_prometheus(captcha)
            if result:
                return result

        self._auth_context.prometheus_web_cookies = (
            self._prometheus_web_client.get_cookies()
        )

        # TODO: Expired hebe certificate
        if not self._auth_context.hebe_certificate:
            self._login_hebe()

        self._login_efeb()

    def _login_prometheus(self, captcha: str | None = None):
        print("Logging for prometheus...")
        request_verification_token, captcha_text, captcha_images = (
            self._prometheus_web_client.get_login_data()
        )

        _, show_captcha = self._prometheus_web_client.query_user_info(
            self._auth_context.prometheus_web_credentials.username,
            request_verification_token,
        )
        if show_captcha:
            return {
                "status": "captcha",
                "captcha_text": captcha_text,
                "captcha_images": captcha_images,
            }

        try:
            self._prometheus_web_client.login(
                self._auth_context.prometheus_web_credentials.username,
                self._auth_context.prometheus_web_credentials.password,
                request_verification_token,
                captcha,
            )
        except InvalidCredentialsException:
            _, show_captcha = self._prometheus_web_client.query_user_info(
                self._auth_context.prometheus_web_credentials.username,
                request_verification_token,
            )
            return {
                "status": "invalid_credentials",
                "captcha_text": captcha_text,
                "captcha_images": captcha_images,
                "show_captcha": show_captcha,
            }

    def _login_hebe(self):
        print("Logging for hebe...")
        self._auth_context.hebe_certificate = HebeCertificate.generate()
        self._hebe_client = HebeClient(
            certificate=self._auth_context.hebe_certificate, rest_url=None, is_ce=True
        )

        try:
            mobile_data = self._prometheus_web_client.get_mobile_data()
        except PrometheusWebNoLoggedInException:
            self._auth_context.prometheus_web_cookies = None
            raise NoLoggedInException()

        symbols: dict[str, list[any]] = {}
        for token in mobile_data["Tokens"]:
            payload = parse_jwt_payload(token)
            if not symbols.get(payload["tenant"]):
                symbols[payload["tenant"]] = [token]
            else:
                symbols[payload["tenant"]].append(token)

        for symbol in symbols:
            self._hebe_client.set_rest_url(get_hebe_url(symbol))
            self._hebe_client.register_jwt(symbols[symbol])

        self._auth_context.symbols = symbols.keys()

    def _login_efeb(self):
        if not self._auth_context.efeb_web_cookies:
            self._auth_context.efeb_web_cookies = dict(
                [(symbol, None) for symbol in self._auth_context.symbols]
            )

        for symbol in self._auth_context.efeb_web_cookies:
            if self._auth_context.efeb_web_cookies[symbol]:
                continue

            print(f"Logging for efeb at {symbol}")

            try:
                student_prometheus_response = self._prometheus_web_client.fs_ls(
                    FsLsQuery(
                        wa="wsignin1.0",
                        wtrealm=f"https://dziennik-logowanie.vulcan.net.pl/{symbol}/Fs/Ls?wa=wsignin1.0&wtrealm=https://uczen.eduvulcan.pl/{symbol}/App&wctx=auth=studentEV&nslo=1",
                        wctx="nslo=1",
                    )
                )
            except PrometheusWebNoLoggedInException:
                self._auth_context.prometheus_web_cookies = None
                raise NoLoggedInException()

            self._efeb_clients[symbol] = EfebClient(
                cookies=self._auth_context.prometheus_web_cookies,
                symbol=symbol,
                is_ce=True,
            )
            student_login_response = self._efeb_clients[symbol].login_fs_ls(
                query=FsLsQuery(
                    wa="wsignin1.0",
                    wtrealm=f"https://uczen.eduvulcan.pl/{symbol}/App",
                    wctx="auth=studentEV&nslo=1",
                ),
                prometheus_response=student_prometheus_response,
            )
            self._efeb_student_vars[symbol] = self._efeb_clients[symbol].student_app(
                login_response=student_login_response
            )

            messages_login_response = self._efeb_clients[symbol].login_fs_ls(
                query=FsLsQuery(
                    wa="wsignin1.0",
                    wtrealm=f"https://wiadomosci.eduvulcan.pl/{symbol}/App",
                    wctx="auth=studentEV&nslo=1",
                ),
            )
            self._efeb_messages_vars[symbol] = self._efeb_clients[symbol].messages_app(
                login_response=messages_login_response
            )
            self._auth_context.efeb_web_cookies[symbol] = self._efeb_clients[
                symbol
            ].get_cookies()

    def _check_is_auth_context_full(self):
        if (
            not self._auth_context.hebe_certificate
            or not self._auth_context.prometheus_web_cookies
            or not self._auth_context.symbols
        ):
            raise NoLoggedInException()

    def _check_is_student_selected(self):
        if not self._student_context:
            raise NoStudentSelectedException()

    def get_students(self):
        self._check_is_auth_context_full()
        return flat_map(
            [*map(self._get_students_in_symbol, self._auth_context.symbols)]
        )

    def _get_students_in_symbol(self, symbol: str):
        self._hebe_client.set_rest_url(get_hebe_url(symbol))
        hebe_students = self._hebe_client.get_students()
        return [
            Student.from_hebe_student(
                hebe_student, PrometheusStudentContext.create(hebe_student)
            )
            for hebe_student in hebe_students
        ]

    def get_lucky_number(self):
        self._check_is_auth_context_full()
        self._check_is_student_selected()
        return self._hebe_client.get_lucky_number(
            self._student_context.student_id,
            self._student_context.constituent_id,
            datetime.now(),
        )

    def get_grades(self, period_number: int):
        self._check_is_auth_context_full()
        self._check_is_student_selected()
        return self._hebe_client.get_grades(
            self._student_context.student_id,
            self._student_context.unit_id,
            self._student_context.periods[period_number],
        )

    def get_exams(self, from_: date, to: date):
        self._check_is_auth_context_full()
        self._check_is_student_selected()
        return self._hebe_client.get_exams(self._student_context.student_id, from_, to)
