# Generación de los documentos

Los documentos de `docs/entregables/` organizan el avance conforme a la actividad. Los generadores utilizan Python con `python-docx`, Pillow y pypdf; son herramientas documentales y no dependencias de la aplicación.

1. Revisar `contenido.py`, `casos_uso.json` y los requisitos vigentes en `docs/diseno/`. Ajustar el contenido a los acuerdos confirmados.
2. Ejecutar `generar_entregables.py` con el entorno documental. Regenera nueve Word, el inventario, el índice y el paquete UML; conserva las copias originales cuando no está disponible la carpeta de trabajo externa.
3. Renderizar todos los Word modificados con el renderer documental y la opción de generar PDF. Revisar visualmente cada página y corregir antes de continuar. El Word y su PDF deben corresponder a la misma versión.
4. Ejecutar `consolidar_pdfs.py --render-dir RUTA_RENDER` con los PDF revisados. Puede repetirse el argumento: la última coincidencia tiene prioridad. El script copia los nueve PDF e integra seis anexos en el informe, con marcadores de navegación.
5. Comprobar que las firmas y resultados pendientes conserven su estado real y actualizar los documentos al cerrar el proyecto.

El informe actual tiene 21 páginas de cuerpo, una de índice de anexos y 35 de anexos. Su Word mantiene los anexos en archivos separados para facilitar la edición. Las fuentes originales no se reemplazan por los documentos consolidados.
