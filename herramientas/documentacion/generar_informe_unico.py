"""Genera el informe autocontenido y el manual independiente de la solución."""

from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import csv
import json

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph
from PIL import Image

import generar_entregables as base
from contenido import *

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / 'docs/entrega_final'
HISTORIAL = REPO / 'docs/historial/2026-11-17_entregables'
CATALOGO = json.loads((REPO / 'docs/diseno/Requerimientos_Diseno.json').read_text())
base.OUT = OUT


class Informe(base.Doc):
    def __init__(self):
        super().__init__('Informe técnico del registro de clientes y pólizas', 'E4 Informe', final=True)
        self.d.sections[0].footer.paragraphs[0].runs[0].text = 'Alfa Consultora | Informe técnico | '
        self.figura = 0

    def p(self,t='',bold=False,size=None,after=6):
        parrafo=super().p(t,bold,size,after)
        if not self.final:parrafo.paragraph_format.line_spacing=1.1
        return parrafo

    def picture(self, stem, caption, land=False):
        self.figura += 1
        path = base.IMG / (stem + '.png')
        w, h = Image.open(path).size
        factor = min((9.3 if land else 6.9)/w, (5.0 if land else 8.2)/h)
        p = self.d.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(3)
        p.add_run().add_picture(str(path), width=Inches(w*factor), height=Inches(h*factor))
        self.p(f'Figura {self.figura}. {caption}. Fuente: elaboración de Alfa Consultora.', size=10)

    def compact(self):
        self.final = False
        for nombre in ('Normal', 'Title', 'Heading 1', 'Heading 2'):
            self.d.styles[nombre].paragraph_format.line_spacing = 1.5


def portada(x):
    base.cabecera(x)
    x.p('Todos los integrantes participan de forma conjunta.')
    x.table(['Integrante', 'Matrícula'], EQUIPO, [5.9, 1.1])
    x.p('Aplicación local para centralizar y consultar clientes, pólizas y vigencias de Urdiales Asesores.')
    x.p('Este informe reúne contexto, requerimientos, análisis, diseños, arquitectura, resultados disponibles y anexos. La implementación y la aceptación final continúan en desarrollo.')
    x.p('Contenido: resumen ejecutivo; introducción; marco teórico; análisis y diseño; implementación y seis fichas de paradigmas; resultados; conclusiones; referencias; anexos A a I.', size=11)


def requisitos(x):
    x.table(['ID', 'Requerimiento funcional', 'Prioridad'],
            [(r['id'], r['descripcion'], r['prioridad']) for r in CATALOGO['requerimientos']],
            [.7, 5.3, 1.0])
    x.p('Priorización propuesta: ocho Must y tres Should. Se conservan los once RF; Should define una prioridad de implementación y no elimina una función acordada con la empresa.', size=11)


def moscow(x):
    x.p('Las prioridades distinguen el núcleo necesario, las funciones importantes, las mejoras opcionales y las exclusiones de esta versión. Se propone su revisión con la empresa antes de comprometer fechas (Agile Business Consortium, 2026).')
    x.table(['Nivel', 'Aplicación en esta versión'], [
        ('M · Must', 'RF-01, 02, 04, 05, 06, 07, 08 y 10: registro, edición, relaciones, cartera, filtros, histórico y atención por fechas.'),
        ('S · Should', 'RF-03: varios contactos; RF-09: estados de cobro; RF-11: cancelación administrativa. Son importantes y se prevén en el proyecto; su secuencia se revisa sin perder los controles existentes.'),
        ('C · Could', 'OP-01: colores por aseguradora acompañados de su nombre. Es un apoyo visual opcional; los nombres y filtros permiten consultar sin él.'),
        ('W · Won’t', 'EX-01 a EX-06: cotizaciones; comunicaciones y campañas; reportes comerciales, tableros y gráficas; importación de Excel desde la interfaz; exportación a Excel; respaldo y restauración de datos.'),
    ], [1.15, 5.85])
    x.p('No se exige el mismo número de elementos por categoría. Los cinco RNF siguen siendo Must por integridad, persistencia, uso, instalación y manejo de datos. Las exclusiones W no cuentan como RF comprometidos ni OP-01 sustituye uno de los once RF.')


