import flet as ft
from i18n import _


def GradesPage(page):  # Funkcja wymaga 'page' jako argument
    modal = ft.AlertDialog(
        modal=True,
        title=ft.Text((_("Test modal"))),
        content=ft.Placeholder(),
        actions=[
            ft.TextButton("OK", on_click=lambda e: page.close(modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    header = ft.Container(
        content=ft.Column(
            [
                ft.Text("Matematyka", size=15),
                ft.Row([
                    ft.Text("4 "+(_("grades")), size=14),
                    ft.Text((_("Average"))+": 1.00", size=14),
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        ),
        padding=ft.padding.all(10),
        expand=True,
    )

    panel = ft.ExpansionPanel(
        header=header,
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text("1", text_align=ft.TextAlign.CENTER),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    padding=10,
                    border_radius=5,
                    width=40,
                    margin=ft.margin.all(5),
                    on_click=lambda e: page.open(modal)  # Użycie lambda, aby opóźnić wywołanie
                ),
                ft.Column(
                    [
                        ft.Text("wiązania"),
                        ft.Row([
                            ft.Text("21.02.2025"),
                            ft.Text("Waga: 1.0"),
                        ])
                    ],
                    spacing=1
                ),
            ]),
            ft.Row([
                ft.Container(
                    content=ft.Text("1", text_align=ft.TextAlign.CENTER),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    padding=10,
                    border_radius=5,
                    width=40,
                    margin=ft.margin.all(5),
                    on_click=lambda e: page.open(modal)  # Użycie lambda, aby opóźnić wywołanie
                ),
                ft.Column(
                    [
                        ft.Text("wiązania"),
                        ft.Row([
                            ft.Text("21.02.2025"),
                            ft.Text("Waga: 1.0"),
                        ])
                    ],
                    spacing=1
                ),
            ]),
        ]),
        expand=False,
    )

    return ft.Column([
        ft.Text((_("Grades")), size=30, weight="bold"),
        ft.ExpansionPanelList([panel]),
        ft.ExpansionPanelList([panel])
    ])