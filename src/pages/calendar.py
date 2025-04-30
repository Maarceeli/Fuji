import flet as ft
from i18n import _
from datetime import datetime, timedelta
from sqlitehandlernr import fetch_exams_for_week, create_exams_database, fetch_homework_for_week, create_homework_database
from components.calendar import *
from sdk.src.interfaces.prometheus.interface import PrometheusInterface
from calendar import monthrange
from collections import defaultdict

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
    calendar_column = ft.Column([], expand=True)

    def on_month_change(start_of_month: datetime, end_of_month: datetime):
        print(f"Month changed! New month range: {start_of_month.strftime('%Y-%m-%d')} to {end_of_month.strftime('%Y-%m-%d')}")
        
        exams_ = interface.get_exams(from_=start_of_month, to=end_of_month)
        create_exams_database(exams_)

        homework_ = interface.get_homework(from_=start_of_month, to=end_of_month)
        create_homework_database(homework_)
        
    def fetch_week_data(start_date: datetime):
        print(f"Fetching for week starting on: {start_date.strftime('%Y-%m-%d')}")
        exams = fetch_exams_for_week(start_date)
        homework = fetch_homework_for_week(start_date)

        entries_by_day = defaultdict(list)

        for exam in exams:
            day = exam.deadline
            entries_by_day[day].append(("exam", exam))

        for hw in homework:
            day = hw.deadline
            entries_by_day[day].append(("homework", hw))

        sorted_days = sorted(entries_by_day.keys())

        calendar_column.controls = []

        for day in sorted_days:
            for entry_type, entry in entries_by_day[day]:
                match entry_type:
                    case "exam":
                        calendar_column.controls.append(ExamEntry(
                            entry.deadline, entry.description, entry.subject, entry.creator, entry.type, entry.created_at, page=page
                        ))
                    case "homework":
                        calendar_column.controls.append(HomeworkEntry(
                            entry.deadline, entry.description, entry.subject, entry.creator, entry.created_at, page=page
                        ))

        page.update()
        print(calendar_column.controls)


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
        calendar_column
    ])

