"""Copia los PDF revisados del informe autocontenido y del manual.

Este paso no sustituye la revisión visual de todas las páginas. Cuando se
repiten directorios, el último PDF disponible de cada documento tiene prioridad.
"""

import argparse
import json
import shutil
from pathlib import Path

from pypdf import PdfReader

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'docs/entrega_final'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-dir', type=Path, action='append', required=True)
    args = parser.parse_args()
    documentos = json.loads((OUT / 'Documentos_Generados.json').read_text())
    fuentes = {}
    for relativo in documentos:
        docx = OUT / relativo
        disponibles = []
        for directorio in args.render_dir:
            candidatos = list(directorio.rglob(docx.stem + '.pdf'))
            if len(candidatos) > 1:
                raise SystemExit(f'Hay varios PDF de {docx.stem} en {directorio}; indicar un directorio más específico')
            disponibles.extend(candidatos)
        if not disponibles:
            raise SystemExit(f'Falta PDF revisado de {relativo}')
        fuente = disponibles[-1]
        if fuente.stat().st_mtime < docx.stat().st_mtime:
            raise SystemExit(f'El PDF es anterior al Word de {relativo}; volver a renderizar')
        fuentes[relativo] = fuente
    paginas = {}
    for relativo, fuente in fuentes.items():
        destino = (OUT / relativo).with_suffix('.pdf')
        shutil.copy2(fuente, destino)
        paginas[destino.name] = len(PdfReader(destino).pages)
    print(json.dumps(paginas, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