def marco_referencias(x):
    referencias = [
        ('Agile Business Consortium. (2026, 28 de mayo). ', 'What is MoSCoW prioritization?', ' https://www.agilebusiness.org/resource/what-is-moscow-prioritization/'),
    ]
    titulos = ['Information Processing 74', 'abc — Abstract base classes', 'dataclasses — Data classes',
               'sqlite3 — DB-API 2.0 interface for SQLite databases', 'tomllib — Parse TOML files',
               'New computational paradigms for computer music']
    for (texto, url), titulo in zip(REFERENCIAS, titulos):
        antes, despues = texto.split(titulo, 1)
        referencias.append((antes, titulo, despues+' '+url))
    for antes, titulo, despues in referencias:
        p=x.p(antes)
        p.add_run(titulo).italic=True
        p.add_run(despues)
        p.paragraph_format.left_indent=Inches(.3)
        p.paragraph_format.first_line_indent=Inches(-.3)
    x.p('Proyecto integrador final versión 2 Lite. (s. f.). Material de la asignatura Paradigmas de Programación proporcionado al equipo.')


def informe():
    x=Informe()
    portada(x)
    x.page('Resumen ejecutivo');base.resumen_texto(x)
    x.page('1 Introducción')
    x.h('Contexto de la empresa');x.p(CONTEXTO)
    x.h('Planteamiento del problema');x.p(PROBLEMA)
    x.h('Objetivo general');x.p(OBJETIVO)
    x.h('Objetivos específicos')
    for t in OBJETIVOS:x.li(t)
    x.page('1 1 Alcance y delimitación')
    x.h('Funciones previstas');x.p(ALCANCE)
    x.h('Límites de esta versión');x.p(EXCLUSIONES)
    x.h('Condiciones académicas');x.p(ACLARACION)
    x.p('Los cinco elementos de la entrega son informe técnico, presentación, diagramas, código y manual de usuario. El video quedó cancelado por indicación del equipo el 19 de noviembre de 2026. Las etapas de avance sirven para organizar el trabajo; su contenido documental se integra en este informe.',size=11)
    x.page('2 Marco teórico de paradigmas');base.marco(x)
    x.page('2 1 Persistencia transformaciones y lógica');base.marco(x,True)
    x.page('3 Análisis y diseño')
    x.h('Levantamiento')
    x.p('La primera sesión se realizó el 5 de noviembre de 2026 a las 16:00 h en Monterrey, Nuevo León. Asistieron José Urdiales Pérez y Aurora por la empresa, y Scarlett Alvarado Urdiales, Josue Abel Villegas Garcia y David Alejandro Carrillo Cázares por Alfa Consultora. El equipo completo participa en el proyecto; la asistencia de esta sesión se registra por separado.')
    x.h('Proceso actual y proceso propuesto');x.p(MARCAS)
    x.p('Actualmente se registra la emisión en Excel, se trasladan fechas a Google Calendar y se buscan los datos para renovar o cobrar. El proceso propuesto consulta registros centralizados, combina filtros, deriva las fechas de atención y valida los cambios. Al renovar conserva el periodo anterior. Los diagramas de actividad completos están dentro del Anexo A.')
    x.h('Organización de la información')
    x.p('El modelo distingue asegurado, contacto, aseguradora, póliza, vigencia, vehículo y cobro. Autos y daños comparten datos generales; los datos de vehículo corresponden a autos y cada inciso de flotilla conserva su identificación. Números de póliza, series y teléfonos son texto. Reglas, diccionario y decisiones pendientes se incluyen en los anexos B y E.')
    x.page('3 1 Requerimientos funcionales');requisitos(x)
    x.page('3 2 Priorización MoSCoW');moscow(x)
    x.page('3 3 Requerimientos no funcionales')
    x.table(['ID', 'Condición verificable'], [(a+' '+c,d) for a,b,c,d in RNF], [1.1,5.9])
    x.p('Todos los RNF tienen prioridad Must. La persistencia se verifica cerrando y reabriendo registros confirmados; no implica una función de respaldo. La integridad se comprueba con fechas, campos y relaciones inválidas y con la reversión de cambios parciales.')
    x.page('3 4 Historias de usuario')
    x.table(['Historia','Necesidad y RF'],[(h[0],h[1]+'\n'+h[2]) for h in HISTORIAS],[.9,6.1])
    x.p('Los doce criterios Dado/Cuando/Entonces, dos por historia, se desarrollan en el Anexo C de este mismo informe.',size=11)
    x.page('3 5 Casos de uso del sistema',land=True)
    x.picture('03_casos_uso','Casos de uso generales con relaciones include y extend',True)
    x.p('CU-02, CU-03 y CU-06 se detallan en el Anexo D. Incluyen flujos básicos, alternos, excepciones y postcondiciones; son especificaciones propuestas.',size=11)
    x.page('3 6 Clases del dominio',land=True)
    x.picture('04_clases_polizas','Clases de pólizas con herencia abstracción y multiplicidades',True)
    x.p('La clase abstracta Poliza se especializa en autos y daños. La vigencia conserva el número y el periodo. Contactos, cobros y vehículos, modelo relacional, secuencias y componentes se muestran en el Anexo A.',size=11)
    x.page('3 7 Matriz de trazabilidad',land=True)
    x.final=False
    base.matriz(x)
    x.final=True
    x.p('OP-01 es opcional y se vincula a la consulta RF-06 y a RNF-03. Los elementos W no generan clases ni módulos comprometidos.',size=10.5)
    x.page('4 Implementación y arquitectura')
    x.p('La versión 0.1.0 prepara una aplicación local con Python, SQLite y configuración TOML. La interfaz inicial usa Tkinter. El código disponible valida la configuración, comprueba el SQL en memoria e inicializa una base vacía. La ventana tiene pestañas informativas; los casos de captura y consulta operativa siguen pendientes.')
    x.table(['Capa','Responsabilidad y estado'],[
        ('Interfaz y aplicación','Arranque disponible; formularios y coordinación de los casos de negocio pendientes.'),
        ('Dominio','Clases de negocio, herencia y llamadas polimórficas pendientes.'),
        ('Persistencia','Conexión e inicialización del esquema disponibles; repositorios y consultas de negocio por implementar.'),
        ('Consultas y reglas','Espacios reservados; faltan funciones puras y motor lógico.'),
    ],[1.3,5.7])
    x.p('El Anexo A contiene los componentes propuestos y sus paradigmas. Las seis fichas siguientes registran evidencia disponible y trabajo pendiente; un archivo reservado no acredita la implementación de un paradigma.')
    for i in range(6):base.ficha(x,i)
    x.page('5 Resultados y aceptación')
    x.p('La verificación de infraestructura del 17 de noviembre de 2026 aprobó nueve pruebas de configuración, esquema y arranque, y confirmó ocho tablas en memoria. No se presentan como aceptación de los requerimientos de negocio ni como una validación firmada por la empresa.')
    x.table(['Escenario','Criterio de aceptación','Resultado'],[(s[0],s[1],'No ejecutado') for s in ESCENARIOS],[1.1,3.9,2.0])
    x.p('Los datos, acciones y resultados esperados están en el Anexo E. Falta implementar los casos, preparar al menos 300 registros realistas de muestra, obtener capturas, ejecutar la aceptación y recoger la retroalimentación de Aurora y José. El boceto del Anexo A es un diseño y no una captura del sistema funcionando.')
    x.page('6 Conclusiones')
    x.h('Conclusión del equipo sobre el avance')
    x.p('El levantamiento delimitó una necesidad de almacenamiento y consulta centralizada. Se organizaron las relaciones entre clientes, pólizas y vigencias, y se documentaron reglas y criterios de aceptación. La infraestructura comprueba configuración y esquema; todavía no permite evaluar beneficios operativos. La siguiente etapa consiste en validar los puntos abiertos e implementar registro, consulta, filtros e histórico antes de ejecutar la aceptación.')
    x.h('Conclusiones individuales')
    x.p('Cada integrante redacta de 150 a 250 palabras sin IA, conforme a la actividad. Los siguientes espacios se completan personalmente.')
    for n,m in EQUIPO:x.p(n+' — redacción personal pendiente.')
    x.h('Trabajo futuro')
    x.p('Completar los módulos, revisar la priorización propuesta, conciliar carga e indicadores académicos, preparar datos sintéticos y actualizar manual, fichas, capturas y resultados. Las exclusiones W se mantienen fuera de esta versión.')
    x.page('Referencias');marco_referencias(x)
    anexos(x)
    x.save(Path('PF_AlfaConsultora_Informe.docx'))


