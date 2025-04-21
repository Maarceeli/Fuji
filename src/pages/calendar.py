import flet as ft
from i18n import _
from datetime import datetime, timedelta

def get_week_range(start_date: datetime):
    start_of_week = start_date - timedelta(days=start_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return f"{start_of_week.strftime('%d.%m')}-{end_of_week.strftime('%d.%m')}"

def CalendarPage(page: ft.Page):
    current_week_start = datetime.today() - timedelta(days=datetime.today().weekday())

    week_label = ft.Text(get_week_range(current_week_start), size=18, weight="bold")

    def on_week_change(new_start_date):
        week_label.value = get_week_range(new_start_date)
        page.update()
        print("Selected week start:", new_start_date.strftime("%Y-%m-%d"))  # Your custom logic here

    def previous_week(e):
        nonlocal current_week_start
        current_week_start -= timedelta(weeks=1)
        on_week_change(current_week_start)

    def next_week(e):
        nonlocal current_week_start
        current_week_start += timedelta(weeks=1)
        on_week_change(current_week_start)

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
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
    ])
