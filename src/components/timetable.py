import flet as ft
from sdk.src.models.lesson import ChangeType

class LessonEntry(ft.Card):
    def __init__(self, start_time, end_time, subject, teacher, room, lesson_number=None, page=None, substitutiontype=None):
        self.page = page
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time
        self.teacher = teacher
        self.room = room
        self.lesson_number = lesson_number or ""
        self.substitutiontype = substitutiontype

        match self.substitutiontype:
            case ChangeType.SUBSTITUTION:
                ccolor = ft.Colors.with_opacity(0.5, ft.Colors.YELLOW_600)
            case ChangeType.ABSENCE:
                ccolor = ft.Colors.with_opacity(0.5, ft.Colors.RED_500)
            case _:
                ccolor = None

        super().__init__(
            elevation=1,
            margin=ft.margin.symmetric(horizontal=10, vertical=4),
            content=ft.Container(
                alignment=ft.alignment.center,  # Center everything vertically
                padding=ft.padding.symmetric(vertical=8, horizontal=12),
                content=ft.Row(
                    controls=[
                        ft.Text(str(self.lesson_number), size=24, weight="bold", width=30),

                        ft.Column(
                            controls=[
                                ft.Row([
                                    ft.Text(self.start_time.strftime("%H:%M"), size=16),
                                    ft.Text(self.subject, size=18, weight="bold"),
                                ], spacing=8),

                                ft.Row([
                                    ft.Text(self.end_time.strftime("%H:%M"), size=16),
                                    ft.Text(f"{self.room} {self.teacher}", size=16, color=ft.Colors.WHITE70),
                                ], spacing=8),
                            ],
                            spacing=4,
                            alignment=ft.MainAxisAlignment.CENTER,  # Center column content
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                )
            ),
            color=ccolor if ccolor else None,
            height=90,
        )
