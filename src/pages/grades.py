import flet as ft
from sqlitehandlernr import fetch_all_grades
from i18n import _

def parse_grade_value(value):
    try:
        base_value = float(value.rstrip('+-'))
        if value.endswith('+'):
            return base_value + 0.25
        elif value.endswith('-'):
            return base_value - 0.25
        return base_value
    except ValueError:
        return None

def format_date(dt):
    return dt.strftime("%Y/%m/%d")

def GradesPage(page):
    grades = fetch_all_grades()
    panels = []
    subjects = {}
    
    for grade in grades:
        subject = grade.subject
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(grade)
    
    modal = ft.BottomSheet(
        content=ft.Column([], spacing=5),
        enable_drag=True,
        open=False,
    )
    
    def open_grade_modal(grade):
        parsed_value = parse_grade_value(grade.value)
        grade_display = f"{grade.value}" if parsed_value is not None else _("Grade not recognized")
        
        modal.content = ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(grade.subject, size=30, weight=ft.FontWeight.BOLD),
                        ft.Text(grade.name, size=18, color=ft.Colors.WHITE70),
                    ], spacing=3, tight=True),
                    padding=ft.padding.only(left=20, top=-20, bottom=5, right=20),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(grade_display, size=48, weight=ft.FontWeight.BOLD),
                            width=80,
                            height=80,
                            bgcolor=ft.Colors.GREEN_700,
                            border_radius=ft.border_radius.only(top_left=8, top_right=8),
                            alignment=ft.alignment.center,
                            margin=ft.margin.only(bottom=5, top=40)
                        ),
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(name=ft.Icons.SCALE, size=16, color=ft.Colors.WHITE70),
                                ft.Text(f"{getattr(grade, 'weight', 1.0):.2f}", size=16),
                            ], spacing=5, alignment=ft.MainAxisAlignment.CENTER),
                            width=80,
                            height=30,
                            bgcolor=ft.Colors.GREEN_700,
                            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
                            alignment=ft.alignment.center,
                        ),
                    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(right=20, top=-5, bottom=10),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Card(
                content=ft.Row([
                    ft.Container(
                            content=ft.Icon(name=ft.Icons.LOOKS_6_ROUNDED, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                    ),
                    ft.Column([
                        ft.Text("Grade", size=14, color=ft.Colors.WHITE70),
                        ft.Text(grade_display, size=20),
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True)
                ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                height=75,
                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                margin=ft.margin.only(left=15, right=15, bottom=5),
            ),
            ft.Card(
                content=ft.Row([
                    ft.Container(
                            content=ft.Icon(name=ft.Icons.SCALE, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                    ),
                    ft.Column([
                        ft.Text("Weight", size=14, color=ft.Colors.WHITE70),
                        ft.Text(f"{getattr(grade, 'weight', 1.0):.2f}", size=20),
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True)
                ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                height=75,
                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                margin=ft.margin.only(left=15, right=15, top=5, bottom=5),
            ),
            ft.Card(
                content=ft.Row([
                    ft.Container(
                            content=ft.Icon(name=ft.Icons.CALENDAR_TODAY, size=20),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(left=10),
                    ),
                    ft.Column([
                        ft.Text("Date", size=14, color=ft.Colors.WHITE70),
                        ft.Text(format_date(grade.created_at), size=20),
                    ], spacing=2, alignment=ft.MainAxisAlignment.CENTER, expand=True)
                ], spacing=15, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                height=75,
                color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                margin=ft.margin.only(left=15, right=15, bottom=5, top=5),
            ),
        ], spacing=5)
        modal.open = True
        page.update()
    
    for subject, grades_list in subjects.items():
        header = ft.Container(
            content=ft.Column([
                ft.Text(subject, size=15),
                ft.Row([
                    ft.Text(f"{len(grades_list)} " + _("grades"), size=14),
                    ft.Text((_("Average")) + ": {:.2f}".format(
                        sum(parse_grade_value(g.value) for g in grades_list if parse_grade_value(g.value) is not None) / max(len([g for g in grades_list if parse_grade_value(g.value) is not None]), 1)
                    ), size=14),
                ])
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START, expand=True),
            padding=ft.padding.all(10),
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
                            padding=ft.padding.symmetric(horizontal=12, vertical=8),
                            border_radius=5,
                            margin=ft.margin.all(5),
                            on_click=lambda e, grade=grade: open_grade_modal(grade),
                        ),
                        ft.Column([
                            ft.Text(grade.name),
                            ft.Row([
                                ft.Text(format_date(grade.created_at)),
                                ft.Text((_("Weight")) + ": {:.1f}".format(getattr(grade, 'weight', 1.0)))
                            ])
                        ], spacing=1)
                    ], expand=True),
                    on_click=lambda e, grade=grade: open_grade_modal(grade),
                )
            )
        
        panel = ft.ExpansionPanel(
            header=header,
            content=ft.Column(grade_rows),
            expand=False,
        )
        panels.append(panel)
    
    return ft.Column([
        ft.Text((_("Grades")), size=30, weight="bold"),
        ft.ExpansionPanelList(panels),
        modal
    ], scroll=True)
