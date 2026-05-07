import flet as ft
from datetime import datetime

def DashboardView(page, tarea_controller):
    user = getattr(page, "user_data", None)

    lista_tareas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)

    fecha_limite = ft.DatePicker(
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2030, 12, 31)
    )

    hora_limite = ft.TimePicker()

    page.overlay.append(fecha_limite)
    page.overlay.append(hora_limite)

    # ---------------- PICKERS ----------------
    def abrir_calendario(e):
        fecha_limite.open = True
        page.update()

    def abrir_reloj(e):
        hora_limite.open = True
        page.update()

    btn_fecha = ft.ElevatedButton(
        "Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=abrir_calendario
    )

    btn_hora = ft.ElevatedButton(
        "Hora",
        icon=ft.Icons.ACCESS_TIME,
        on_click=abrir_reloj
    )

    txt_fecha = ft.Text("Fecha: No seleccionada")
    txt_hora = ft.Text("Hora: No seleccionada")

    def actualizar_fecha(e):
        if fecha_limite.value:
            txt_fecha.value = f"Fecha: {fecha_limite.value.strftime('%d/%m/%Y')}"
        else:
            txt_fecha.value = "Fecha: No seleccionada"
        page.update()

    def actualizar_hora(e):
        if hora_limite.value:
            txt_hora.value = f"Hora: {hora_limite.value.strftime('%H:%M')}"
        else:
            txt_hora.value = "Hora: No seleccionada"
        page.update()

    fecha_limite.on_change = actualizar_fecha
    hora_limite.on_change = actualizar_hora

    # ---------------- TAREAS ----------------
    def eliminar_tarea(id_tarea):
        success, msg = tarea_controller.eliminar_tarea(id_tarea)

        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

        if success:
            cargar_tareas()

    def cargar_tareas():
        lista_tareas.controls.clear()

        if user and "id_usuario" in user:
            tareas = tarea_controller.obtener_lista(user["id_usuario"])

            for t in tareas:
                lista_tareas.controls.append(
                    ft.Container(
                        padding=10,
                        border=ft.border.all(1),
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(t["titulo"], weight="bold"),
                                        ft.Text(t.get("descripcion", "")),
                                        ft.Text(f"Estado: {t.get('estado','pendiente')}")
                                    ],
                                    expand=True
                                ),

                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, id=t["id_tarea"]: eliminar_tarea(id)
                                )
                            ]
                        )
                    )
                )

        page.update()

    txt_titulo = ft.TextField(label="Título", expand=True)
    txt_descripcion = ft.TextField(label="Descripción", expand=True, multiline=True)

    prioridad = ft.Dropdown(
        label="Prioridad",
        value="media",
        options=[
            ft.dropdown.Option("alta"),
            ft.dropdown.Option("media"),
            ft.dropdown.Option("baja"),
        ]
    )

    clasificacion = ft.Dropdown(
        label="Clasificación",
        value="personal",
        options=[
            ft.dropdown.Option("personal"),
            ft.dropdown.Option("trabajo"),
            ft.dropdown.Option("estudio"),
            ft.dropdown.Option("hogar"),
        ]
    )

    estado = ft.Dropdown(
        label="Estado",
        value="pendiente",
        options=[
            ft.dropdown.Option("pendiente"),
            ft.dropdown.Option("en_progreso"),
            ft.dropdown.Option("completada"),
        ]
    )

    def agregar_tarea(e):
        if user and "id_usuario" in user:

            val_fecha = None
            val_hora = None

            if fecha_limite.value:
                val_fecha = fecha_limite.value.strftime('%Y-%m-%d')

            if hora_limite.value:
                val_hora = hora_limite.value.strftime('%H:%M:%S')

            success, msg = tarea_controller.guardar_nueva(
                user["id_usuario"],
                txt_titulo.value,
                txt_descripcion.value,
                prioridad.value,
                clasificacion.value,
                estado.value,
                val_fecha,
                val_hora
            )

            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()

            if success:
                txt_titulo.value = ""
                txt_descripcion.value = ""
                fecha_limite.value = None
                hora_limite.value = None
                txt_fecha.value = "Fecha: No seleccionada"
                txt_hora.value = "Hora: No seleccionada"
                cargar_tareas()

    def mostrar_perfil(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Usuario: {user.get('nombre','')}"))
        page.snack_bar.open = True
        page.update()

    def logout(e):
        page.go("/")

    cargar_tareas()

    return ft.View(
        route="/dashboard",
        controls=[

            ft.AppBar(
                title=ft.Text(f"Bienvenido {user.get('nombre','Usuario')}"),
                actions=[
                    ft.IconButton(ft.Icons.PERSON, on_click=mostrar_perfil),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=logout)
                ],
            ),

            ft.Container(
                padding=20,
                content=ft.Column(
                    [

                        ft.Text("Nueva tarea", size=18, weight="bold"),

                        txt_titulo,
                        txt_descripcion,

                        ft.Row([prioridad, clasificacion, estado]),

                        ft.Row([btn_fecha, btn_hora]),

                        ft.Row([txt_fecha, txt_hora]),

                        ft.ElevatedButton(
                            "Guardar",
                            on_click=agregar_tarea
                        ),

                        ft.Divider(),

                        ft.Text("Mis tareas", size=18, weight="bold"),

                        lista_tareas
                    ]
                )
            ),
        ]
    )