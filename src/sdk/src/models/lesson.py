from datetime import datetime, date, time
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
    position: int
    date: date
    room: str | None
    start: time
    end: time
    subject: str | None
    teacher: str | None
    group: str | None
    visible: bool

    @staticmethod
    def from_hebe_dict(data: dict):
        return Lesson(
            position = data["TimeSlot"]["Position"],
            date = datetime.fromtimestamp(data["Date"]["Timestamp"] / 1000).date(),
            room = data["Room"]["Code"] if data.get("Room") else None,
            start = datetime.strptime(data["TimeSlot"]["Start"], "%H:%M").time(),
            end = datetime.strptime(data["TimeSlot"]["End"], "%H:%M").time(),
            subject = data["Subject"]["Name"] if data["Subject"] else data["Event"],
            teacher = data["TeacherPrimary"]["DisplayName"],
            group = data["Distribution"]["Shortcut"] if data["Distribution"] else None,
            visible = data["Visible"],
        )
