from datetime import datetime, date
from pydantic import BaseModel

class LessonDate(BaseModel):
    Timestamp: int
    Date: str
    DateDisplay: str
    Time: str

class Change(BaseModel):
    Id: int
    Type: int
    IsMerge: bool
    Separation: bool


class Substitution(BaseModel):
    Id: int
    UnitId: int
    ScheduleId: int
    LessonDate: LessonDate

class Distribution(BaseModel):
    Id: int
    Key: str
    Shortcut: str
    Name: str
    PartType: str


class Room(BaseModel):
    Id: int
    Code: str


class TimeSlot(BaseModel):
    Id: int
    Start: str
    End: str
    Display: str
    Position: int


class Subject(BaseModel):
    Id: int
    Key: str
    Name: str
    Kod: str
    Position: int


class Teacher(BaseModel):
    Id: int
    Surname: str
    Name: str
    DisplayName: str


class Clazz(BaseModel):
    Id: int
    Key: str
    DisplayName: str
    Symbol: str


class Lesson(BaseModel):
    Id: int
    MergeChangeId: int | None
    Event: str | None
    Date: date
    Room: Room
    TimeSlot: TimeSlot
    Subject: Subject
    TeacherPrimary: Teacher
    TeacherSecondary: Teacher | None
    TeacherSecondary2: Teacher | None
    Change: Change | None
    Clazz: Clazz
    Distribution: Distribution | None
    PupilAlias: str | None
    Visible: bool
    Substitution: Substitution | None

    @staticmethod
    def from_hebe_dict(data: dict):
        return Lesson(
            Id=data["Id"],
            MergeChangeId=data["MergeChangeId"],
            Event=data["Event"],
            Date=date.fromtimestamp(data["Date"]["Timestamp"] / 1000),
            Room=Room(**data["Room"]),
            TimeSlot=TimeSlot(**data["TimeSlot"]),
            Subject=Subject(**data["Subject"]),
            TeacherPrimary=Teacher(**data["TeacherPrimary"]),
            TeacherSecondary=Teacher(**data["TeacherSecondary"]) if data["TeacherSecondary"] else None,
            TeacherSecondary2=Teacher(**data["TeacherSecondary2"]) if data["TeacherSecondary2"] else None,
            Change=Change(**data["Change"]) if data["Change"] else None,
            Clazz=Clazz(**data["Clazz"]),
            Distribution=Distribution(**data["Distribution"]) if data["Distribution"] else None,
            PupilAlias=data["PupilAlias"],
            Visible=data["Visible"],
            Substitution=Substitution(**data["Substitution"]) if data["Substitution"] else None,
        )
