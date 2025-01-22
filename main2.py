import flet as ft

def main(page: ft.Page):

    t = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Home",
                icon=ft.Icon(ft.Icons.HOME),
                content=ft.Text("Home"),
            ),
            ft.Tab(
                text="Grades",
                icon=ft.Icons.LOOKS_6_OUTLINED,
                content=ft.Text("Grades"),
            ),
            ft.Tab(
                text="Timetable",
                icon=ft.Icons.BACKPACK_OUTLINED,
                content=ft.Text("Timetable"),
            ),
            ft.Tab(
                text="Homework",
                icon=ft.Icons.BOOK_OUTLINED,
                content=ft.Text("Homework"),
            ),
            ft.Tab(
                text="Exams",
                icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
                content=ft.Text("Exams"),
            ),
            ft.Tab(
                text="Behaviour",
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED,
                content=ft.Text("Behaviour"),
            ),
            ft.Tab(
                text="Attendance",
                icon=ft.Icons.STICKY_NOTE_2_OUTLINED,
                content=ft.Text("Attendance"),
            ),
            ft.Tab(
                text="Settings",
                icon=ft.Icons.SETTINGS_OUTLINED,
                content=ft.Text("Settings"),
            ),
        ],
        expand=1,
    )

    page.add(t)

ft.app(main)