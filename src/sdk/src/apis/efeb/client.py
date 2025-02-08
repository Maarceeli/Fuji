import dataclasses
import requests

from sdk.src.apis.common.models import FsLsResponse, FsLsQuery
from sdk.src.apis.common.utils import parse_fs_ls_response_form
from sdk.src.apis.efeb.constants import (
    ENDPOINT_LOGIN_FS_LS,
    ENDPOINT_MESSAGES_APP,
    ENDPOINT_STUDENT_APP,
    BASE_LOGIN,
    BASE_MESSAGES,
    BASE_MESSAGES_CE,
    BASE_STUDENT,
    BASE_STUDENT_CE,
)
from sdk.src.apis.efeb.utils import parse_app_html


class EfebClient:
    def __init__(self, cookies: dict, symbol: str, is_ce: bool):
        self._session = requests.Session()
        self._session.cookies.update(cookies)
        self._symbol = symbol
        self._is_ce = is_ce

    def get_cookies(self):
        return self._session.cookies.get_dict()

    def login_fs_ls(
        self, query: FsLsQuery, prometheus_response: FsLsResponse | None = None
    ):
        response = self._session.request(
            method="POST" if prometheus_response else "GET",
            url=f"{BASE_LOGIN}/{self._symbol}/{ENDPOINT_LOGIN_FS_LS}",
            data=(
                dataclasses.asdict(prometheus_response) if prometheus_response else None
            ),
            params=dataclasses.asdict(query),
        )
        return parse_fs_ls_response_form(response.text)

    def student_app(self, login_response: FsLsResponse | None = None):
        response = self._session.request(
            method="POST" if login_response else "GET",
            url=f"{BASE_STUDENT_CE if self._is_ce else BASE_STUDENT}/{self._symbol}/{ENDPOINT_STUDENT_APP}",
            data=dataclasses.asdict(login_response) if login_response else None,
        )
        return parse_app_html(response.text)

    def messages_app(self, login_response: FsLsResponse | None = None):
        response = self._session.request(
            method="POST" if login_response else "GET",
            url=f"{BASE_MESSAGES_CE if self._is_ce else BASE_MESSAGES}/{self._symbol}/{ENDPOINT_MESSAGES_APP}",
            data=dataclasses.asdict(login_response) if login_response else None,
        )
        return parse_app_html(response.text)