def anexos(x):
    x.compact()
    x.page('Anexos del informe técnico')
    x.p('Los anexos forman parte de este mismo archivo editable y de su PDF. Amplían la especificación del cuerpo principal y reúnen los formatos de evidencia y validación.')
    x.table(['Anexo','Contenido'],[
        ('A','Diagramas complementarios del proceso, datos, clases, secuencias, componentes y boceto.'),
        ('B','Reglas de negocio, consultas lógicas y diccionario de datos.'),
        ('C','Seis historias con dos criterios de aceptación cada una.'),
        ('D','Tres casos de uso detallados.'),
        ('E','Escenarios de aceptación y definiciones pendientes.'),
        ('F','Guion de entrevista y validación.'),
        ('G','Minuta de la primera sesión y carta de validación por revisar y firmar.'),
        ('H','Bitácora de uso de IA.'),
        ('I','Preparación de la presentación y acta de entrega de los cinco elementos.'),
    ],[.7,6.3],size=11)
    x.p('El manual de usuario se entrega como documento independiente. Las fuentes editables de los diagramas también se conservan en su paquete; no se requiere abrir otro informe para leer el análisis y diseño.')
    complementos=[d for d in DIAGRAMAS if d[0] not in ('03_casos_uso','04_clases_polizas')]
    for stem,titulo,land in complementos:
        x.page('Anexo A '+titulo,land)
        x.picture(stem,titulo,land)
    x.page('Anexo B Reglas de negocio')
    for codigo,t in REGLAS:x.h2(codigo);x.p(t,size=11)
    x.p('La renovación anual y la periodicidad del pago son conceptos separados. Vencimiento y cancelación no son equivalentes. Un ajuste por día inhábil debe conservar la fecha contractual.',size=11)
    x.h2('Reglas propuestas para consultas lógicas')
    for codigo,t in REGLAS_LOGICAS:x.p(codigo+' '+t,size=10.5,after=4)
    x.page('Anexo B Diccionario de datos')
    x.table(['Grupo','Datos identificados','Tratamiento'],DATOS,[1.0,2.8,3.2],size=10.5)
    for numero,bloque in enumerate((HISTORIAS[:3],HISTORIAS[3:]),1):
        x.page('Anexo C Historias y criterios '+str(numero))
        base.historias(x,bloque)
    for c in base.CASOS:
        x.page('Anexo D '+c[0]);base.caso(x,c)
    x.page('Anexo E Escenarios de aceptación')
    x.p('Los cinco escenarios de negocio están pendientes de ejecución en la aplicación. Se prueban con datos ficticios y una fecha de referencia explícita.',bold=True,size=11)
    for s in ESCENARIOS[:3]:escenario(x,s)
    x.page('Anexo E Edición y persistencia')
    for s in ESCENARIOS[3:]:escenario(x,s)
    x.h2('Registro de ejecución')
    x.table(['Escenario','Resultado observado','Validó y fecha'],[(s[0],'Pendiente de ejecutar','Por registrar') for s in ESCENARIOS],[1.0,3.8,2.2],size=10.5)
    x.page('Anexo E Definiciones pendientes')
    x.table(['ID','Responsables de revisión','Definición pendiente'],PENDIENTES,[.7,1.5,4.8],size=10.5)
    x.p('Revisó por la empresa: ____________________ Fecha: ____________________',size=11)
    x.p('Revisó por Alfa Consultora: ________________ Fecha: ____________________',size=11)
    entrevista(x)
    incorporar_formato(x,HISTORIAL/'Anexos/Minuta_Primera_Sesion_Urdiales_Alcance_Acotado.docx','Anexo G ')
    incorporar_formato(x,HISTORIAL/'Anexos/Carta_Membretada_Validacion_Alcance_Urdiales.docx','Anexo G ')
    bitacora(x)
    presentacion(x)
    acta(x)


