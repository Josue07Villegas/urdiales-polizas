"""Ventana inicial sin conexión a los casos de uso pendientes."""

import tkinter as tk
from tkinter import ttk

from urdiales_polizas.configuracion import Configuracion


def crear_ventana(config: Configuracion) -> tk.Tk:
    ventana = tk.Tk()
    ventana.title(config.nombre)
    ventana.geometry("1000x620")
    ventana.minsize(820, 500)

    contenedor = ttk.Frame(ventana, padding=24)
    contenedor.pack(fill="both", expand=True)
    ttk.Label(contenedor, text="Urdiales Asesores", font=("Arial", 22, "bold")).pack(
        anchor="w"
    )
    ttk.Label(contenedor, text="Clientes y pólizas · Prototipo inicial").pack(
        anchor="w", pady=(4, 18)
    )

    pestanas = ttk.Notebook(contenedor)
    pestanas.pack(fill="both", expand=True)
    for titulo, descripcion in (
        ("Cartera", "Pólizas actuales y próximas fechas de atención."),
        ("Clientes", "Datos de asegurados y sus contactos."),
        ("Histórico", "Vigencias anteriores y vencidas."),
    ):
        pagina = ttk.Frame(pestanas, padding=16)
        pestanas.add(pagina, text=titulo)
        ttk.Label(pagina, text=descripcion).pack(anchor="w", pady=(0, 12))
        ttk.Label(
            pagina,
            text="Esta pantalla está en preparación. Aún no permite capturar ni consultar registros.",
            wraplength=700,
        ).pack(anchor="w")

    ttk.Button(contenedor, text="Cerrar", command=ventana.destroy).pack(
        anchor="e", pady=(18, 0)
    )
    return ventana


def iniciar_interfaz(config: Configuracion) -> None:
    try:
        ventana = crear_ventana(config)
    except tk.TclError as error:
        raise RuntimeError(
            "No hay pantalla gráfica disponible. Usa --comprobar para revisar la base del proyecto."
        ) from error
    ventana.mainloop()
