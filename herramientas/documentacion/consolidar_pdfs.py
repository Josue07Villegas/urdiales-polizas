"""Reúne PDF ya renderizados y revisados e integra los anexos del informe.

Este paso no sustituye la revisión visual de todas las páginas. Cuando se
repiten directorios, el último PDF disponible de cada documento tiene prioridad.
"""

import argparse
import json
import shutil
from pathlib import Path

from pypdf import PdfReader, PdfWriter


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'docs/entregables'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-dir', type=Path, action='append', required=True)
    args = parser.parse_args()
    documentos = json.loads((OUT / 'Documentos_Generados.json').read_text())
    fuentes = {}
    for relativo in documentos:
        docx = OUT / relativo
        candidatos = [d / docx.stem / (docx.stem + '.pdf') for d in args.render_dir]
        disponibles = [p for p in candidatos if p.is_file()]
        if not disponibles:
            raise SystemExit(f'Falta PDF revisado de {relativo}')
        fuente = disponibles[-1]
        if fuente.stat().st_mtime < docx.stat().st_mtime:
            raise SystemExit(f'El PDF es anterior al Word de {relativo}; volver a renderizar')
        fuentes[relativo] = fuente

    # Comprobar todas las entradas antes de modificar la carpeta de entrega.
    anexos = [
        ('Anexo A Análisis y diseño', 'E2/E2_AlfaConsultora_Analisis_Diseno.pdf'),
        ('Anexo B Guion de entrevista', 'Anexos/Guion_Entrevista_Validacion.pdf'),
        ('Anexo C Minuta', 'Anexos/Minuta_Primera_Sesion_Urdiales_Alcance_Acotado.pdf'),
        ('Anexo D Carta de validación', 'Anexos/Carta_Membretada_Validacion_Alcance_Urdiales.pdf'),
        ('Anexo E Manual inicial', 'E4/PF_AlfaConsultora_Manual.pdf'),
        ('Anexo F Bitácora de IA', 'Anexos/Bitacora_Uso_IA.pdf'),
    ]
    generados = {Path(r).with_suffix('.pdf').as_posix() for r in documentos}
    for _, relativo in anexos:
        if relativo not in generados and not (OUT / relativo).is_file():
            raise SystemExit(f'Falta anexo {relativo}')
    paginas = {}
    for relativo, fuente in fuentes.items():
        destino = (OUT / relativo).with_suffix('.pdf')
        shutil.copy2(fuente, destino)
        paginas[destino.relative_to(OUT).as_posix()] = len(PdfReader(destino).pages)

    informe = OUT / 'E4/PF_AlfaConsultora_Informe.pdf'
    escritor = PdfWriter()
    escritor.append(informe, outline_item='Informe técnico e índice de anexos')
    for titulo, relativo in anexos:
        escritor.append(OUT / relativo, outline_item=titulo)
    escritor.add_metadata({'/Title': 'Informe técnico de Alfa Consultora para Urdiales Asesores',
                           '/Author': 'Alfa Consultora'})
    total = len(escritor.pages)
    temporal = informe.with_suffix('.tmp.pdf')
    with temporal.open('wb') as archivo:
        escritor.write(archivo)
    escritor.close()
    temporal.replace(informe)
    paginas['E4/PF_AlfaConsultora_Informe.pdf'] = total
    print(json.dumps(paginas, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