def escenario(x,s):
    codigo,titulo,rel,datos,accion,esperado=s
    x.h2(codigo+' '+titulo);x.p('Relación: '+rel,size=10.5)
    x.p('Dado '+datos+' Cuando '+accion+' Entonces '+esperado,size=11)


def entrevista(x):
    x.page('Anexo F Guion de entrevista y validación')
    x.p('Las respuestas recabadas están en la minuta y en las especificaciones del informe. Este guion sirve para cerrar las definiciones abiertas; no acredita respuestas aún no confirmadas.',size=11)
    preguntas=[
        '¿Dónde registran asegurados y pólizas después de emitirlas y quién mantiene los datos?',
        '¿Qué dificultad concreta encuentran al buscar por asegurado, compañía y fechas? Medir un ejemplo real.',
        '¿Qué datos comparten autos y daños y cuáles son específicos de cada tipo?',
        '¿Qué contactos, teléfonos, correos y datos del referente deben conservar y cómo se relacionan?',
        'En una flotilla, ¿qué comparte la matriz y qué pertenece a cada inciso?',
        '¿Qué cambia al renovar: número de póliza, vigencia, riesgos y forma de pago?',
        '¿Qué combinaciones de asegurado, aseguradora, fechas y cobranza o renovación necesitan consultar?',
        '¿A qué casos aplican los 30 días de anticipación y qué calendario inhábil se usa?',
        '¿Qué información debe conservarse en el histórico y quién puede corregirla?',
        '¿En qué casos se cancela una póliza y cómo debe aplicarse la restricción de reactivación?',
        '¿Qué datos se capturan para cada cobro y cómo se confirma su estado?',
        '¿En qué equipo y sistema operativo se instalará la solución y quién la utilizará?',
        '¿Los datos sintéticos y los cinco escenarios representan sus casos habituales?',
        '¿Se confirma el alcance y la prioridad propuesta, manteniendo exportación y respaldos fuera de esta versión?',
        '¿Qué observaciones tienen sobre la minuta y la carta y cuándo se realizará la validación?',
    ]
    for i,t in enumerate(preguntas,1):x.p(str(i)+'. '+t,size=11,after=4)
    x.p('Fecha y participantes: ______________________________________________',size=11)
    x.p('Acuerdos y pendientes: ______________________________________________\n_________________________________________________________________',size=11)


