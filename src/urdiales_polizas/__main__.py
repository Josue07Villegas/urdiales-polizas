"""Punto de entrada del proyecto."""

import argparse

from urdiales_polizas import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Base de Urdiales Asesores.")
    parser.add_argument("--version", action="version", version=__version__)
    parser.parse_args(argv)
    print("Estructura inicial creada. Los casos de uso están pendientes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
