import flet as ft
from datetime import datetime
from sdk.src.models.exam import ExamType
from i18n import _

class ExamBottomSheet(ft.BottomSheet):
    def __init__(
        self,
        subject: str,
        description: str,
        exam_type: str,
        deadline: str,
        creator: str,
        created_at: datetime,
    ) -> None:
        # Pick an icon based on exam_type
        icon = ft.Icons.SCHOOL
        match exam_type:
            case ExamType.SHORT_TEST:
                icon = ft.Icons.TIMER
            case ExamType.CLASSWORK:
                icon = ft.Icons.FACT_CHECK
            case ExamType.TEST:
                icon = ft.Icons.ASSIGNMENT
            case ExamType.OTHER:
                icon = ft.Icons.SCHOOL
        
        examtype = "Other"
        match exam_type:
            case ExamType.SHORT_TEST:
                examtype = _("Short Test")
            case ExamType.CLASSWORK:
                examtype = _("Classwork")
            case ExamType.TEST:
                examtype = _("Test")
            case ExamType.OTHER:
                examtype = _("Other")
        
        # format created_at
        created_str = created_at.strftime("%Y-%m-%d %H:%M")

        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    [
                        # — Header —
                        ft.Row(
                            [
                                ft.Text(
                                    subject,
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Icon(name=icon, size=40),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            description,
                            size=16,
                            color=ft.Colors.WHITE70,
                        ),

                        # — Type —
                        ft.Card(
                            margin=ft.margin.symmetric(vertical=4),
                            color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            content=ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                content=ft.Row(
                                    [
                                        ft.Icon(name=icon, size=20),
                                        ft.Column(
                                            [
                                                ft.Text(_("Type"), size=12, color=ft.Colors.WHITE70),
                                                ft.Text(examtype, size=18),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ),

                        # — Created At —
                        ft.Card(
                            margin=ft.margin.symmetric(vertical=4),
                            color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            content=ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.Icons.CREATE, size=20),
                                        ft.Column(
                                            [
                                                ft.Text(_("Created At"), size=12, color=ft.Colors.WHITE70),
                                                ft.Text(created_str, size=18),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ),

                        # — Deadline —
                        ft.Card(
                            margin=ft.margin.symmetric(vertical=4),
                            color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            content=ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.Icons.CALENDAR_TODAY, size=20),
                                        ft.Column(
                                            [
                                                ft.Text(_("Deadline"), size=12, color=ft.Colors.WHITE70),
                                                ft.Text(deadline, size=18),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ),

                        # — Teacher / Creator —
                        ft.Card(
                            margin=ft.margin.symmetric(vertical=4),
                            color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            content=ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                content=ft.Row(
                                    [
                                        ft.Icon(name=ft.Icons.PERSON, size=20),
                                        ft.Column(
                                            [
                                                ft.Text(_("Teacher"), size=12, color=ft.Colors.WHITE70),
                                                ft.Text(creator, size=18),
                                            ],
                                            spacing=2,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                            ),
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.all(20),
            ),
            enable_drag=True,
            open=False,
        )

class ExamEntry(ft.Card):
    def __init__(self, deadline, description, subject, creator, exam_type, created_at, page):
        # Store the required data in the ExamEntry itself
        self.subject = subject
        self.description = description
        self.exam_type = exam_type
        self.deadline = deadline
        self.creator = creator
        self.created_at = created_at
        self.page = page  # Store the page object

        examtype = "Other"
        match exam_type:
            case ExamType.SHORT_TEST:
                examtype = _("Short Test")
            case ExamType.CLASSWORK:
                examtype = _("Classwork")
            case ExamType.TEST:
                examtype = _("Test")
            case ExamType.OTHER:
                examtype = _("Other")
        
        super().__init__(
            content=ft.Container(
                content=ft.Column([
                    # Top Row: Description and Type
                    ft.Row([
                        ft.Text(description, font_family="Roboto", weight='bold', size=18, width=800, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(examtype, font_family="Roboto", size=16, color=ft.Colors.BLUE_300),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    # Creator
                    ft.Row([
                        ft.Icon(name=ft.Icons.PERSON, size=16),
                        ft.Text(creator, font_family="Roboto", size=16),
                    ], spacing=5),

                ], spacing=8),
                padding=15,
                width=max,
                on_click=self.show_bottom_sheet,
            ),
            elevation=2,
            margin=ft.margin.symmetric(horizontal=10, vertical=5),
        )

    def show_bottom_sheet(self, e):
        sheet = ExamBottomSheet(
            subject=self.subject,
            description=self.description,
            exam_type=self.exam_type,
            deadline=self.deadline,
            creator=self.creator,
            created_at=self.created_at,
        )
        
        self.page.overlay.append(sheet)
        self.page.update()
        sheet.open = True
        self.page.update()

class HomeworkBottomSheet(ft.BottomSheet):
    def __init__(
        self,
        subject: str,
        description: str,
        deadline: str,
        creator: str,
        created_at: datetime,
    ) -> None:
        
        # format created_at
        created_str = created_at.strftime("%Y-%m-%d %H:%M")

        super().__init__(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Column([
                            # — Header —
                            ft.Row(
                                [
                                    ft.Text(
                                        subject,
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Icon(name=ft.Icons.BOOK, size=40),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                description,
                                size=16,
                                color=ft.Colors.WHITE70,
                            ),
                        ]),
                        
                        ft.Column([
                            # — Created At —
                            ft.Card(
                                margin=ft.margin.symmetric(vertical=4),
                                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                content=ft.Container(
                                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                    content=ft.Row(
                                        [
                                            ft.Icon(name=ft.Icons.CREATE, size=20),
                                            ft.Column(
                                                [
                                                    ft.Text(_("Created At"), size=12, color=ft.Colors.WHITE70),
                                                    ft.Text(created_str, size=18),
                                                ],
                                                spacing=2,
                                            ),
                                        ],
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                            ),

                            # — Deadline —
                            ft.Card(
                                margin=ft.margin.symmetric(vertical=4),
                                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                content=ft.Container(
                                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                    content=ft.Row(
                                        [
                                            ft.Icon(name=ft.Icons.CALENDAR_TODAY, size=20),
                                            ft.Column(
                                                [
                                                    ft.Text(_("Deadline"), size=12, color=ft.Colors.WHITE70),
                                                    ft.Text(deadline, size=18),
                                                ],
                                                spacing=2,
                                            ),
                                        ],
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                            ),

                            # — Teacher / Creator —
                            ft.Card(
                                margin=ft.margin.symmetric(vertical=4),
                                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                content=ft.Container(
                                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                                    content=ft.Row(
                                        [
                                            ft.Icon(name=ft.Icons.PERSON, size=20),
                                            ft.Column(
                                                [
                                                    ft.Text(_("Teacher"), size=12, color=ft.Colors.WHITE70),
                                                    ft.Text(creator, size=18),
                                                ],
                                                spacing=2,
                                            ),
                                        ],
                                        spacing=10,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                            ),
                        ]),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.all(20),
            ),
            enable_drag=True,
            open=False,
        )

class HomeworkEntry(ft.Card):
    def __init__(self, deadline, description, subject, creator, created_at, page):
        # Store the required data in the ExamEntry itself
        self.subject = subject
        self.description = description
        self.deadline = deadline
        self.creator = creator
        self.created_at = created_at
        self.page = page  # Store the page object
        
        super().__init__(
            content=ft.Container(
                content=ft.Column([
                    # Top Row: Description and Type
                    ft.Row([
                        ft.Text(description, font_family="Roboto", weight='bold', size=18, width=800, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(_("Homework"), font_family="Roboto", size=16, color=ft.Colors.BLUE_300),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                    # Creator
                    ft.Row([
                        ft.Icon(name=ft.Icons.PERSON, size=16),
                        ft.Text(creator, font_family="Roboto", size=16),
                    ], spacing=5),

                ], spacing=8),
                padding=15,
                width=max,
                on_click=self.show_bottom_sheet,
            ),
            elevation=2,
            margin=ft.margin.symmetric(horizontal=10, vertical=5),
        )

    def show_bottom_sheet(self, e):
        sheet = HomeworkBottomSheet(
            subject=self.subject,
            description=self.description,
            deadline=self.deadline,
            creator=self.creator,
            created_at=self.created_at,
        )
        
        self.page.overlay.append(sheet)
        self.page.update()
        sheet.open = True
        self.page.update()