def incorporar_formato(x,path,prefijo):
    """Reproduce el texto y las tablas en orden, conservando las fuentes intactas."""
    d=Document(path)
    iniciado=False
    for el in d.element.body:
        if el.tag==qn('w:p'):
            texto=Paragraph(el,d).text
            if not texto.strip():continue
            style=el.find('w:pPr/w:pStyle',el.nsmap)
            nombre=style.get(qn('w:val')) if style is not None else ''
            if nombre=='Title':
                x.page(prefijo+texto);iniciado=True
            elif not iniciado:
                # La carta tiene el membrete antes del título.
                if not hasattr(x,'_cabecera_carta'):x._cabecera_carta=[]
                x._cabecera_carta.append(texto)
            elif nombre.startswith('Heading'):
                x.h2(texto)
            else:
                p=x.p(texto,size=11,after=4)
                if '\t' in texto:p.paragraph_format.tab_stops.add_tab_stop(Inches(3.6))
            if iniciado and getattr(x,'_cabecera_carta',None):
                for t in x._cabecera_carta:x.p(t,bold=t=='URDIALES ASESORES',size=11,after=4)
                x._cabecera_carta=[]
        elif el.tag==qn('w:tbl'):
            rows=[]
            for row in el.findall(qn('w:tr')):
                rows.append([''.join(n.text or '' for n in c.iter(qn('w:t'))) for c in row.findall(qn('w:tc'))])
            if rows:x.table(rows[0],rows[1:],[1.8,5.2],size=10.5)


def bitacora(x):
    x.page('Anexo H Bitácora de uso de IA')
    x.p('Alfa Consultora registra el apoyo documental y técnico de IA. El equipo completa los responsables de revisión y los ajustes humanos; no se atribuyen revisiones aún no registradas.',size=11)
    x.table(['Fecha','Uso de la herramienta','Revisión y ajustes'],[
        ('Preparación de visita','Codex e imágenes: identidad y formatos.','Completar fecha, integrante y revisión.'),
        ('17/11/2026','Codex: análisis, historias, UML y esquema.','Se acotó el seguimiento a datos y fechas. Revisor por registrar.'),
        ('17/11/2026','Codex: esqueleto Python y GitHub privado.','Nueve pruebas de infraestructura correctas; funciones de negocio pendientes.'),
        ('17/11/2026','Codex: minuta, carta y organización documental.','Se corrigieron asistentes y lugar. Exportación y respaldos excluidos; firmas pendientes.'),
        ('19/11/2026','Codex: informe autocontenido y priorización MoSCoW.','Se integraron análisis y anexos en un Word. Se registró la cancelación del video. Prioridades propuestas y revisión humana pendientes.'),
    ],[1.1,2.8,3.1],size=10.5)
    x.p('Las conclusiones individuales se redactan sin IA. Cada integrante debe poder explicar y modificar el código. Revisor y cambios finales: ____________________________',size=11)


