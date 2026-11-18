from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

RAIZ = Path(__file__).resolve().parents[1]


class EntradaTest(unittest.TestCase):
    def test_comprobar_funciona_sin_interfaz_y_no_crea_archivos(self):
        with TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            config = carpeta / "config.toml"
            config.write_text(
                '[aplicacion]\nnombre = "Prueba"\n'
                '[base_datos]\nruta = "datos/prueba.sqlite3"\n'
                '[atencion]\ndias_anticipacion = 30\n', encoding="utf-8",
            )
            resultado = subprocess.run(
                [sys.executable, str(RAIZ / "main.py"), "--config", str(config), "--comprobar"],
                cwd=carpeta, capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(resultado.returncode, 0, resultado.stderr)
            self.assertIn("8 tablas", resultado.stdout)
            self.assertFalse((carpeta / "datos").exists())

    def test_un_archivo_inexistente_devuelve_error_sin_traceback(self):
        with TemporaryDirectory() as temporal:
            resultado = subprocess.run(
                [sys.executable, str(RAIZ / "main.py"), "--config", "ausente.toml", "--comprobar"],
                cwd=temporal, capture_output=True, text=True, encoding="utf-8", check=False,
            )
            self.assertEqual(resultado.returncode, 1)
            self.assertIn("No se pudo iniciar", resultado.stderr)
            self.assertNotIn("Traceback", resultado.stderr)
