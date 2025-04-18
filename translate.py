import flet as ft
import requests

# Función para consumir la API REST
def translate_text(e):
    # Obtener el control de la página
    page = e.page
    input_text = input_box.value
    if not input_text.strip():
        output_box.value = "Por favor, ingresa un texto para traducir."
        page.update()
        return

    # Consumir la API REST
    url = "http://127.0.0.1:8000/translate"  # Ruta correcta de la API Flask
    try:
        response = requests.post(url, json={"text": input_text})
        if response.status_code == 200:
            translated_text = response.json().get("translated_text", "Error en la traducción")
            output_box.value = translated_text
        else:
            output_box.value = f"Error: {response.status_code} - No se pudo traducir el texto."
    except requests.ConnectionError:
        output_box.value = "Error: No se pudo conectar con el servidor. Verifica que la API está corriendo."
    except Exception as ex:
        output_box.value = f"Error inesperado: {str(ex)}"
    
    page.update()

# Interfaz con Flet
def main(page: ft.Page):
    # Declarar variables como globales para que sean accesibles dentro de translate_text
    global input_box, output_box

    # Configuración de la página
    page.title = "Traductor SDC Learning"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"

    # Encabezado
    header = ft.Text(
        "Traductor SDC Learning", 
        size=30, 
        weight="bold", 
        color=ft.colors.BLUE
    )

    # Cajas de texto (lado izquierdo y derecho)
    input_box = ft.TextField(
        label="Texto de origen", 
        hint_text="Escribe aquí el texto que deseas traducir...", 
        multiline=True, 
        width=400, 
        height=200
    )
    output_box = ft.TextField(
        label="Texto traducido", 
        hint_text="La traducción aparecerá aquí...", 
        multiline=True, 
        width=400, 
        height=200, 
        read_only=True
    )

    # Botón de traducción (centrado entre las cajas)
    translate_button = ft.ElevatedButton(
        "Traducir", 
        icon=ft.icons.TRANSLATE, 
        on_click=translate_text,  # Llamar directamente a la función
        width=150
    )

    # Layout principal
    page.add(
        ft.Column(
            [
                header,
                ft.Row(
                    [
                        input_box,  # Caja de texto a la izquierda
                        ft.Column(
                            [
                                translate_button  # Botón centrado
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        output_box  # Caja de texto a la derecha
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

# Ejecutar Flet
ft.app(target=main)