def presentacion(x):
    x.page('Anexo I Preparación de la presentación')
    x.p('El paquete final se compone de informe técnico, presentación, diagramas, código y manual de usuario. Las diapositivas y el código completo se preparan con el sistema funcionando. El video fue cancelado.',size=11)
    x.table(['Bloque','Tiempo','Contenido'],[
        ('Apertura','2 min','Consultora, equipo, objetivo y agenda.'),
        ('Negocio','3 min','Proceso actual, problema e impacto medido.'),
        ('Análisis y diseño','6 min','RF, casos de uso, clases y una secuencia.'),
        ('Arquitectura','5 min','Componentes y evidencia de los seis paradigmas.'),
        ('Demostración','7 min','Tres escenarios de aceptación.'),
        ('Cierre','2 min','Beneficios, implantación y siguientes pasos.'),
        ('Preguntas y cambio','5 min','Preguntas y análisis de un cambio pequeño.'),
    ],[1.6,.8,4.6],size=10.5)
    x.p('Máximo de 15 diapositivas. Todos los integrantes participan y deben poder responder preguntas. Verificar equipo, datos sintéticos y apertura de archivos. La guía indica entregar el paquete digital 24 horas antes y llevar acta por duplicado, resumen ejecutivo y aplicación instalada.',size=11)
    x.p('Las etapas internas no generan informes adicionales. Si se conserva el control del 60 % de Must para la revisión de avance, esta propuesta tiene ocho Must y el mínimo aritmético sería cinco completos; confirmar la base de evaluación con el docente.',size=11)


def acta(x):
    x.page('Anexo I Acta de entrega y aceptación')
    x.p('Consultora: Alfa Consultora\nEmpresa: Urdiales Asesores\nFecha y lugar: __________________________________________________',size=11)
    x.h2('Elementos entregados')
    x.table(['Elemento','Recibido y observaciones'],[(t,'_______________________________') for t in ['Informe técnico','Presentación','Diagramas editables e imágenes','Código y datos de muestra','Manual de usuario']],[3.0,4.0],size=10.5)
    x.h2('Escenarios ejecutados')
    x.table(['Escenario','Resultado','Observaciones'],[('EA-___','____________','___________________') for _ in range(3)],[1.2,2.0,3.8],size=10.5)
    x.p('Decisión: [  ] Aceptada  [  ] Aceptada con observaciones  [  ] Rechazada',size=11)
    x.p('Observaciones: __________________________________________________\n________________________________________________________________',size=11)
    x.p('Por la empresa: __________________  Por Alfa Consultora: ______________',size=11)
    x.p('Nombre y cargo: __________________  Nombre: ________________________',size=11)
    x.p('Se completa al finalizar la presentación. Imprimir dos ejemplares.',size=10)


def manual():
    # Reutiliza el contenido de arranque comprobado y lo entrega sin carpetas por etapa.
    base.manual()
    anterior=OUT/'E4/PF_AlfaConsultora_Manual.docx'
    documento=Document(anterior)
    documento.sections[0].footer.paragraphs[0].runs[0].text='Alfa Consultora | Manual de usuario | '
    documento.save(OUT/'PF_AlfaConsultora_Manual.docx')
    anterior.unlink()
    anterior.parent.rmdir()


