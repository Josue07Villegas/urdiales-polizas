"""Permite ejecutar el proyecto desde el repositorio sin instalar paquetes."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from urdiales_polizas.__main__ import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
