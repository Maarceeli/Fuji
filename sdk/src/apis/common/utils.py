from bs4 import BeautifulSoup

from sdk.src.apis.common.models import FsLsResponse


def parse_fs_ls_response_form(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return FsLsResponse(
        wa=soup.select_one('input[name="wa"]')["value"],
        wresult=soup.select_one('input[name="wresult"]')["value"],
        wctx=soup.select_one('input[name="wctx"]')["value"],
    )
