import flet as ft
from i18n import _
from datetime import datetime, timedelta
from sqlitehandlernr import fetch_timetable_for_day, create_timetable_database
from components.timetable import *
from sdk.src.interfaces.prometheus.interface import PrometheusInterface

def TimetablePage(page: ft.Page, interface: PrometheusInterface):
    current_day = datetime.today()
    current_month = current_day.month

    day_label = ft.Text(current_day.strftime("%A, %Y-%m-%d"), size=18, weight="bold")
    timetable_column = ft.Column([], expand=True, scroll=True)

    def on_month_change(start_of_month: datetime, end_of_month: datetime):
        print(f"Month changed! New month range: {start_of_month.strftime('%Y-%m-%d')} to {end_of_month.strftime('%Y-%m-%d')}")
        timetable = interface.get_timetable(from_=start_of_month, to=end_of_month)
        create_timetable_database(timetable_list=timetable)

    def fetch_day_data(date: datetime):
        print(f"Fetching for day: {date.strftime('%Y-%m-%d')}")
        timetable = fetch_timetable_for_day(day=date)
        timetable_column.controls = []
        
        for lesson in timetable:
            timetable_column.controls.append(LessonEntry(start_time=lesson.start, end_time=lesson.end, subject=lesson.subject, teacher=lesson.teacher, room=lesson.room, lesson_number=lesson.position, page=page, substitutiontype=lesson.substitutiontype))

        page.update()

    def on_day_change(new_date: datetime):
        nonlocal current_day, current_month
        new_month = new_date.month
        if new_month != current_month:
            current_month = new_month
            start_of_month = new_date.replace(day=1)
            end_day = monthrange(new_date.year, new_date.month)[1]
            end_of_month = new_date.replace(day=end_day)
            on_month_change(start_of_month, end_of_month)

        current_day = new_date
        day_label.value = current_day.strftime("%A, %Y-%m-%d")
        fetch_day_data(new_date)

    def previous_day(e):
        on_day_change(current_day - timedelta(days=1))

    def next_day(e):
        on_day_change(current_day + timedelta(days=1))

    def on_load():
        fetch_day_data(current_day)

    if page.route == "/timetable":
        on_load()

    return ft.Column([
        ft.Row([
            ft.Text("Timetable", size=30, weight="bold"),
            ft.Row([
                ft.IconButton(icon=ft.Icons.ARROW_LEFT, on_click=previous_day),
                day_label,
                ft.IconButton(icon=ft.Icons.ARROW_RIGHT, on_click=next_day),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
        timetable_column
    ])
