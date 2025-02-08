from datetime import date
from pydantic import BaseModel

class HebePeriod(BaseModel):
    id: int
    number: int
    current: bool
    from_: date
    to: date

    @staticmethod
    def from_dict(data: dict):
        return HebePeriod(
            id=data["Id"],
            number=data["Number"],
            current=data["Current"],
            from_=date.fromtimestamp(data["Start"]["Timestamp"] / 1000),
            to=date.fromtimestamp(data["End"]["Timestamp"] / 1000),
        )


class HebeStudent(BaseModel):
    id: int
    full_name: str
    unit_id: int
    constituent_id: int
    capabilities: list[str]
    register_id: int
    register_student_number: int | None
    class_name: str
    is_parent: bool
    messagebox_key: str
    messagebox_name: str
    periods: list[HebePeriod]
    rest_url: str
    symbol: str

    @staticmethod
    def from_dict(data: dict):
        return HebeStudent(
            id=data["Pupil"]["Id"],
            full_name=data["Pupil"]["FirstName"] + " " + data["Pupil"]["Surname"],
            unit_id=data["Unit"]["Id"],
            constituent_id=data["ConstituentUnit"]["Id"],
            capabilities=data["Capabilities"],
            register_id=data["Journal"]["Id"],
            register_student_number=data["Journal"]["PupilNumber"],
            class_name=data["ClassDisplay"],
            is_parent=bool(data["CaretakerId"]),
            messagebox_key=data["MessageBox"]["GlobalKey"],
            messagebox_name=data["MessageBox"]["Name"],
            periods=list(map(HebePeriod.from_dict, data["Periods"])),
            rest_url=data["Unit"]["RestURL"],
            symbol=data["TopLevelPartition"],
        )
