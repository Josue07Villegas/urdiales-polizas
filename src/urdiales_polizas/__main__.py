"""Punto de entrada del proyecto."""

import argparse
from pathlib import Path
import sqlite3
import sys

from urdiales_polizas import __version__
from urdiales_polizas.configuracion import cargar_configuracion
from urdiales_polizas.persistencia.base_datos import comprobar_esquema, inicializar_bd


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Base de Urdiales Asesores.")
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--config", type=Path,
        default=Path("config.toml") if Path("config.toml").is_file()
        else Path("config.example.toml"),
        help="Archivo TOML; las rutas relativas se resuelven desde ese archivo.",
    )
    acciones = parser.add_mutually_exclusive_group()
    acciones.add_argument(
        "--comprobar", action="store_true",
        help="Validar configuración y SQL en memoria sin crear la base local.",
    )
    acciones.add_argument(
        "--inicializar-bd", action="store_true",
        help="Crear una base vacía o comprobar su versión si ya existe.",
    )
    argumentos = parser.parse_args(argv)
    try:
        config = cargar_configuracion(argumentos.config)
        if argumentos.comprobar:
            tablas = comprobar_esquema()
            print(f"Configuración válida. Anticipación: {config.dias_anticipacion} días.")
            print(f"Esquema válido: {tablas} tablas comprobadas en memoria.")
            print(f"Base prevista: {config.ruta_bd}")
            print("No se creó ni modificó la base de datos local.")
        elif argumentos.inicializar_bd:
            creada = inicializar_bd(config.ruta_bd)
            estado = "Base vacía creada" if creada else "Base existente conservada"
            print(f"{estado}: {config.ruta_bd}")
        else:
            try:
                from urdiales_polizas.interfaz.ventana_principal import iniciar_interfaz
            except ImportError as error:
                raise RuntimeError(
                    "Tkinter no está disponible. Instala el soporte de Tkinter de tu Python."
                ) from error
            iniciar_interfaz(config)
    except (OSError, ValueError, sqlite3.Error, RuntimeError) as error:
        print(f"No se pudo iniciar: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
