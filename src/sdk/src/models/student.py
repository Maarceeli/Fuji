from datetime import date
from typing import Generic, TypeVar

from pydantic import BaseModel

from sdk.src.apis.hebe.student import HebePeriod, HebeStudent


class Period(BaseModel):
    id: int
    number: int
    current: bool
    from_: date
    to: date

    @staticmethod
    def from_hebe_period(period: HebePeriod):
        return Period(
            id=period.id,
            number=period.number,
            current=period.current,
            from_=period.from_,
            to=period.to,
        )


T = TypeVar("T")


class Student(BaseModel, Generic[T]):
    full_name: str
    is_parent: bool
    class_name: str
    register_number: int | None
    periods: list[Period]
    context: T

    @staticmethod
    def from_hebe_student(student: HebeStudent, context: T):
        return Student(
            full_name=student.full_name,
            is_parent=student.is_parent,
            class_name=student.class_name,
            register_number=student.register_student_number,
            periods=list(map(Period.from_hebe_period, student.periods)),
            context=context,
        )
