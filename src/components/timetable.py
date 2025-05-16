import flet as ft

class LessonEntry(ft.Card):
    def __init__(self, start_time, end_time, subject, teacher, room, lesson_number=None, page=None):
        self.page = page
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time
        self.teacher = teacher
        self.room = room
        self.lesson_number = lesson_number or ""  # optional

        super().__init__(
            elevation=1,
            margin=ft.margin.symmetric(horizontal=10, vertical=4),
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=8, horizontal=12),
                content=ft.Row(
                    [
                        # Lesson number on the left
                        ft.Text(str(self.lesson_number), size=24, weight="bold", width=30),

                        # Vertical column of lesson details
                        ft.Column(
                            [
                                # Top row: Start time and subject
                                ft.Row([
                                    ft.Text(self.start_time.strftime("%H:%M"), size=16),
                                    ft.Text(self.subject, size=18, weight="bold"),
                                ], spacing=8),

                                # Bottom row: End time and room + teacher
                                ft.Row([
                                    ft.Text(self.end_time.strftime("%H:%M"), size=16),
                                    ft.Text(f"{self.room} {self.teacher}", size=16, color=ft.Colors.WHITE70),
                                ], spacing=8),
                            ],
                            spacing=4,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        )
