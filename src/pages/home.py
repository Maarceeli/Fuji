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
                                ft.Placeholder()
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
                        
                        ft.Placeholder()
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
