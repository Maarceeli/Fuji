import flet as ft
from i18n import _


def ExamsPage(page: ft.Page):
    return ft.Column([
        ft.Row([
            ft.Text((_("Exams")), size=30, weight="bold"),
            ft.Row(
                [
                    ft.IconButton(icon=ft.icons.ARROW_LEFT),
                    ft.Text("14.04-20.04", size=18, weight="bold"),
                    ft.IconButton(icon=ft.icons.ARROW_RIGHT),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Row([
                                ft.Text("Example subject" ,weight="bold"),
                                ft.Row(
                                    [
                                        ft.Text("14.04.2025"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                            subtitle=ft.Row([
                                ft.Text("Short test - Example description"),
                                ft.Row(
                                    [
                                        ft.Text("Example teacher"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                        )

                    ]
                ),
                padding=5,
            )
    ),
    ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Row([
                                ft.Text("Example subject" ,weight="bold"),
                                ft.Row(
                                    [
                                        ft.Text("14.04.2025"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                            subtitle=ft.Row([
                                ft.Text("Short test - Example description"),
                                ft.Row(
                                    [
                                        ft.Text("Example teacher"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER
                                )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, spacing=10),
                        )

                    ]
                ),
                padding=5,
            )
    )
    ])
