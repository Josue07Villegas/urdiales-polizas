# Entregables y evidencia académica

Resumen de la guía Proyecto Integrador de Paradigmas v2 Lite proporcionada al equipo. Revisar las fechas oficiales y la rúbrica antes de cada entrega.

Los documentos editables organizados y sus versiones PDF se encuentran en [entregables/](entregables/LEEME.md). El [inventario](entregables/Inventario_Entregables.csv) distingue contenido preparado, validación pendiente y evidencia que depende del sistema terminado.

| Entrega | Contenido principal | Relación con este repositorio |
| --- | --- | --- |
| E1 · semana 1 · 5 % | Propuesta, consultora, empresa, problema, alcance, paradigmas y carta de validación | Propuesta integrada; firma de carta y visto bueno pendientes |
| E2 · semana 3 · 20 % | Componente 1: análisis, requerimientos, historias, UML y trazabilidad | Documento integrado; validar contenido, obtener firma y alinear con el código al implementar |
| E3 · semana 5 · 10 % | Demostración de al menos 60 % de requisitos Must | Esta estructura inicial todavía no alcanza ese avance |
| E4 · semana 6 · 65 % | Entrega formal y presentación | Código, informe, UML, manual, presentación y video por completar |

## Componente 1 y E2

- Guía de entrevista y minuta firmada o confirmada por correo.
- Actividades AS-IS y TO-BE.
- Al menos 10 RF y 5 RNF, numerados y priorizados con MoSCoW.
- Al menos 6 historias de usuario con criterios Dado/Cuando/Entonces.
- Casos de uso generales con include/extend y 3 casos detallados.
- Clases con atributos, métodos, visibilidad, multiplicidades, herencia y una clase abstracta.
- Al menos 2 secuencias y diagrama de componentes con paradigmas.
- Matriz RF → caso de uso → clases → archivos Python.

El diseño vigente conserva 11 RF y 5 RNF. La exportación a Excel y las funciones de respaldo y restauración de datos no son obligatorias en la guía y están excluidas del alcance. El video de respaldo de la demostración sí es obligatorio como parte del paquete final.

E2 integra seis historias actualizadas, tres casos detallados, cinco escenarios y las fuentes UML existentes. La evidencia firmada y la correspondencia con clases implementadas permanecen pendientes.

## Informe técnico final

La guía pide 15–25 páginas sin anexos, PDF, Arial o Calibri 12, interlineado 1.5, figuras numeradas y APA 7.

1. Portada y resumen ejecutivo de una página.
2. Introducción: empresa, problemática, objetivos y alcance.
3. Marco teórico de paradigmas y programación lógica; al menos 6 referencias, 2 académicas.
4. Análisis y diseño: integrar el Componente 1 de forma compacta.
5. Implementación: arquitectura y seis fichas de análisis de paradigmas.
6. Resultados: capturas del sistema, aceptación y retroalimentación de la empresa.
7. Conclusiones del equipo y conclusiones individuales de 150–250 palabras, escritas por cada integrante sin IA.
8. Referencias y anexos: carta, minutas, manual y bitácora de uso de IA.

Las fichas deben describir código existente y evidencia comprobable. No se acredita un paradigma por el nombre de una carpeta.

## Distribución propuesta de paradigmas

| Paradigma | Ubicación prevista | Estado |
| --- | --- | --- |
| Imperativo | `datos/carga_demo.py` | Carga y limpieza pendientes de conciliar |
| Estructurado | `aplicacion/servicios.py` e `interfaz/` | Arranque básico; casos de uso pendientes |
| Orientado a objetos | `dominio/` | Clases de negocio pendientes |
| Declarativo | `persistencia/esquema.sql` y repositorios | Esquema disponible; consultas de negocio pendientes de conectar |
| Funcional | `consultas/transformaciones.py` | Funciones puras y composición pendientes |
| Lógico | `reglas/atencion.py` | Motor y consultas lógicas pendientes |

La guía también contempla Python 3.11+, SQLite con consultas que incluyan JOIN y GROUP BY, configuración TOML y un conjunto de datos de demostración suficiente. Los requisitos completos deben comprobarse contra la guía original; este archivo es un resumen de trabajo.

## Paquete final

Entregar 24 horas antes de la presentación, según la guía:

- `PF_Equipo#_Informe.pdf`
- `PF_Equipo#_UML.zip`: imágenes y fuentes editables.
- `PF_Equipo#_Codigo.zip`: código, README y datos de ejemplo, sin entorno virtual. GitHub es complementario.
- `PF_Equipo#_Manual.pdf`
- `PF_Equipo#_Presentacion.pdf`
- `PF_Equipo#_Video.mp4`: máximo 5 minutos.

El día de la presentación: resumen ejecutivo impreso, acta de entrega/aceptación por duplicado y sistema instalado y probado con los datos de demostración. No incluir datos reales de clientes en el repositorio ni en el paquete de ejemplo.
