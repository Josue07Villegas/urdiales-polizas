# Análisis y diseño propuestos

Versión de trabajo del 17 de noviembre de 2026. Estos diseños son una base para E2 y para el capítulo 3 del informe técnico. No acreditan validación ni firma de la empresa.

- [Documento de diseños en Word](Disenos_Urdiales_v1.docx).
- [Requerimientos propuestos RF-01 a RF-11](Requerimientos_Diseno.json).
- [Matriz de trazabilidad propuesta](Matriz_Trazabilidad.csv).
- [Fuentes editables de los diagramas](uml/).
- [Imágenes PNG y SVG](imagenes/).
- [Consultas SQL propuestas](consultas_propuestas.sql).
- [Esquema SQL utilizado por la base inicial](../../src/urdiales_polizas/persistencia/esquema.sql).

## Cómo interpretar los archivos

Los nombres de módulos en los diagramas y la matriz se resuelven dentro de `src/urdiales_polizas/`. Que un módulo exista como archivo no significa que su caso de uso esté implementado.

Se retiró RF-12 de exportación a Excel. La exportación y las funciones de respaldo y restauración quedan fuera del alcance; permanecen 11 RF y 5 RNF, suficientes para el mínimo de la actividad.

Las fuentes DOT se pueden editar con Graphviz; las secuencias incluyen fuentes PlantUML y SVG editables. Las imágenes y el documento Word corresponden al diseño previo a la implementación. Deben actualizarse cuando se validen o cambien las clases, contratos o relaciones.

La base local aplica el esquema propuesto, incluidas restricciones de integridad. Su presencia en SQL no sustituye la validación de los supuestos del negocio ni las pruebas de aceptación de la aplicación.

## Inventario

| Archivo | Contenido |
| --- | --- |
| `01_actividad_actual` | Proceso actual con Excel y calendario |
| `02_actividad_propuesta` | Proceso propuesto de registro y consulta |
| `03_casos_uso` | Casos de uso generales |
| `04_clases_polizas` | Pólizas, herencia y vigencias |
| `05_clases_detalle` | Contactos, vehículos y cobros |
| `06_modelo_relacional` | Ocho tablas SQLite |
| `07_secuencia_consulta` | Consulta de cartera con filtros |
| `08_secuencia_renovacion` | Nueva vigencia y conservación de la anterior |
| `09_componentes` | Componentes y paradigmas propuestos |
| `10_boceto_cartera` | Boceto de la futura consulta; distinto de la ventana inicial actual |

Consulta los [pendientes de validación](../pendientes.md) antes de convertir una propuesta en comportamiento definitivo.
