from datetime import date, datetime
from pydantic import BaseModel

class Homework(BaseModel):
    deadline: date
    subject: str
    description: str
    creator: str
    created_at: datetime

    @staticmethod
    def from_hebe_dict(data: dict):
        return Homework(
            deadline=datetime.fromtimestamp(data["Deadline"]["Timestamp"] / 1000),
            subject=data["Subject"]["Name"],
            description=data["Content"],
            creator=data["Creator"]["DisplayName"],
            created_at=datetime.fromtimestamp(data["DateCreated"]["Timestamp"] / 1000),
        )
