# Decisiones y trabajo pendientes

## Decisiones de alcance

La exportación a Excel y las funciones de respaldo y restauración quedan excluidas de esta entrega. Se retira RF-12 y se conservan RF-01 a RF-11; la actividad pide al menos 10 RF y 5 RNF. No se necesita agregar una función para sustituir la exportación.

## Confirmar con la empresa

| Tema | Qué falta acordar |
| --- | --- |
| Anticipación | A qué pólizas y cobros aplica el plazo de 30 días |
| Días inhábiles | Calendario y ajuste de la fecha de atención, conservando la contractual |
| Contactos y referentes | Relación, datos opcionales y medios que se necesitan consultar |
| Flotillas | Datos compartidos de la matriz y datos específicos por inciso |
| Canceladas | Ubicación en las consultas y confirmación de que no se reactivan |
| Histórico | Quién puede editarlo y qué datos deben conservarse |
| Aseguradoras | Catálogo y nombres correctos antes de preparar la demostración |

El esquema incluye decisiones de diseño propuestas. No se presentan como una aprobación firmada de la empresa.

## Conciliar con el docente

- Carga y limpieza CSV/Excel exigidas académicamente frente a la exclusión comercial de importación.
- Al menos tres reportes o indicadores útiles exigidos por la guía frente a la exclusión de reportes comerciales. Una consulta técnica `GROUP BY` no acredita por sí sola ese requisito.
- Biblioteca y evidencia para programación lógica con `kanren` o `sympy`, según la guía. Todavía no se eligió ni instaló una dependencia.
- Construcción del conjunto de al menos 300 registros realistas de demostración, con las condiciones de la guía.

## Orden propuesto de desarrollo

1. Validar E2: requerimientos, historias de usuario, diagramas y trazabilidad.
2. Implementar entidades, contactos y repositorios con altas y edición.
3. Implementar pólizas de autos y daños y sus vigencias.
4. Conectar cartera, filtros combinables y orden por proximidad.
5. Implementar histórico y renovación con una transacción y pruebas de reversión.
6. Incorporar cobros y atención por fechas con reglas validadas.
7. Preparar datos sintéticos y evidencias de los seis paradigmas.
8. Completar pruebas de aceptación, manual, informe y demostración.

No asignar como terminado un requisito porque tenga una carpeta o un archivo reservado.
