from datetime import datetime

from pydantic import BaseModel


class Grade(BaseModel):
    value: str
    is_point: bool
    point_numerator: int | None
    point_denominator: int | None
    weight: float
    name: str
    created_at: datetime
    subject: str
    creator: str

    @staticmethod
    def from_hebe_dict(data: dict[str, any]):
        return Grade(
            value=data["Content"],
            is_point=data["Numerator"] != None,
            point_numerator=data["Numerator"],
            point_denominator=data["Denominator"],
            weight=data["Column"]["Weight"],
            name=data["Column"]["Name"] or data["Column"]["Code"],
            created_at=datetime.fromtimestamp(data["DateCreated"]["Timestamp"] / 1000),
            subject=data["Column"]["Subject"]["Name"],
            creator=data["Creator"]["DisplayName"],
        )
