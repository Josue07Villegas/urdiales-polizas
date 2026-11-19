# Entrega final y organización del trabajo

La entrega se compone de **cinco elementos**: informe técnico, presentación, diagramas, código y manual de usuario. El video quedó cancelado por indicación del equipo el 19 de noviembre de 2026. Esta aclaración actualiza la lista de la guía original.

El [informe técnico único](entrega_final/PF_AlfaConsultora_Informe.docx) concentra contexto, problema, objetivos, alcance, teoría, análisis, diseño, implementación, resultados y conclusiones. Dentro del mismo Word se integran los anexos con reglas, datos, historias completas, casos de uso, aceptación, entrevista, minuta, carta y bitácora de IA. El PDF contiene ese mismo informe; no se agrega E2 como documento independiente.

| Elemento | Contenido y estado |
| --- | --- |
| Informe técnico | Documento integrado; implementación completa, capturas, firmas, aceptación y conclusiones individuales pendientes |
| Presentación | Máximo 15 diapositivas; guion en el Anexo I del informe, diapositivas pendientes |
| Diagramas | Imágenes en el informe y fuentes editables en el paquete UML |
| Código | Repositorio con infraestructura ejecutable; faltan casos completos y al menos 300 registros realistas |
| Manual de usuario | Documento independiente de tres páginas; procedimientos completos y capturas pendientes |

## Etapas internas

E1–E4 sirven como referencias de avance y reparto de responsabilidades. El equipo Alfa Consultora participa de forma conjunta. Los documentos separados del 17 de noviembre se guardaron como [historial](historial/2026-11-17_entregables/ESTADO_HISTORICO.txt); no son informes finales adicionales.

## Requerimientos y prioridades

El [catálogo vigente](diseno/Requerimientos_Diseno.json) mantiene RF-01 a RF-11. La priorización propuesta incluye ocho Must y tres Should. OP-01 Could permite colores por aseguradora con texto, como apoyo opcional ya mencionado en el levantamiento. EX-01 a EX-06 Won’t registran funciones fuera de esta versión. Los cinco RNF siguen siendo Must.

Should no elimina un acuerdo de alcance: se propone atender primero el núcleo y revisar la secuencia con la empresa. Las exclusiones no cuentan como RF comprometidos. La exportación y las funciones de respaldo y restauración de datos permanecen excluidas. No se reintroduce RF-12.

## Condiciones académicas que siguen vigentes

- Informe de 15–25 páginas sin anexos, Arial o Calibri 12, interlineado 1.5, figuras numeradas y APA 7.
- Al menos 10 RF, 5 RNF, 6 historias con criterios Dado/Cuando/Entonces, 3 CU detallados, UML y matriz RF → CU → clases → archivo Python.
- Seis fichas de paradigma con código real y observaciones verificadas; mínimo 6 referencias, incluidas 2 académicas.
- Conclusiones individuales de 150–250 palabras, redactadas por cada integrante sin IA.
- Python 3.11+, SQLite con JOIN/GROUP BY, TOML y datos realistas de demostración.
- Carga/limpieza de datos, tres indicadores y módulo lógico pendientes de conciliar con el alcance comercial. No se presume una excepción aprobada.

Consultar el [índice vigente](entrega_final/LEEME.md) y el [inventario](entrega_final/Inventario_Entrega.csv). El acta y el resumen ejecutivo son material de apoyo dentro del informe. La presentación y la validación empresarial se completan con el sistema funcionando.
