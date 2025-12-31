import flet as ft
from core.ai import bode_responder

def main(page: ft.Page):
    page.title = "FENIX MOBILE"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_always_on_top = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0a0a0a"
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    page.theme = ft.Theme(visual_density=ft.VisualDensity.COMPACT)
    
    header = ft.Text("NÚCLEO FENIX", size=28, weight="bold", color="#00fbff")
    chat_display = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    def enviar_comando(e):
        if not entrada.value: return
        chat_display.controls.append(ft.Text(f"Senhor: {entrada.value}", color="white"))
        cmd_atual = entrada.value
        entrada.value = ""
        page.update()
        
        resposta = bode_responder(cmd_atual)
        chat_display.controls.append(ft.Text(f"Feni: {resposta}", color="#00fbff", weight="bold"))
        page.update()

    entrada = ft.TextField(
        hint_text="Comando neural...",
        border_color="#00fbff",
        expand=True,
        on_submit=enviar_comando,
    )

    page.add(
        header,
        ft.Divider(color="#1f1f1f"),
        ft.Container(content=chat_display, expand=True, border=ft.Border.all(1, "#1f1f1f"), border_radius=10, padding=10),
        ft.Row(
            controls=[
                entrada, 
                ft.IconButton(
                    icon=ft.Icons.SEND, # CORREÇÃO: Usando a constante exata da biblioteca
                    icon_color="#00fbff", 
                    on_click=enviar_comando
                )
            ]
        )
    )

if __name__ == "__main__":
    import os
    # Pega a porta do Railway ou usa a 8550 por padrão
    port = int(os.getenv("PORT", 8550)) 
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")