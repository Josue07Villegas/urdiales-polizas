"""Permite probar el código fuente desde el repositorio sin instalarlo."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
