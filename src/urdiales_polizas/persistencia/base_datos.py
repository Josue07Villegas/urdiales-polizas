"""Inicialización explícita de una base vacía; todavía no hay migraciones."""

from importlib.resources import files
from pathlib import Path
import sqlite3

TABLAS = frozenset({
    "asegurados", "contactos", "medios_contacto", "aseguradoras",
    "polizas", "vigencias", "vehiculos_asegurados", "cobros",
})
VERSION_ESQUEMA = 1


def abrir_conexion(ruta: Path | str) -> sqlite3.Connection:
    conexion = sqlite3.connect(str(ruta))
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def _leer_esquema() -> str:
    return files("urdiales_polizas.persistencia").joinpath("esquema.sql").read_text(
        encoding="utf-8"
    )


def _crear_esquema(conexion: sqlite3.Connection) -> None:
    try:
        conexion.executescript(
            "BEGIN IMMEDIATE;\n" + _leer_esquema()
            + f"\nPRAGMA user_version = {VERSION_ESQUEMA};\nCOMMIT;"
        )
    except sqlite3.Error:
        conexion.rollback()
        raise


def _tablas(conexion: sqlite3.Connection) -> frozenset[str]:
    return frozenset(fila[0] for fila in conexion.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' "
        "AND name NOT LIKE 'sqlite_%'"
    ))


def comprobar_esquema() -> int:
    """Comprueba el SQL empaquetado usando solamente memoria."""
    conexion = abrir_conexion(":memory:")
    try:
        _crear_esquema(conexion)
        if _tablas(conexion) != TABLAS:
            raise ValueError("El esquema no contiene las tablas esperadas.")
        return len(TABLAS)
    finally:
        conexion.close()


def inicializar_bd(ruta: Path) -> bool:
    """Devuelve True al crear; preserva bases de esta versión ya inicializadas.

    Una base con otro esquema se rechaza. No borra datos ni aplica migraciones.
    """
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = abrir_conexion(ruta)
    try:
        tablas = _tablas(conexion)
        version = conexion.execute("PRAGMA user_version").fetchone()[0]
        if tablas:
            if tablas != TABLAS or version != VERSION_ESQUEMA:
                raise ValueError("La base existente tiene otro esquema o versión.")
            return False
        if version != 0:
            raise ValueError("La base vacía tiene una versión no compatible.")
        _crear_esquema(conexion)
        return True
    finally:
        conexion.close()
