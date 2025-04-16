from datetime import datetime, date
from pydantic import BaseModel


class LessonDate(BaseModel):
    Timestamp: int
    Date: str
    DateDisplay: str
    Time: str


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
    Date: LessonDate
    Room: Room
    TimeSlot: TimeSlot
    Subject: Subject
    TeacherPrimary: Teacher
    TeacherSecondary: Teacher | None
    TeacherSecondary2: Teacher | None
    Change: str | None
    Clazz: Clazz
    Distribution: str | None
    PupilAlias: str | None
    Visible: bool
    Substitution: str | None
    Parent: str | None

    @staticmethod
    def from_hebe_dict(data: dict):
        return Lesson(
            Id=data["Id"],
            MergeChangeId=data["MergeChangeId"],
            Event=data["Event"],
            Date=LessonDate(**data["Date"]),
            Room=Room(**data["Room"]),
            TimeSlot=TimeSlot(**data["TimeSlot"]),
            Subject=Subject(**data["Subject"]),
            TeacherPrimary=Teacher(**data["TeacherPrimary"]),
            TeacherSecondary=Teacher(**data["TeacherSecondary"]) if data["TeacherSecondary"] else None,
            TeacherSecondary2=Teacher(**data["TeacherSecondary2"]) if data["TeacherSecondary2"] else None,
            Change=data["Change"],
            Clazz=Clazz(**data["Clazz"]),
            Distribution=data["Distribution"],
            PupilAlias=data["PupilAlias"],
            Visible=data["Visible"],
            Substitution=data["Substitution"],
            Parent=data["Parent"]
        )
