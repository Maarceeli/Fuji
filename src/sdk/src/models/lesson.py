from datetime import datetime, date
from pydantic import BaseModel

#class Change(BaseModel):
#    Id: int
#    Type: int
#    IsMerge: bool
#    Separation: bool


#class Substitution(BaseModel):
#    Id: int
#    UnitId: int
#    ScheduleId: int
#    LessonDate: LessonDate

# TODO: Add a model for the substitutions

class Lesson(BaseModel):
    id: int
    position : int
    date: date
    room: str | None
    start: str
    end: str
    subject: str | None
    teacher: str | None
    group: str | None
    visible: bool

    @staticmethod
    def from_hebe_dict(data: dict):
        return Lesson(
            id=data["Id"],
            position = data["TimeSlot"]["Position"],
            date=datetime.fromtimestamp(data["Date"]["Timestamp"] / 1000),
            room=data["Room"]["Code"],
            start=data["TimeSlot"]["Start"],
            end=data["TimeSlot"]["End"],
            subject=data["Subject"]["Name"],
            teacher=data["TeacherPrimary"]["DisplayName"],
            group=data["Distribution"]["Shortcut"] if data["Distribution"] else None,
            visible=data["Visible"],
        )
