from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    name: str | None
    content: str
    points: str | None
    creator: str
    created_at: datetime

    @staticmethod
    def from_hebe_dict(data: dict):
        return Note(
            name=data["Category"]["Name"] if data["Category"] else None,
            content=data["Content"],
            points=str(data["Points"]) if data["Points"] else None,
            creator=data["Creator"]["DisplayName"],
            created_at=datetime.fromtimestamp(data["DateValid"]["Timestamp"] / 1000),
        )
