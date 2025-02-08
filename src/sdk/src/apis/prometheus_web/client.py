import json
from bs4 import BeautifulSoup
import requests

from sdk.src.apis.common.models import FsLsQuery
from sdk.src.apis.common.utils import parse_fs_ls_response_form
from sdk.src.apis.prometheus_web.constants import (
    ENDPOINT_ACCOUNT_QUERY_USER_INFO,
    ENDPOINT_API_AP,
    ENDPOINT_FS_LS,
    ENDPOINT_LOGIN,
    HEADERS,
    PROMETHEUS_WEB_BASE,
)
from sdk.src.apis.prometheus_web.exceptions import (
    NoLoggedInException,
    InvalidCredentialsException,
)


class PrometheusWebClient:
    def __init__(self, cookies: dict[str, str] | None = None):
        self._session = requests.Session()
        if cookies:
            self._session.cookies.update(cookies)

    def is_logged(self):
        if not self._session.cookies.get_dict():
            return False
        home_response = self._session.get(PROMETHEUS_WEB_BASE)
        soup = BeautifulSoup(home_response.text, "html.parser")
        return bool(soup.select_one("div.user-avatar"))

    def get_login_data(self):
        login_page = self._session.get(
            f"{PROMETHEUS_WEB_BASE}/logowanie",
            headers=HEADERS,
        ).text

        return self._parse_login_page(login_page)

    def _parse_login_page(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        request_verification_token = soup.select_one(
            'input[name="__RequestVerificationToken"]'
        )["value"]

        captcha_text = soup.select_one('label[for="captchaUser"]').text
        captcha_images = [img["src"] for img in soup.select(".v-captcha-image")]

        return request_verification_token, captcha_text, captcha_images

    def query_user_info(self, username: str, request_verification_token: str):
        response = self._session.post(
            f"{PROMETHEUS_WEB_BASE}/{ENDPOINT_ACCOUNT_QUERY_USER_INFO}",
            {
                "alias": username,
                "__RequestVerificationToken": request_verification_token,
            },
        )
        data = response.json()["data"]
        return data["ExtraMessage"], data["ShowCaptcha"]

    def login(
        self,
        username: str,
        password: str,
        reqest_verification_token: str,
        captcha: str | None,
    ):
        login_result = self._session.post(
            f"{PROMETHEUS_WEB_BASE}/{ENDPOINT_LOGIN}",
            data={
                "Alias": username,
                "Password": password,
                "captchaUser": captcha,
                "__RequestVerificationToken": reqest_verification_token,
            },
            headers=HEADERS,
        )

        if "Zła nazwa użytkownika lub hasło." in login_result.text:
            raise InvalidCredentialsException()

    def get_mobile_data(self):
        response = self._session.get(
            f"{PROMETHEUS_WEB_BASE}/{ENDPOINT_API_AP}", headers=HEADERS
        )

        if "Logowanie" in response.text:
            raise NoLoggedInException()

        soup = BeautifulSoup(response.text, "html.parser")
        return json.loads(soup.select_one("input#ap")["value"])

    def fs_ls(self, query: FsLsQuery):
        response = self._session.get(
            f"{PROMETHEUS_WEB_BASE}/{ENDPOINT_FS_LS}",
            params=dict(query),
        )

        if "Logowanie" in response.text:
            raise NoLoggedInException()

        return parse_fs_ls_response_form(response.text)

    def get_cookies(self):
        return self._session.cookies.get_dict()
