import flet as ft
import configparser
from i18n import _
from constants import *
from components.home import RecentGradesColumn
from utils import getconfigpath, getinitials

def HomePage():
    config = configparser.ConfigParser()
    config.read(f"{getconfigpath()}/config.ini")

    studentFullName = config['User']['fullName']
    studentClass = config['User']['grade']
    return ft.Column([
        ft.Text((_("Home")), size=30, weight="bold"),
        ft.Text("\n", size=30, weight="bold"),
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.CircleAvatar(
                                content=ft.Text(getinitials(studentFullName)),
                            ),
                            title=ft.Text(studentFullName),
                            subtitle=ft.Text(studentClass),
                        ),
                    ]
                ),
                        width=400,
                        padding=10
            ),
        ),
        ft.Row([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.BACKPACK_OUTLINED, size=32, color="#FFFFFF"),
                            ft.Text((_("Timetable")), size=24, font_family="Roboto", weight="bold")
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
                    #margin=20,
                    padding=10,
                    alignment=ft.alignment.top_left,
                    ),
                width=420,
                height=275, 
            ),
            
            ft.Card(
                content=ft.Container(
                    content=RecentGradesColumn(),
                    #margin=20,
                    padding=10,
                    alignment=ft.alignment.top_left,
                    #bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    #width=420,
                    #height=270,
                    #border_radius=10
                    ),
                width=420,
                height=275,
            ),
        ]),
    ])