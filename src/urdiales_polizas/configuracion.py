"""Lectura de configuración TOML sin modificar el archivo original."""

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class Configuracion:
    nombre: str
    ruta_bd: Path
    dias_anticipacion: int


def cargar_configuracion(archivo: Path) -> Configuracion:
    archivo = archivo.resolve()
    with archivo.open("rb") as entrada:
        datos = tomllib.load(entrada)

    try:
        nombre = datos["aplicacion"]["nombre"]
        ruta = datos["base_datos"]["ruta"]
        dias = datos["atencion"]["dias_anticipacion"]
    except (KeyError, TypeError) as error:
        raise ValueError("Faltan campos requeridos en la configuración TOML.") from error

    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre de la aplicación debe ser texto no vacío.")
    if not isinstance(ruta, str) or not ruta.strip():
        raise ValueError("La ruta de la base de datos debe ser texto no vacío.")
    if type(dias) is not int or dias < 0:
        raise ValueError("Los días de anticipación deben ser un entero no negativo.")

    ruta_bd = Path(ruta).expanduser()
    if not ruta_bd.is_absolute():
        ruta_bd = archivo.parent / ruta_bd
    return Configuracion(nombre.strip(), ruta_bd.resolve(), dias)
