from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel


class ExamType(Enum):
    TEST = 0
    SHORT_TEST = 1
    CLASSWORK = 2
    OTHER = 3

    @staticmethod
    def from_hebe_type_name(type_name: str):
        match type_name:
            case "Sprawdzian":
                return ExamType.TEST
            case "Kartkówka":
                return ExamType.SHORT_TEST
            case "Praca klasowa":
                return ExamType.CLASSWORK
            case _:
                return ExamType.OTHER


class Exam(BaseModel):
    deadline: date
    subject: str
    type: ExamType
    description: str
    creator: str
    created_at: datetime

    @staticmethod
    def from_hebe_dict(data: dict):
        return Exam(
            deadline=datetime.fromtimestamp(data["Deadline"]["Timestamp"] / 1000),
            subject=data["Subject"]["Name"],
            type=ExamType.from_hebe_type_name(data["Type"]),
            description=data["Content"],
            creator=data["Creator"]["DisplayName"],
            created_at=datetime.fromtimestamp(data["DateCreated"]["Timestamp"] / 1000),
        )
