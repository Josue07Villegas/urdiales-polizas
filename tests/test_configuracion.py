from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from urdiales_polizas.configuracion import cargar_configuracion


class ConfiguracionTest(unittest.TestCase):
    def test_resuelve_la_base_desde_el_archivo_toml(self):
        with TemporaryDirectory() as temporal:
            carpeta = Path(temporal)
            archivo = carpeta / "config.toml"
            archivo.write_text(
                '[aplicacion]\nnombre = "Prueba"\n'
                '[base_datos]\nruta = "local/prueba.sqlite3"\n'
                '[atencion]\ndias_anticipacion = 30\n', encoding="utf-8",
            )
            config = cargar_configuracion(archivo)
            self.assertEqual(config.ruta_bd, carpeta / "local/prueba.sqlite3")
            self.assertEqual(config.dias_anticipacion, 30)
            self.assertFalse(config.ruta_bd.exists())

    def test_rechaza_anticipaciones_invalidas(self):
        for valor in ("-1", "true", '"30"'):
            with self.subTest(valor=valor), TemporaryDirectory() as temporal:
                archivo = Path(temporal) / "config.toml"
                archivo.write_text(
                    '[aplicacion]\nnombre = "Prueba"\n'
                    '[base_datos]\nruta = "prueba.sqlite3"\n'
                    f'[atencion]\ndias_anticipacion = {valor}\n', encoding="utf-8",
                )
                with self.assertRaises(ValueError):
                    cargar_configuracion(archivo)

    def test_explica_cuando_faltan_campos(self):
        with TemporaryDirectory() as temporal:
            archivo = Path(temporal) / "config.toml"
            archivo.write_text('[aplicacion]\nnombre = "Prueba"\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Faltan campos"):
                cargar_configuracion(archivo)
