from datetime import datetime, date, time
from pydantic import BaseModel
from enum import Enum

class ChangeType(Enum):
    SUBSTITUTION = 0
    ABSENCE = 1
    MERGE = 2
    MOVE = 3
    SEPARATION = 4

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
    substitutiontype: ChangeType | None
    replacedteacher: str | None
    replacedroom: str | None

    @staticmethod
    def from_hebe_dict(data: dict):
        if data["Substitution"]:
            stype = None

            if data["Substitution"]["TeacherPrimary"]:
                stype = ChangeType.SUBSTITUTION

            elif data["Substitution"]["TimeSlot"]:
                stype = ChangeType.MOVE

            elif data["Substitution"]["TeacherAbsenceReasonId"] or data["Substitution"]["TeacherPrimary"] == None:
                stype = ChangeType.ABSENCE


            return Lesson(
                position = data["TimeSlot"]["Position"],
                date = datetime.fromtimestamp(data["Date"]["Timestamp"] / 1000).date(),
                room = data["Substitution"]["Room"]["Code"] if data["Substitution"]["Room"] else data["Room"]["Code"] if data["Room"] else None,
                start = datetime.strptime(data["TimeSlot"]["Start"], "%H:%M").time(),
                end = datetime.strptime(data["TimeSlot"]["End"], "%H:%M").time(),
                subject = data["Subject"]["Name"] if data["Subject"] else data["Event"],
                teacher = data["Substitution"]["TeacherPrimary"]["DisplayName"] if data["Substitution"]["TeacherPrimary"] else data["TeacherPrimary"]["DisplayName"] if data["TeacherPrimary"] else None,
                group = data["Distribution"]["Shortcut"] if data["Distribution"] else None,
                visible = data["Visible"],
                substitutiontype = stype,
                replacedteacher = data["TeacherPrimary"]["DisplayName"] if data["TeacherPrimary"] else None,
                replacedroom = data["Room"]["Code"] if data["Room"] else None,
            )

        else:
            return Lesson(
                position = data["TimeSlot"]["Position"],
                date = datetime.fromtimestamp(data["Date"]["Timestamp"] / 1000).date(),
                room = data["Room"]["Code"] if data["Room"] else None,
                start = datetime.strptime(data["TimeSlot"]["Start"], "%H:%M").time(),
                end = datetime.strptime(data["TimeSlot"]["End"], "%H:%M").time(),
                subject = data["Subject"]["Name"] if data["Subject"] else data["Event"],
                teacher = data["TeacherPrimary"]["DisplayName"] if data["TeacherPrimary"] else None,
                group = data["Distribution"]["Shortcut"] if data["Distribution"] else None,
                visible = data["Visible"],
                substitutiontype = None,
                replacedteacher = None,
                replacedroom = None,
            )
