from dataclasses import dataclass


@dataclass
class FsLsQuery:
    wa: str
    wtrealm: str
    wctx: str


@dataclass
class FsLsResponse:
    wa: str
    wresult: str
    wctx: str
