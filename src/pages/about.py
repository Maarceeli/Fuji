import flet as ft
from i18n import _
import sys
import os
from version import ver

def AboutPage(BASE_DIR):
    return ft.Column([
        ft.Text((_("About")), size=30, weight="bold"),
        ft.Row([
            ft.Image(
                src=f"{BASE_DIR}/assets/logo.png",
                width=64,
                fit=ft.ImageFit.CONTAIN,
                border_radius=ft.border_radius.all(100000)
            ),
            ft.Text("Fuji", size=32, weight="normal")
        ], alignment=ft.MainAxisAlignment.CENTER),  # You can also remove `expand=True`
        ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO, color=ft.Colors.WHITE),
                    ft.Text(f"Version: {ver}")
                ]),
                padding=10
            ),
            width=max,
            height=75,
            
        )
    ])

        
        