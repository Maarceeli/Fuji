import flet as ft
from vars import *

def HomePage():
    return ft.Column([
            ft.Text("  Home", size=30, weight="bold"),
            ft.Text("\n", size=30, weight="bold"),
            ft.Row([
                ft.Container( # Timetable Card
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.BACKPACK_OUTLINED, size=32, color="#FFFFFF"),
                            ft.Text("Timetable", size=24, font_family="Roboto", weight="bold")
                        ]),
                        ft.ListView(
                            controls=[
                                ft.Text("1. Lorem ipsum\n2. Lorem ipsum\n3. Lorem ipsum\n4. Im curious what happens if i ran out of space\n5. It just creates a new line\n6. No idea why i tested that\n7. I also want to test what happens if there is too much lines\n8. Lorem ipsum\n9. Yay now you can scroll\n10. Looks like dogshit but it works\n11. Simi simi jej simi jaj", size=16, weight="normal")
                            ],
                            expand=True,
                            spacing=10,
                            padding=10,
                            auto_scroll=False
                        )
                    ]), 
                    margin=20,
                    padding=10,
                    alignment=ft.alignment.top_left,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    width=420,
                    height=270,
                    border_radius=10,
                ),
                
                ft.Container( # Recent Grades Card
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_6_OUTLINED, size=32, color="#FFFFFF"),
                            ft.Text("Recent Grades", size=24, font_family="Roboto", weight="bold")
                        ]),
                        ft.ListView(
                            controls=[
                                ft.Row([
                                    ft.Text("Matematyka", size=16, weight="normal"),
                                    ft.Container(
                                        content=ft.Text("6"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[6],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                    ft.Container(
                                        content=ft.Text("5"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[5],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                    ft.Container(
                                        content=ft.Text("4"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[4],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                    ft.Container(
                                        content=ft.Text("3"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[3],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                    ft.Container(
                                        content=ft.Text("2"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[2],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                    ft.Container(
                                        content=ft.Text("1"),
                                        margin=0,
                                        padding=0,
                                        alignment=ft.alignment.center,
                                        bgcolor=grade[1],
                                        width=20,
                                        height=20,
                                        border_radius=5,
                                    ),
                                ])
                            ],
                            expand=False,
                            spacing=10,
                            padding=10,
                            auto_scroll=False
                        )
                    ]), 
                    margin=20,
                    padding=10,
                    alignment=ft.alignment.top_left,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    width=420,
                    height=270,
                    border_radius=10,
                )
            ])
        ])