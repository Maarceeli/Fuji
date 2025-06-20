from datetime import date
from sdk.src.models.exam import Exam
from sdk.src.models.grade import Grade
from sdk.src.models.note import Note
from sdk.src.models.student import Student
from sdk.src.models.lesson import Lesson
from sdk.src.models.homework import Homework


class CoreInterface:
    def select_student(self, context) -> None:
        pass

    def login(self) -> None:
        pass

    def get_students(self) -> list[Student]:
        pass

    def get_lucky_number(self) -> int:
        pass

    def get_grades(period_number: int) -> list[Grade]:
        pass

    def get_exams(from_: date, to: date) -> list[Exam]:
        pass

    def get_notes() -> list[Note]:
        pass
    
    def get_timetable(from_: date, to: date) -> list[Lesson]:
        pass

    def get_homework(from_: date, to: date) -> list[Homework]:
        pass