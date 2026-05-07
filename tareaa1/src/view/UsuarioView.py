import flet as ft

def UserView(page, auth_controller):
    page.title = "Perfil"
    user = getattr(page, "user_data", None)

    def formatear_fecha(fecha):
        if not fecha:
            return "No disponible"

        if isinstance(fecha, str) and " " in fecha:
            fecha_parte, hora_parte = fecha.split(" ")
            año, mes, dia = fecha_parte.split("-")
            return f"{dia}/{mes}/{año} {hora_parte}"

        if isinstance(fecha, str):
            año, mes, dia = fecha.split("-")
            return f"{dia}/{mes}/{año}"

        return str(fecha)

    nombre = ft.Text(f"Nombre: {user['nombre'] if user else 'Usuario'}", size=18)
    apellido = ft.Text(f"Apellido: {user['apellido'] if user else 'Usuario'}", size=18)
    telefono = ft.Text(f"Teléfono: {user['telefono'] if user else 'Usuario'}", size=18)
    email = ft.Text(f"Email: {user['email'] if user else 'Usuario'}", size=18)

    fecha_registro = ft.Text(
        f"Creación: {formatear_fecha(user['fecha_registro']) if user else 'Usuario'}",
        size=18
    )

    ultimo_acceso = ft.Text(
        f"Último acceso: {formatear_fecha(user['ultimo_acceso']) if user else 'Usuario'}",
        size=18
    )

    return ft.View(
        route="/perfil",
        controls=[

            ft.AppBar(
                title=ft.Text("Perfil de Usuario"),
                bgcolor=ft.Colors.BLUE_GREY_400,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(ft.Icons.BOOK, on_click=lambda _: page.go("/dashboard")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
            ),

            ft.Container(
                padding=20,
                content=ft.Column(
                    [

                        ft.Text("Información del usuario", size=22, weight="bold", color=ft.Colors.BLUE_GREY_700),

                        ft.Divider(),

                        nombre,
                        apellido,
                        telefono,
                        email,

                        ft.Divider(),

                        fecha_registro,
                        ultimo_acceso
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ]
    )