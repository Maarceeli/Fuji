from sqlmodel import *
from datetime import date, datetime, timedelta, time
from sqlalchemy import func
from typing import Optional
from sdk.src.models.exam import ExamType

class Grades(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Add an auto-incrementing id
    value: str  # value is no longer a primary key
    is_point: bool
    point_numerator: Optional[float] = None
    point_denominator: Optional[float] = None
    weight: float
    name: str
    created_at: datetime
    subject: str
    creator: str
    semester: int

class Notes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Add an auto-incrementing id
    name: Optional[str] = Field(default=None, nullable=True)
    content: Optional[str] = Field(default=None, nullable=True)
    points: Optional[str] = Field(default=None, nullable=True)
    creator: str
    created_at: datetime
    
class Timetable(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Add an auto-incrementing id
    position : int
    date: date
    room: str | None
    start: time
    end: time
    subject: str | None
    teacher: str | None
    group: str | None
    visible: bool

class Exam(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Add an auto-incrementing id
    deadline: date
    subject: str
    type: ExamType
    description: str
    creator: str
    created_at: datetime

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

def create_grades_database(grades_list, smstr):
    with Session(engine) as session:
        session.execute(delete(Grades))
        for grade in grades_list:
            grade_obj = Grades(
                value=grade.value, 
                is_point=grade.is_point,
                point_numerator=grade.point_numerator, 
                point_denominator=grade.point_denominator, 
                weight=grade.weight, 
                name=grade.name, 
                created_at=grade.created_at,
                subject=grade.subject, 
                creator=grade.creator,
                semester=smstr
            )
            
            session.add(grade_obj)
            session.commit()
            
def create_timetable_database(timetable_list):
    with Session(engine) as session:
        session.execute(delete(Timetable))
        for lesson in timetable_list:
            lesson_obj = Timetable(
                position = lesson.position,
                date=lesson.date,
                room=lesson.room, 
                start=lesson.start, 
                end=lesson.end, 
                subject=lesson.subject, 
                teacher=lesson.teacher, 
                group=lesson.group, 
                visible=lesson.visible
            )
            
            session.add(lesson_obj)
            session.commit()
            
def create_exams_database(exams_list):
    with Session(engine) as session:
        session.execute(delete(Timetable))
        for exam in exams_list:
            exam_obj = Exam(
                deadline=exam.deadline,
                subject=exam.subject,
                type=exam.type,
                description=exam.description,
                creator=exam.creator,
                created_at=exam.created_at,
            )

            session.add(exam_obj)
            session.commit()
         
def add_grades_to_database(grades_list, smstr):
    with Session(engine) as session:
        for grade in grades_list:
            grade_obj = Grades(
                value=grade.value, 
                is_point=grade.is_point,
                point_numerator=grade.point_numerator, 
                point_denominator=grade.point_denominator, 
                weight=grade.weight, 
                name=grade.name, 
                created_at=grade.created_at,
                subject=grade.subject, 
                creator=grade.creator,
                semester=smstr
            )
            
            session.add(grade_obj)
            session.commit()

def fetch_grades_this_week():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=7)

    with Session(engine) as session:
        grades = session.query(Grades).filter(Grades.created_at >= start_of_week, Grades.created_at < end_of_week).all()
    
    return grades

def fetch_all_grades(semester: int):
    with Session(engine) as session:
        grades = session.query(Grades).filter(Grades.semester == semester).all()
    return grades


def create_notes_database(notes_list):
    with Session(engine) as session:
        session.execute(delete(Notes))
        for note in notes_list:  
            note_obj = Notes(
                name=note.name or "Untitled", 
                content=note.content, 
                points=note.points or "None", 
                creator=note.creator, 
                created_at=note.created_at,
            )
            
            session.add(note_obj)
            session.commit()

def fetch_all_notes():
    with Session(engine) as session:
        notes = session.query(Notes).all()
    
    return notes

def fetch_exams_for_week(specific_day: date):
    start_of_week = specific_day - timedelta(days=specific_day.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)

    print(start_of_week, end_of_week)

    with Session(engine) as session:
        exams = session.query(Exam).filter(
            Exam.deadline >= start_of_week,
            Exam.deadline < end_of_week
        ).all()

    return exams
