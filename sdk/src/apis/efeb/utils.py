from bs4 import BeautifulSoup
import re


def parse_fs_ls_form(html: str):
    soup = BeautifulSoup(html, "html.parser")
    return {
        "wa": soup.select_one('input[name="wa"]')["value"],
        "wresult": soup.select_one('input[name="wresult"]')["value"],
        "wctx": soup.select_one('input[name="wctx"]')["value"],
    }


def parse_app_html(html: str):
    return re.search("appGuid: '(.*?)'", html).group(1), re.search(
        "antiForgeryToken: '(.*?)'", html
    ).group(1)
