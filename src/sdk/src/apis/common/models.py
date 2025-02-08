from pydantic import BaseModel


class FsLsQuery(BaseModel):
    wa: str
    wtrealm: str
    wctx: str


class FsLsResponse(BaseModel):
    wa: str
    wresult: str
    wctx: str
