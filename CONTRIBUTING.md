# Trabajo del equipo

## Antes de programar

1. Revisa el [alcance](docs/alcance.md), los [pendientes](docs/pendientes.md) y la matriz de trazabilidad.
2. Elige una tarea pequeña vinculada a un requerimiento o a infraestructura necesaria.
3. Acuerda con el equipo si cambia una regla pendiente de validar.
4. Crea una rama descriptiva, por ejemplo `feat/registro-asegurados` o `docs/historias-usuario`.

No se han asignado módulos ni roles individuales en este repositorio.

## Commits atómicos en español

Cada commit debe contener una intención concreta que se pueda revisar y revertir. Incluye el código y las pruebas necesarias para ese cambio. Evita juntar una función nueva con una reorganización ajena.

Formato sugerido:

```text
tipo: describir el cambio con un verbo en infinitivo
```

Tipos: `feat`, `fix`, `docs`, `test`, `refactor`, `chore` y `ci`.

Ejemplos:

```text
feat: registrar asegurados con contactos opcionales
fix: conservar la vigencia anterior al fallar una renovación
docs: precisar los filtros acordados con la empresa
test: comprobar el histórico de pólizas vencidas
```

Usa el cuerpo del commit para explicar una decisión cuando el título no baste. Evita mensajes como `cambios`, `avance` o `final`.

Antes de confirmar:

```bash
git diff
git add ruta/del/archivo.py tests/test_del_cambio.py
git diff --cached
git commit -m "feat: describir el cambio concreto"
```

## Comprobaciones

Ejecuta desde la raíz:

```bash
python3 main.py --comprobar
python3 -m unittest discover -s tests -t . -v
git diff --check
```

Para cambios de interfaz, abre la ventana y comprueba lo que cambió. Para nuevas reglas o persistencia, prueba el comportamiento y sus errores relevantes con datos sintéticos.

## Mantener diseño y código alineados

- Actualiza la matriz RF → caso de uso → clase → archivo cuando implementes una función.
- Actualiza el UML editable y su imagen al cambiar relaciones, clases o contratos.
- Conserva los números de póliza y teléfonos como texto y usa parámetros SQL.
- Resuelve el reloj y las fechas mediante valores explícitos en las pruebas para evitar que cambien con el día de ejecución.
- No marques como validada una decisión sin evidencia de la empresa o del docente.
- Documenta el uso de IA requerido por la guía; cada integrante escribe su conclusión individual por su cuenta.

## Revisión y datos

Comparte una solicitud de cambios pequeña con el problema, el comportamiento resultante, las pruebas realizadas y las decisiones pendientes. Revisa los archivos preparados para el commit y evita datos reales de clientes, bases locales, credenciales, minutas firmadas y documentos sensibles.
