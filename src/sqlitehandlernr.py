from sqlmodel import *
from datetime import datetime, timedelta
from sqlalchemy import func
from typing import Optional

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

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

def create_grades_database(grades_list):
    with Session(engine) as session:
        session.execute(delete(Grades))
        for grade in grades_list:
            # Format the created_at to the desired format
            formatted_time = grade.created_at.strftime('%d/%m/%Y %H:%M:%S')
            
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

def fetch_all_grades():
    with Session(engine) as session:
        grades = session.query(Grades).all()
    
    return grades
