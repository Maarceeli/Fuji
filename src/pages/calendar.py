import flet as ft
from i18n import _
from datetime import datetime, timedelta
from sqlitehandlernr import fetch_exams_for_week, create_exams_database
from components.calendar import *
from sdk.src.interfaces.prometheus.interface import PrometheusInterface
from calendar import monthrange

def get_month_range(date: datetime):
    start = date.replace(day=1)
    end_day = monthrange(date.year, date.month)[1]
    end = date.replace(day=end_day)
    return start, end

def get_week_range(start_date: datetime):
    start_of_week = start_date - timedelta(days=start_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return f"{start_of_week.strftime('%d.%m')}-{end_of_week.strftime('%d.%m')}"

def CalendarPage(page: ft.Page, interface: PrometheusInterface):
    current_week_start = datetime.today() - timedelta(days=datetime.today().weekday())
    current_month = current_week_start.month  # Initial month
    week_label = ft.Text(get_week_range(current_week_start), size=18, weight="bold")
    exams_column = ft.Column([], expand=True)

    def on_month_change(start_of_month: datetime, end_of_month: datetime):
        print(f"Month changed! New month range: {start_of_month.strftime('%Y-%m-%d')} to {end_of_month.strftime('%Y-%m-%d')}")
        
        exams_ = interface.get_exams(from_=start_of_month, to=end_of_month)
        create_exams_database(exams_)
        

    def fetch_week_data(start_date: datetime):
        print(f"Fetching for week starting on: {start_date.strftime('%Y-%m-%d')}")
        exams = fetch_exams_for_week(start_date)

        exams_column.controls = []
        for exam in exams:
            exams_column.controls.append(ExamEntry(exam.deadline, exam.description, exam.subject, exam.creator, exam.type, exam.created_at, page=page))
        page.update()

    def on_week_change(new_start_date):
        nonlocal current_week_start, current_month
        new_month = new_start_date.month
        if new_month != current_month:
            current_month = new_month
            start_of_month, end_of_month = get_month_range(new_start_date)
            on_month_change(start_of_month, end_of_month)

        current_week_start = new_start_date
        week_label.value = get_week_range(new_start_date)
        page.update()
        fetch_week_data(new_start_date)

    def previous_week(e):
        on_week_change(current_week_start - timedelta(weeks=1))

    def next_week(e):
        on_week_change(current_week_start + timedelta(weeks=1))

    def on_load():
        fetch_week_data(current_week_start)

    if page.route == "/calendar":
        on_load()

    return ft.Column([
        ft.Row([
            ft.Text((_("Calendar")), size=30, weight="bold"),
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.ARROW_LEFT, on_click=previous_week),
                    week_label,
                    ft.IconButton(icon=ft.icons.ARROW_RIGHT, on_click=next_week),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
        exams_column
    ])

