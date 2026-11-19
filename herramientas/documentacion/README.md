# Documentación de la solución

La entrada vigente es `generar_informe_unico.py`. Produce un informe técnico completo, con todos los anexos dentro del Word, y un manual independiente en `docs/entrega_final/`. E1–E4 son etapas para organizar avances; no generan informes finales independientes. El video fue cancelado por indicación del equipo el 19/11/2026.

## Actualización

1. Ajustar `contenido.py`, `casos_uso.json`, el catálogo y la matriz de `docs/diseno/` a los acuerdos confirmados. El catálogo contiene ocho RF Must, tres Should, una mejora Could y seis exclusiones Won’t como propuesta para validación.
2. Ejecutar `generar_informe_unico.py` con el entorno documental de Python que incluya python-docx y Pillow. `generar_entregables.py` redirige a la misma entrada y conserva componentes de formato y contenido reutilizables.
3. Renderizar los dos Word con la herramienta documental y generar sus PDF. Inspeccionar visualmente todas las páginas y corregir cualquier defecto. El informe debe mantener de 15 a 25 páginas de cuerpo, antes de los anexos.
4. Ejecutar `consolidar_pdfs.py --render-dir RUTA_RENDER` con pypdf disponible. Copia los PDF revisados sin concatenar informes ni añadir anexos externos. Se puede repetir el argumento para dar prioridad a un render posterior; cada directorio debe contener una sola coincidencia por nombre de PDF.
5. Revisar el inventario, las firmas, las capturas y los resultados antes de preparar el paquete de cinco elementos. El generador no crea una presentación ni un sistema terminado.

La fuente del informe y la del manual corresponden al mismo contenido en Word y PDF. La organización documental del 17/11/2026 y los originales se conservan en `docs/historial/2026-11-17_entregables/`. No utilizar sus prioridades antiguas como versión vigente.