def indices():
    (OUT/'LEEME.md').write_text('''# Entrega final de Alfa Consultora

La documentación académica se concentra en un informe técnico autocontenido. El Word y su PDF incluyen análisis, requerimientos, historias, reglas, diagramas, trazabilidad, arquitectura, seis fichas, resultados disponibles y anexos. No se requiere abrir E1 o E2.

Los cinco elementos son informe, presentación, diagramas, código y manual. El video se canceló por indicación del equipo el 19 de noviembre de 2026. Las etapas E1–E4 solo organizan avances y responsabilidades.

| Elemento | Ubicación | Estado |
| --- | --- | --- |
| Informe técnico | PF_AlfaConsultora_Informe.docx y PDF | Integrado; faltan implementación, firmas, capturas, aceptación y conclusiones individuales |
| Presentación | Guion dentro del Anexo I del informe | Diapositivas pendientes; máximo 15 |
| Diagramas | PF_AlfaConsultora_UML.zip | Fuentes editables e imágenes; también se muestran en el informe |
| Código | Repositorio de la solución | Esqueleto; faltan casos completos y al menos 300 registros de muestra |
| Manual | PF_AlfaConsultora_Manual.docx y PDF | Inicio disponible; operación completa y capturas pendientes |

MoSCoW propuesto: ocho RF Must y tres Should; OP-01 Could corresponde a colores por aseguradora y EX-01 a EX-06 Won’t registran exclusiones. Los cinco RNF son Must. Should no elimina funciones acordadas: una reducción de compromiso debe revisarse con la empresa y el docente. La carga e indicadores académicos siguen pendientes de conciliación.

Las versiones por etapa del 17 de noviembre se conservaron en docs/historial/2026-11-17_entregables. Sus prioridades y referencias al video son históricas. Los originales del análisis y los diseños permanecen intactos.

Generación y verificación: herramientas/documentacion/README.md. Cada integrante redacta personalmente su conclusión de 150–250 palabras sin IA.
''',encoding='utf-8')
    (OUT/'Documentos_Generados.json').write_text(json.dumps(['PF_AlfaConsultora_Informe.docx','PF_AlfaConsultora_Manual.docx'],indent=2)+'\n')
    with (OUT/'Inventario_Entrega.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f)
        w.writerow(['Elemento','Contenido','Ubicación','Estado'])
        for fila in [
            ('Informe','Contexto y alcance','Sección 1','Integrado'),
            ('Informe','Marco teórico y referencias','Sección 2 y Referencias','Siete fuentes técnicas y académicas, incluidas dos académicas'),
            ('Informe','11 RF y 5 RNF con MoSCoW','Secciones 3 1 a 3 3','Priorización propuesta para validación'),
            ('Informe','Seis historias y doce criterios DCT','Sección 3 4 y Anexo C','Especificados'),
            ('Informe','UML y trazabilidad','Secciones 3 5 a 3 7 y Anexo A','Diseño propuesto; alinear con la implementación'),
            ('Informe','Tres casos de uso completos','Anexo D','Especificados'),
            ('Informe','Reglas y datos','Anexo B','Validar puntos abiertos'),
            ('Informe','Arquitectura y seis fichas','Sección 4','Dos fichas parciales y cuatro pendientes de código real'),
            ('Informe','Aceptación y evidencias','Sección 5 y Anexo E','Cinco escenarios no ejecutados; faltan capturas'),
            ('Informe','Conclusiones','Sección 6','Conclusiones individuales sin IA pendientes'),
            ('Informe','Entrevista minuta carta e IA','Anexos F a H','Firmas y revisión humana pendientes'),
            ('Presentación','Hasta 15 diapositivas','Guion del Anexo I','Diapositivas pendientes'),
            ('Diagramas','Fuentes e imágenes','PF_AlfaConsultora_UML.zip','Preparados como diseño'),
            ('Código','Python y datos de muestra','Repositorio','Casos completos y 300 registros pendientes'),
            ('Manual','Tres a seis páginas','PF_AlfaConsultora_Manual','Manual inicial; capturas pendientes'),
        ]:w.writerow(fila)
    with ZipFile(OUT/'PF_AlfaConsultora_UML.zip','w',ZIP_DEFLATED) as z:
        for sub in ('uml','imagenes'):
            for p in sorted((REPO/'docs/diseno'/sub).iterdir()):z.write(p,Path(sub)/p.name)
        for nombre in ('Matriz_Trazabilidad.csv','Requerimientos_Diseno.json'):
            z.write(REPO/'docs/diseno'/nombre,nombre)


def main():
    OUT.mkdir(exist_ok=True,parents=True)
    informe();manual();indices()
    print('Informe autocontenido y manual generados; renderizar y revisar todas las páginas.')


if __name__=='__main__':
    main()
