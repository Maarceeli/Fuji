import flet as ft
from sqlitehandlernr import fetch_all_grades
from i18n import _
from utils import getcurrentsemester, calculate_weighted_average, format_date, parse_grade_value
from components.grades import GradeBottomSheet

def GradesPage(page: ft.Page):
    semester = ft.Ref[ft.Dropdown]()
    content_column = ft.Ref[ft.Column]()

    modal = GradeBottomSheet(None, None, None, None, None)
    
    def open_grade_modal(grade):
        global modal
        
        grade_display = grade.value

        modal = GradeBottomSheet(GradeDate=format_date(grade.created_at),GradeName=grade.subject,GradeDesc=grade.name,GradeValue=grade_display,GradeWeight=grade.weight)
        page.open(modal)
        page.update()

    def build_content_for_semester(selected_semester):
        all_grades = fetch_all_grades(selected_semester)
        panels = []
        subjects = {}

        for grade in all_grades:
            subject = grade.subject
            subjects.setdefault(subject, []).append(grade)

        for subject, grades_list in subjects.items():
            header = ft.Container(
                content=ft.Column([
                    ft.Text(subject, size=15),
                    ft.Row([
                        ft.Text(f"{len(grades_list)} " + _("grades"), size=14),
                        ft.Text((_("Average") + ": {:.2f}").format(calculate_weighted_average(grades_list)), size=14)
                    ])
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
                padding=10,
                expand=True,
            )

            grade_rows = []
            for grade in grades_list:
                grade_rows.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Container(
                                content=ft.Text(grade.value, text_align=ft.TextAlign.CENTER),
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                padding=12,
                                border_radius=5,
                                margin=5,
                                on_click=(lambda e, g=grade: open_grade_modal(g)),
                                width=41,
                                height=41,
                            ),
                            ft.Column([
                                ft.Text(grade.name),
                                ft.Row([
                                    ft.Text(format_date(grade.created_at)),
                                    ft.Text((_("Weight")) + ": {:.1f}".format(getattr(grade, 'weight', 1.0)))
                                ])
                            ], spacing=1)
                        ], expand=True),
                        on_click=(lambda e, g=grade: open_grade_modal(g)),
                    )
                )

            panel = ft.ExpansionPanel(
                header=header,
                content=ft.Column(grade_rows),
                expand=False,
            )
            panels.append(panel)

        return panels

    def on_semester_change(e):
        selected_sem = int(semester.current.value)
        panels = build_content_for_semester(selected_sem)
        content_column.current.controls = [
            ft.ExpansionPanelList(panels),
            modal
        ]
        page.update()

    return ft.Column([
        ft.Row([
            ft.Text((_("Grades")), size=30, weight="bold"),
            ft.Dropdown(
                ref=semester,
                width=150,
                value=str(getcurrentsemester()),
                options=[
                    ft.dropdown.Option("1", text=(_("Semester 1"))),
                    ft.dropdown.Option("2", text=(_("Semester 2"))),
                ],
                on_change=on_semester_change,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
        ft.Container(
            content=ft.Column(
                ref=content_column,
                controls=[
                    ft.ExpansionPanelList(build_content_for_semester(getcurrentsemester())),
                    modal
                ],
                scroll=True
            ),
            expand=True
        )

    ])
