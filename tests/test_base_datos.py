from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from urdiales_polizas.persistencia.base_datos import (
    abrir_conexion, comprobar_esquema, inicializar_bd,
)


class BaseDatosTest(unittest.TestCase):
    def test_el_esquema_se_puede_crear_en_memoria(self):
        self.assertEqual(comprobar_esquema(), 8)

    def test_reinicializar_conserva_los_registros(self):
        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "datos/base.sqlite3"
            self.assertTrue(inicializar_bd(ruta))
            conexion = abrir_conexion(ruta)
            try:
                conexion.execute("INSERT INTO asegurados(nombre) VALUES (?)", ("Cliente ficticio",))
                conexion.commit()
            finally:
                conexion.close()
            self.assertFalse(inicializar_bd(ruta))
            conexion = abrir_conexion(ruta)
            try:
                self.assertEqual(conexion.execute(
                    "SELECT nombre FROM asegurados"
                ).fetchone()[0], "Cliente ficticio")
            finally:
                conexion.close()

    def test_rechaza_otra_base_sin_modificarla(self):
        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "otra.sqlite3"
            with sqlite3.connect(ruta) as conexion:
                conexion.execute("CREATE TABLE externa (id INTEGER)")
                conexion.execute("INSERT INTO externa VALUES (7)")
            with self.assertRaisesRegex(ValueError, "otro esquema"):
                inicializar_bd(ruta)
            with sqlite3.connect(ruta) as conexion:
                self.assertEqual(conexion.execute("SELECT id FROM externa").fetchone()[0], 7)
                self.assertEqual(conexion.execute(
                    "SELECT count(*) FROM sqlite_master WHERE type='table'"
                ).fetchone()[0], 1)

    def test_las_conexiones_rechazan_relaciones_inexistentes(self):
        with TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "prueba.sqlite3"
            inicializar_bd(ruta)
            conexion = abrir_conexion(ruta)
            try:
                with self.assertRaises(sqlite3.IntegrityError):
                    conexion.execute(
                        "INSERT INTO cobros(vigencia_id, fecha_vencimiento) VALUES (?, ?)",
                        (999, "2026-12-20"),
                    )
            finally:
                conexion.rollback()
                conexion.close()
