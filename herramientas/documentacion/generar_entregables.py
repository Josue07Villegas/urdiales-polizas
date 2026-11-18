"""Organiza el material existente sin sobrescribir los documentos fuente.

Ejecutar con el Python de las dependencias documentales de Codex.
El renderizado y la revisión visual son pasos posteriores obligatorios.
"""

from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import ast
import csv
import json
import shutil
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED

from docx import Document
from docx.enum.section import WD_SECTION_START, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from PIL import Image

from contenido import *

REPO = Path(__file__).resolve().parents[2]
WORK = REPO.parent
OUT = REPO / 'docs/entregables'
IMG = REPO / 'docs/diseno/imagenes'
FUENTES = WORK / 'diseno'
ARCHIVOS = []
REQ = json.loads((REPO/'docs/diseno/Requerimientos_Diseno.json').read_text())['requerimientos']
with (REPO/'docs/diseno/Matriz_Trazabilidad.csv').open(encoding='utf-8-sig', newline='') as f:
    TRAZAS = list(csv.DictReader(f))
CASOS = json.loads((Path(__file__).parent/'casos_uso.json').read_text())


class Doc:
    def __init__(self, titulo, clave, final=False):
        self.d = Document()
        self.clave = clave
        self.final = final
        self.contador = 0
        self.setup(self.d.sections[0])
        for nombre, size in [('Normal',12),('Title',20),('Heading 1',15),('Heading 2',12)]:
            st=self.d.styles[nombre]
            st.font.name='Arial';st.font.size=Pt(size);st.font.color.rgb=RGBColor(0,0,0)
            st.font.bold=nombre!='Normal'
            st.paragraph_format.space_after=Pt(6)
            st.paragraph_format.space_before=Pt(8 if nombre.startswith('Heading') else 0)
            st.paragraph_format.line_spacing=1.5 if final else 1.1
            st.paragraph_format.widow_control=True
            if nombre!='Normal':st.paragraph_format.keep_with_next=True
            for el in list(st.element.iter(qn('w:pBdr'))):el.getparent().remove(el)
        self.d.core_properties.title=titulo
        self.d.core_properties.author='Alfa Consultora'
        self.d.core_properties.last_modified_by='Alfa Consultora'
        self.d.core_properties.modified=datetime.now(timezone.utc)
        ft=self.d.sections[0].footer.paragraphs[0]
        ft.alignment=WD_ALIGN_PARAGRAPH.RIGHT
        ft.add_run('Alfa Consultora | '+clave+' | ').font.size=Pt(9)
        fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');ft._p.append(fld)
        if clave in ('E1','E4 Informe'):
            p=self.d.add_paragraph();p.paragraph_format.space_after=Pt(8)
            p.add_run().add_picture(str(OUT/'recursos/Alfa_Consultora_Logo.png'),width=Inches(1.65))
        self.page(titulo, first=True)

    def setup(self,s,land=False):
        s.orientation=WD_ORIENT.LANDSCAPE if land else WD_ORIENT.PORTRAIT
        s.page_width=Inches(11 if land else 8.5);s.page_height=Inches(8.5 if land else 11)
        s.top_margin=s.bottom_margin=Inches(.65)
        s.left_margin=s.right_margin=Inches(.75)
        s.header_distance=s.footer_distance=Inches(.28)

    def page(self,titulo,land=False,first=False):
        if not first:
            s=self.d.add_section(WD_SECTION_START.NEW_PAGE);self.setup(s,land)
            s.footer.is_linked_to_previous=True
        self.d.add_paragraph(titulo,'Title')

    def p(self,t='',bold=False,size=None,after=6):
        p=self.d.add_paragraph();p.paragraph_format.space_after=Pt(after)
        r=p.add_run(t);r.bold=bold
        if size:r.font.size=Pt(size)
        return p

    def h(self,t):self.d.add_paragraph(t,'Heading 1')
    def h2(self,t):self.d.add_paragraph(t,'Heading 2')
    def li(self,t):
        p=self.p('• '+t)
        p.paragraph_format.left_indent=Inches(.13);p.paragraph_format.first_line_indent=Inches(-.13)

    def table(self,headers,rows,widths=None,size=None):
        size=size or (12 if self.final else 10.5)
        t=self.d.add_table(rows=1,cols=len(headers));t.autofit=False;t.alignment=WD_TABLE_ALIGNMENT.CENTER
        if widths is None:widths=[7/len(headers)]*len(headers)
        for c,w in zip(t.columns,widths):c.width=Inches(w)
        pr=t._tbl.tblPr
        b=OxmlElement('w:tblBorders')
        for lado in ('top','left','bottom','right','insideH','insideV'):
            el=OxmlElement('w:'+lado)
            for k,v in [('val','single'),('sz','4'),('color','D9D9D9')]:el.set(qn('w:'+k),v)
            b.append(el)
        pr.append(b)
        for i,textos in enumerate([headers,*rows]):
            row=t.rows[0] if i==0 else t.add_row()
            rp=row._tr.get_or_add_trPr();rp.append(OxmlElement('w:cantSplit'))
            if i==0:rp.append(OxmlElement('w:tblHeader'))
            for j,(c,txt) in enumerate(zip(row.cells,textos)):
                c.width=Inches(widths[j]);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                cp=c._tc.get_or_add_tcPr();mar=OxmlElement('w:tcMar')
                for lado,val in [('top','80'),('bottom','80'),('left','90'),('right','90')]:
                    m=OxmlElement('w:'+lado);m.set(qn('w:w'),val);m.set(qn('w:type'),'dxa');mar.append(m)
                cp.append(mar)
                if i==0:
                    sh=OxmlElement('w:shd');sh.set(qn('w:fill'),'EAF0F4');cp.append(sh)
                p=c.paragraphs[0];p.paragraph_format.space_after=Pt(1)
                p.paragraph_format.line_spacing=1.5 if self.final else 1.03
                r=p.add_run(str(txt));r.font.size=Pt(size);r.bold=i==0
        self.p('',size=2,after=2)
        return t

    def fig(self,stem,titulo,land=False):
        self.contador+=1
        self.page('Anexo gráfico '+str(self.contador)+' '+titulo,land)
        path=IMG/(stem+'.png');w,h=Image.open(path).size
        maxw=9.35 if land else 6.9;maxh=5.65 if land else 8.5
        escala=min(maxw/w,maxh/h)
        p=self.d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing=1.0;p.paragraph_format.space_after=Pt(2)
        p.add_run().add_picture(str(path),width=Inches(w*escala),height=Inches(h*escala))
        self.p(f'Figura A{self.contador}. {titulo}. Fuente: elaboración de Alfa Consultora. Diseño propuesto.',size=10,after=2)

    def code(self,texto):
        p=self.d.add_paragraph();p.paragraph_format.line_spacing=1.0;p.paragraph_format.space_after=Pt(7)
        r=p.add_run(texto);r.font.name='DejaVu Sans Mono';r.font.size=Pt(9)

    def save(self,ruta):
        ruta=OUT/ruta;ruta.parent.mkdir(parents=True,exist_ok=True)
        self.d.save(ruta);ARCHIVOS.append(ruta)
        print(ruta.relative_to(REPO))
        return ruta


def cabecera(x,estado=True):
    x.p('Universidad Regiomontana',bold=True)
    x.p('Paradigmas de Programación')
    x.p('Docente: Azael Adan Gutierrez Castruita')
    x.p('Consultora: Alfa Consultora | Empresa: Urdiales Asesores')
    x.p('Monterrey, Nuevo León | '+FECHA)
    if estado:x.p('Versión para revisión académica. Implementación y validación final pendientes.',size=10.5)


def integrantes(x):
    x.p('Todos los integrantes participan de forma conjunta.',size=10.5 if not x.final else 12)
    x.table(['Nombre','Matrícula','Rol'],[(n,m,'Integrante') for n,m in EQUIPO],[4.5,1.0,1.5])


def propuesta():
    x=Doc('Propuesta de servicio para Urdiales Asesores','E1')
    cabecera(x)
    x.h('Consultora y equipo');integrantes(x)
    x.h('Empresa cliente')
    x.p(CONTEXTO)
    x.p('Contacto: José Urdiales Pérez, dueño. Ubicación de la visita: Monterrey, Nuevo León. Tamaño de la empresa, domicilio y medio de contacto: por confirmar.')
    x.h('Participación de la empresa')
    x.p('Se realizó una primera sesión el 5 de noviembre de 2026 a las 16:00 h. Asistieron José y Aurora por la empresa, y Scarlett, Josue y David por Alfa Consultora. La carta y la minuta se incluyen como formatos por revisar y firmar en Anexos.')

    x.page('Problema solución y alcance')
    x.h('Problema');x.p(PROBLEMA)
    x.h('Solución propuesta');x.p(OBJETIVO)
    x.h('Beneficios esperados')
    x.p('Disponer de un punto de consulta para los registros, reducir búsquedas dispersas, distinguir pólizas de un mismo asegurado y conservar la información de periodos anteriores. Estos beneficios se deberán comprobar con la empresa; no se atribuyen ahorros medidos.')
    x.h('Alcance incluido');x.p(ALCANCE)
    x.h('Alcance excluido');x.p(EXCLUSIONES)
    x.h('Objetivos de la intervención')
    for t in OBJETIVOS[:4]:x.li(t)

    x.page('Paradigmas reglas y visto bueno')
    x.h('Paradigmas por módulo')
    x.table(['Paradigma','Módulo previsto y justificación'],[(a,b+'\n'+c) for a,b,c,d in PARADIGMAS],[1.4,5.6],size=10)
    x.h('Reglas preliminares de negocio')
    for codigo,t in REGLAS_LOGICAS:x.p(codigo+' '+t,size=11)
    x.p('Estas reglas derivan de RF-06, RF-09 y RF-10. Las reglas de atención combinan varias condiciones; aplicabilidad, calendario y consultas del motor se revisarán con la empresa y el docente.',size=10.5)
    x.h('Visto bueno del docente')
    x.p('Observaciones: ______________________________________________________')
    x.p('Nombre y firma: __________________________  Fecha: ___________________')
    x.p('Carta de validación: Anexos/Carta_Membretada_Validacion_Alcance_Urdiales. Su firma o confirmación institucional sigue pendiente.',size=10.5)
    x.save(Path('E1/E1_AlfaConsultora_Propuesta.docx'))


def requisitos(x):
    anchos=[.7,5.3,1.0] if x.final else [.7,5.45,.85]
    x.table(['ID','Requerimiento funcional','MoSCoW'],[(r['id'],r['descripcion'],r['prioridad']) for r in REQ],anchos)
    x.p('M significa Must o indispensable. Son 11 RF de alcance acotado; la exportación a Excel y las funciones de respaldo no forman parte de esta entrega.',size=10.5 if not x.final else 12)


def historias(x,seleccion,completas=True):
    for codigo,t,rf,criterios in seleccion:
        x.h2(codigo+' '+t)
        x.p('Relación: '+rf,size=10.5 if not x.final else 12)
        for dado,cuando,entonces in (criterios if completas else criterios[:1]):
            x.p(dado+'. '+cuando[0].upper()+cuando[1:]+'. '+entonces[0].upper()+entonces[1:], size=11 if not x.final else 12)


def caso(x,datos):
    titulo,meta,basico,alternos,excepciones,post=datos
    for label,value in meta:x.p(label+': '+value,size=11)
    x.h2('Flujo básico')
    for i,t in enumerate(basico,1):x.p(str(i)+'. '+t,size=11,after=4)
    x.h2('Flujos alternos')
    for t in alternos:x.p(t,size=11,after=4)
    x.h2('Excepciones')
    for t in excepciones:x.p(t,size=11,after=4)
    x.h2('Postcondición');x.p(post,size=11)


def matriz(x):
    rows=[]
    for r in TRAZAS:
        rows.append((r['RF'],r['Casos de uso'],r['Clases'],r['Modulos propuestos'],r['Paradigmas']))
    x.table(['RF','CU','Clases','Archivo Python previsto','Paradigma'],rows,[.65,.85,1.75,4.4,1.85],size=9.5)
    x.p('Los archivos se ubican bajo src/urdiales_polizas/. Su existencia no acredita la implementación de las clases o del caso de uso. El estado actual es infraestructura y módulos reservados.',size=10)


def analisis():
    x=Doc('Análisis de requerimientos y diseño UML','E2')
    cabecera(x);x.h('Propósito')
    x.p('Especificar el problema, el alcance y el comportamiento esperado antes de implementar la solución. Este documento reúne el Componente 1 de la actividad y se incorpora como Anexo A del informe técnico.')
    x.h('Organización del documento')
    for t in ['1 Levantamiento y procesos','2 Requerimientos y reglas','3 Historias de usuario','4 Casos de uso','5 Trazabilidad y aceptación','6 Pendientes de validación','Anexo gráfico con diez figuras editables']:
        x.p(t,after=4)
    x.p('Fuentes: notas de la primera sesión, análisis base, diseños iniciales y aclaraciones posteriores del equipo. Las marcas R/C permanecen únicamente en el proceso actual. Los originales se conservan en Fuentes_originales.',size=10.5)

    x.page('1 Levantamiento y procesos')
    x.p(CONTEXTO);x.p(PROBLEMA)
    x.h2('Sesión y evidencia')
    x.p('5 de noviembre de 2026, 16:00 h, Monterrey, Nuevo León. Por la empresa: José Urdiales Pérez y Aurora. Por la consultora: Scarlett Alvarado Urdiales, Josue Abel Villegas Garcia y David Alejandro Carrillo Cázares.')
    x.p('El guion y la minuta están en Anexos. La minuta y carta son formatos completados para revisión; no se registra una firma ni confirmación por correo que no se haya recibido.')
    x.h2('Proceso actual')
    for i,t in enumerate(ACTUAL,1):x.p(str(i)+'. '+t,size=11,after=4)
    x.p(MARCAS,size=10.5)
    x.h2('Proceso propuesto')
    x.p('Consultar la cartera con filtros, derivar próximas fechas y guardar altas, cambios o nuevas vigencias con validación. Véanse las figuras A1 y A2 para los diagramas AS-IS y TO-BE.')

    x.page('2 Requerimientos funcionales')
    x.p('Alcance incluido: '+ALCANCE,size=11)
    requisitos(x)
    x.page('2 1 Requerimientos no funcionales')
    x.table(['ID','Condición','MoSCoW','Verificación prevista'],RNF,[.8,1.15,.85,4.2],size=11)
    x.h('Límites del alcance');x.p(EXCLUSIONES)
    x.h('Exigencias académicas por conciliar');x.p(ACLARACION)

    x.page('2 2 Reglas del negocio y decisiones')
    for codigo,t in REGLAS:x.h2(codigo);x.p(t)
    x.p('La renovación anual y la periodicidad del pago son conceptos separados. El vencimiento no implica cancelación automática ni acredita una regla legal. Un ajuste por día inhábil conserva la fecha contractual.',size=11)
    x.h2('Reglas propuestas para las consultas lógicas')
    for codigo,t in REGLAS_LOGICAS:x.p(codigo+' '+t,size=10.5,after=4)
    x.page('2 3 Diccionario de datos')
    x.table(['Entidad o grupo','Datos identificados','Tratamiento'],DATOS,[1.0,2.8,3.2],size=10.5)

    x.page('3 Historias de usuario de registro y consulta');historias(x,HISTORIAS[:3])
    x.page('3 1 Historias de atención renovación y edición');historias(x,HISTORIAS[3:])
    for i,c in enumerate(CASOS,1):
        x.page('4 '+str(i)+' '+c[0]);caso(x,c)
    x.page('5 Matriz de trazabilidad',land=True);matriz(x)
    x.page('5 1 Escenarios de aceptación')
    x.p('Estado de todos los escenarios de negocio: no ejecutados. Son criterios de la futura validación, con datos ficticios y fecha de referencia explícita.',bold=True)
    for s in ESCENARIOS[:3]:
        codigo,t,rel,datos,accion,esperado=s
        x.h2(codigo+' '+t);x.p('Relación: '+rel,size=10.5)
        x.p('Dado '+datos+' Cuando '+accion+' Entonces '+esperado,size=11)
    x.page('5 2 Escenarios de edición y persistencia')
    for s in ESCENARIOS[3:]:
        codigo,t,rel,datos,accion,esperado=s
        x.h2(codigo+' '+t);x.p('Relación: '+rel,size=10.5)
        x.p('Dado '+datos+' Cuando '+accion+' Entonces '+esperado,size=11)
    x.h('Registro de ejecución')
    x.table(['Escenario','Resultado observado','Validó y fecha'],[(s[0],'Pendiente de ejecutar','Por registrar') for s in ESCENARIOS],[1.0,3.8,2.2])
    x.page('6 Pendientes y confirmación de requerimientos')
    x.table(['ID','Responsables de revisión','Definición pendiente'],PENDIENTES,[.7,1.5,4.8],size=10.5)
    x.p('La validación debe confirmar los puntos abiertos y registrar los cambios en requerimientos, diagramas y matriz. La aprobación del alcance no equivale a aceptar un sistema terminado.')
    x.p('Revisó por la empresa: ____________________ Fecha: ____________________')
    x.p('Revisó por Alfa Consultora: ________________ Fecha: ____________________')
    for stem,t,land in DIAGRAMAS:x.fig(stem,t,land)
    x.save(Path('E2/E2_AlfaConsultora_Analisis_Diseno.docx'))


def resumen_texto(x):
    x.h('Problema');x.p(PROBLEMA)
    x.h('Solución y alcance');x.p(OBJETIVO)
    x.p('La solución prevista relaciona asegurados, contactos, pólizas, vigencias, vehículos y cobros. Ofrece filtros combinables y fechas próximas primero; al renovar conserva el periodo anterior en histórico.')
    x.h('Beneficios esperados')
    x.p('Un punto de consulta, menor dispersión de información y mejor identificación de fechas próximas. El ahorro de tiempo se medirá durante la validación; todavía no hay un resultado económico cuantificado.')
    x.h('Avance y siguientes pasos')
    x.p('Existen análisis, UML, esquema SQLite y una base ejecutable de infraestructura. Faltan los casos de uso completos, datos de demostración, evidencia de paradigmas y aceptación de la empresa. Exportación y respaldos están fuera del alcance.')


def marco(x,segunda=False):
    if not segunda:
        x.h('Programación multiparadigma')
        x.p('Un paradigma organiza conceptos para expresar una solución. Combinar paradigmas permite elegir herramientas distintas para cada parte del problema; el proyecto relaciona entidades, consultas y reglas sin atribuir toda la solución a una sola técnica (Van Roy, 2009).')
        x.h('Imperativo y estructurado')
        x.p('La programación imperativa describe cambios de estado mediante pasos. La estructura propuesta limita los flujos a secuencia, selección e iteración, separando funciones de carga, validación y coordinación. Una carga académica debe registrar válidos, inválidos y errores; ese módulo todavía está pendiente.')
        x.h('Orientación a objetos')
        x.p('El dominio propone entidades con estado y operaciones, una clase abstracta Poliza y especializaciones para autos y daños. Python proporciona ABC y abstractmethod para definir contratos abstractos (Python Software Foundation, s. f.-a). Herencia, polimorfismo y encapsulamiento deben demostrarse en el código que aún falta construir.')
    else:
        x.h('Declarativo y configuración')
        x.p('SQL expresa relaciones, restricciones y consultas. SQLite permite persistencia local sin un proceso servidor separado y sqlite3 ofrece parámetros para vincular valores a las consultas (Python Software Foundation, s. f.-c). TOML separa parámetros del código y tomllib permite leerlos desde Python 3.11 (Python Software Foundation, s. f.-d).')
        x.h('Funcional')
        x.p('Se propone transformar colecciones mediante funciones puras, composición y datos inmutables, manteniendo efectos de almacenamiento fuera de esas funciones. dataclass con frozen=True ayuda a expresar objetos cuyos campos no se reasignan normalmente después de crearse (Python Software Foundation, s. f.-b). La ficha funcional deberá mostrar además la evidencia específica exigida por la guía.')
        x.h('Programación lógica')
        x.p('La programación lógica describe relaciones mediante hechos, reglas y consultas. La interpretación procedimental de implicaciones permite resolver consultas a partir de esos enunciados (Kowalski, 1974). En el proyecto se propone consultar casos de atención por fecha, con al menos ocho hechos, tres reglas y tres consultas de interfaz, además de su equivalente en Prolog. La biblioteca y el módulo están pendientes.')


def ficha(x,indice):
    nombre,modulo,problema,estado=PARADIGMAS[indice]
    x.page('4 '+str(indice+1)+' Ficha de paradigma '+nombre.lower())
    x.h2('1 Ubicación');x.p('src/urdiales_polizas/'+modulo)
    x.h2('2 Problema que resuelve');x.p(problema+' Relación prevista: '+(['requisito académico de carga; RF-01 a RF-05','coordinación de RF-01 a RF-11','RF-01 a RF-05, RF-08, RF-09 y RF-11','persistencia de RF-01 a RF-11 y RNF-01, RNF-02','RF-06, RF-10 e indicadores académicos por conciliar','RF-10 y consultas lógicas académicas'][indice]))
    x.h2('3 Características aplicadas y estado');x.p(estado)
    x.h2('4 Fragmento comentado del código real')
    if indice==1:
        fuente=(REPO/'src/urdiales_polizas/persistencia/base_datos.py').read_text()
        bloque=fuente.split('def comprobar_esquema()',1)[1].split('\ndef inicializar_bd',1)[0].strip()
        x.code('def comprobar_esquema()'+bloque)
        x.p('Lectura del fragmento: la secuencia crea el esquema; if selecciona el error; try/finally asegura el cierre. Procede de persistencia/base_datos.py y verifica infraestructura, no un caso de uso terminado.',size=10)
    elif indice==3:
        fuente=(REPO/'src/urdiales_polizas/persistencia/esquema.sql').read_text()
        bloque='CREATE TABLE cobros'+fuente.split('CREATE TABLE cobros',1)[1].split('\nCREATE INDEX',1)[0]
        x.code(bloque.strip())
        x.p('Lectura del fragmento: REFERENCES expresa la relación; CHECK define dominios y fechas; UNIQUE evita repetir un vencimiento en la misma vigencia. Está en el esquema que carga la aplicación. Faltan conectar cuatro consultas, incluidas JOIN y GROUP BY.',size=10)
    else:
        x.p('Pendiente de incorporar un fragmento de 10 a 25 líneas de la implementación real con comentarios. El archivo reservado no constituye evidencia del paradigma.')
    x.h2('5 Justificación y alternativa')
    alternativas=[
        'Un recorrido paso a paso facilita contabilizar errores de carga. Se comparará con una transformación funcional; esta última puede simplificar datos, pero no sustituye el registro explícito exigido por la guía.',
        'Separar funciones facilita seguir el arranque y el manejo de errores. La alternativa de concentrar flujo, interfaz y SQL en una sola función dificultaría revisar responsabilidades.',
        'La especialización propuesta diferencia validaciones de autos y daños a través de un contrato común. Se comparará con diccionarios y condicionales; la decisión debe demostrarse con llamadas polimórficas reales.',
        'Las restricciones SQL concentran integridad en el almacenamiento. Validar solamente en formularios dejaría sin protección otras escrituras; la aplicación también debe validar y presentar errores comprensibles.',
        'Funciones puras permitirían comprobar clasificación y orden sin modificar registros. La alternativa imperativa deberá compararse una vez implementadas las transformaciones y los indicadores acordados.',
        'Un motor lógico permitirá expresar hechos, reglas y consultas explícitas. Una cadena de if no acredita por sí sola la evidencia lógica; se elegirá kanren o sympy.logic y se documentará su equivalente Prolog.',
    ]
    x.p(alternativas[indice])
    x.h2('6 Ventajas y limitaciones observadas')
    if indice in (1,3):x.p('La verificación disponible cubre arranque, configuración y esquema. Las observaciones de uso del equipo y de la empresa deben agregarse al implementar y probar los casos de negocio; no se atribuyen experiencias de programación no registradas.')
    else:x.p('Pendiente de completar por el equipo después de programar y probar el módulo. Registrar qué se facilitó, qué se complicó y qué se cambiaría; no se inventan resultados de una implementación ausente.')


def informe():
    x=Doc('Informe técnico del registro de clientes y pólizas','E4 Informe',final=True)
    cabecera(x);integrantes(x)
    x.p('Documento de avance organizado conforme a la sección 7 de la actividad. La aceptación final, las capturas de operación, el cierre de las seis fichas y las conclusiones individuales todavía deben completarse.')
    x.p('El Anexo A reúne la especificación del Componente 1 en el documento E2; los demás anexos reúnen la evidencia documental y el manual. La edición Word conserva esos anexos como archivos editables separados.')
    x.page('Resumen ejecutivo');resumen_texto(x)
    x.page('1 Introducción')
    x.h('Contexto de la empresa');x.p(CONTEXTO)
    x.h('Planteamiento del problema');x.p(PROBLEMA)
    x.h('Objetivo general');x.p(OBJETIVO)
    x.h('Objetivos específicos')
    for t in OBJETIVOS:x.li(t)
    x.page('1 1 Alcance y delimitación')
    x.h('Funciones incluidas');x.p(ALCANCE)
    x.h('Funciones excluidas');x.p(EXCLUSIONES)
    x.h('Condiciones académicas');x.p(ACLARACION)
    x.h('Información pendiente de validar')
    x.p('Aplicabilidad de los 30 días, calendario inhábil, contactos y referentes, flotillas, catálogo de aseguradoras, canceladas e histórico. El tamaño de la empresa, el equipo de despliegue y el costo de búsqueda todavía deben precisarse. Los puntos están detallados en E2.')
    x.page('2 Marco teórico de paradigmas');marco(x)
    x.page('2 1 Persistencia transformaciones y lógica');marco(x,True)
    x.page('3 Análisis y diseño')
    x.h('Levantamiento');x.p('La entrevista inicial se realizó el 5 de noviembre de 2026 a las 16:00 h en Monterrey, Nuevo León. Asistieron José Urdiales Pérez y Aurora por la empresa, y Scarlett, Josue y David por Alfa Consultora. El guion y la minuta acompañan el Anexo A. Las firmas o confirmaciones se integrarán cuando se reciban.')
    x.h('Proceso actual y propuesto');x.p(MARCAS)
    x.p('La propuesta reúne registros y calcula atención por fechas para una consulta ordenada. Captura, consulta y edición se coordinan con dominio y persistencia. Las figuras A1 y A2 de E2 presentan AS-IS y TO-BE; las figuras A3 a A10 reúnen casos de uso, clases, datos, secuencias, componentes y boceto.')
    x.h('Documentación integrada')
    x.p('El Anexo A conserva 11 RF, 5 RNF, reglas y diccionario de datos, seis historias con criterios Dado/Cuando/Entonces, tres casos de uso detallados, matriz y cinco escenarios de aceptación. La síntesis de las siguientes secciones no sustituye sus especificaciones completas.')
    x.page('3 1 Requerimientos funcionales');requisitos(x)
    x.page('3 2 Calidad e historias de usuario')
    x.table(['ID y prioridad','Condición verificable'],[(a+' '+c,d) for a,b,c,d in RNF],[1.1,5.9])
    x.p('Todos los RNF tienen prioridad Must. Sus verificaciones están en E2, sección 2 1. La persistencia conserva los cambios al reabrir; es un criterio distinto de una función de respaldo.')
    x.page('3 3 Historias de usuario')
    x.table(['Historia','Necesidad y RF'],[(h[0],h[1]+'\n'+h[2]) for h in HISTORIAS],[.9,6.1],size=12)
    x.page('3 4 Casos de uso reglas y trazabilidad')
    x.p('Los tres casos principales detallados son CU-02 Registrar o editar una póliza, CU-03 Consultar cartera y aplicar filtros y CU-06 Registrar una renovación. E2 conserva flujos básicos, alternos, excepciones y postcondiciones.')
    for codigo,t in REGLAS[:4]:x.p(codigo+' '+t)
    x.p('La matriz de E2, sección 5, vincula cada RF con casos de uso, clases, archivos Python y paradigma. Sus módulos existen como infraestructura o espacios reservados; la trazabilidad a clases implementadas deberá verificarse después de programar.')
    x.p('El modelo relacional separa ocho tablas para evitar mezclar titulares, pólizas, periodos, unidades y cobros. Los números de póliza, series y teléfonos son texto; las fechas se conservan completas y la renovación no sobrescribe el periodo anterior.')
    x.page('4 Implementación y arquitectura')
    x.p('La versión 0.1.0 del repositorio prepara una aplicación local con Python, SQLite y configuración TOML. La interfaz inicial usa Tkinter. El código disponible permite validar configuración, comprobar el SQL en memoria e inicializar una base vacía. La ventana contiene pestañas informativas sin captura ni consulta operativa.')
    x.table(['Capa','Responsabilidad y estado'],[
        ('Interfaz y aplicación','Arranque y ventana inicial disponibles; coordinación de casos de uso pendiente.'),
        ('Dominio','Espacios para entidades; faltan clases de negocio, herencia, polimorfismo y encapsulamiento.'),
        ('Persistencia','Conexión e inicialización del esquema disponibles; repositorios de negocio pendientes.'),
        ('Consultas y reglas','Módulos reservados; faltan funciones puras y motor lógico.'),
    ],[1.3,5.7],size=12)
    x.p('Las seis fichas siguientes separan evidencia disponible de trabajo pendiente. El esquema y los archivos por sí solos no acreditan los seis paradigmas.')
    for i in range(6):ficha(x,i)
    x.page('5 Resultados y aceptación')
    x.p('En la verificación de infraestructura del 17 de noviembre de 2026 se aprobaron nueve pruebas de configuración, esquema y arranque. El diagnóstico confirmó ocho tablas en memoria. Estas pruebas no acreditan los requerimientos de negocio ni sustituyen la aceptación de la empresa.')
    x.p('Comprobaciones: resolución de rutas TOML; rechazo de valores inválidos y campos faltantes; creación del esquema; integridad referencial; conservación al reinicializar; rechazo de otro esquema; diagnóstico sin crear archivos y error comprensible ante configuración ausente.')
    x.table(['Escenario','Criterio de aceptación','Resultado'],[(s[0],s[1],'No ejecutado') for s in ESCENARIOS],[1.1,3.9,2.0],size=12)
    x.p('Pendiente: capturas del sistema operando con los casos completos, al menos 300 registros de muestra, ejecución de los cinco escenarios, selección de tres para demostración y retroalimentación documentada de Aurora y José. El boceto A10 es diseño y no se presenta como captura del sistema funcionando.')
    x.page('6 Conclusiones')
    x.h('Conclusión del equipo sobre el avance')
    x.p('El levantamiento permitió delimitar una necesidad de consulta y almacenamiento centralizado. Se estructuraron relaciones entre asegurados, pólizas y vigencias y se documentaron reglas y criterios de aceptación. La infraestructura disponible comprueba configuración y esquema, pero todavía no permite evaluar beneficios operativos ni dar por cumplidos los casos de negocio. La siguiente etapa consiste en validar los puntos abiertos e implementar registro, consulta, filtros e histórico antes de ejecutar la aceptación.')
    x.h('Conclusiones individuales')
    x.p('Cada integrante debe redactar de 150 a 250 palabras sin IA, conforme a la actividad. Se reservan sus espacios sin redactar contenido en su nombre.')
    for n,m in EQUIPO:x.p(n+' — redacción personal pendiente.',size=12)
    x.h('Trabajo futuro')
    x.p('Completar los módulos, conciliar evidencia académica de carga e indicadores, preparar datos sintéticos, validar con la empresa y actualizar manual, fichas y resultados. La exportación y los respaldos permanecen excluidos de esta entrega.')
    x.page('Referencias')
    titulos_en_cursiva=[
        'Information Processing 74',
        'abc — Abstract base classes',
        'dataclasses — Data classes',
        'sqlite3 — DB-API 2.0 interface for SQLite databases',
        'tomllib — Parse TOML files',
        'New computational paradigms for computer music',
    ]
    for (texto,url),titulo in zip(REFERENCIAS,titulos_en_cursiva):
        antes,despues=texto.split(titulo,1)
        p=x.p(antes)
        p.add_run(titulo).italic=True
        p.add_run(despues+' '+url)
        p.paragraph_format.left_indent=Inches(.3);p.paragraph_format.first_line_indent=Inches(-.3)
        p.paragraph_format.line_spacing=1.5
    x.p('Proyecto integrador final versión 2 Lite. (s. f.). Material de la asignatura Paradigmas de Programación proporcionado al equipo.')
    x.page('Anexos')
    x.p('Los anexos se agregan al PDF del informe y se conservan como documentos editables separados en este paquete. Las firmas y la aceptación se integran cuando se obtengan.')
    x.table(['Anexo','Documento'],[
        ('A','E2 Análisis de requerimientos y diseño UML.'),
        ('B','Guion de entrevista consolidado.'),
        ('C','Minuta de la primera sesión por revisar y firmar.'),
        ('D','Carta de validación y alcance por revisar y firmar.'),
        ('E','Manual de usuario de la versión inicial.'),
        ('F','Bitácora de uso de IA por completar con revisión del equipo.'),
    ],[.8,6.2])
    x.p('El acta de entrega y aceptación permanece como formato separado para el día de la presentación. Las diapositivas, el video y el paquete de código final se prepararán con el sistema terminado; el guion de entrega organiza ese trabajo.')
    x.save(Path('E4/PF_AlfaConsultora_Informe.docx'))


def manual():
    x=Doc('Manual de usuario de la versión inicial','E4 Manual')
    x.p('Urdiales Asesores | Alfa Consultora | '+FECHA)
    x.h('Alcance de esta versión')
    x.p('Este manual describe el arranque disponible de la versión 0.1.0. Aún no permite capturar clientes ni consultar pólizas desde los formularios. Las instrucciones de operación se completarán al implementar los casos de uso.')
    x.h('Requisitos')
    x.p('Python 3.11 o superior con SQLite y TOML. Para abrir la ventana se requiere Tkinter y un entorno gráfico. No se requiere Excel ni un servidor de base de datos. El equipo definitivo y su sistema operativo están por confirmar.')
    x.h('Inicio en cinco pasos')
    for t in [
        '1. Obtener la carpeta del proyecto y abrirla en el equipo de instalación.',
        '2. Verificar Python 3.11 o superior con python3 --version; en Windows puede usarse py -3.11.',
        '3. Si se requiere personalizar la ruta local, copiar config.example.toml como config.toml. La ruta de datos se interpreta desde ese archivo.',
        '4. Ejecutar python3 main.py --comprobar y confirmar que se informa configuración válida y ocho tablas en memoria.',
        '5. Ejecutar python3 main.py para abrir la ventana inicial. En Windows sustituir python3 por el comando correspondiente.',
    ]:x.p(t,size=11)
    x.p('El diagnóstico y la apertura de la ventana no crean una base de clientes. No hay registros de demostración precargados.',size=10.5)
    x.page('Comprobación y base local')
    x.h('Diagnóstico')
    x.code('python3 main.py --comprobar')
    x.p('La salida esperada informa configuración válida, anticipación de 30 días, ocho tablas comprobadas en memoria y ruta prevista. No modifica ni crea la base de datos local.')
    x.h('Inicialización explícita')
    x.code('python3 main.py --inicializar-bd')
    x.p('Esta orden crea una base vacía en la ruta configurada. Si ya existe con la misma versión y tablas esperadas, conserva los registros. Si tiene otro esquema o versión, devuelve un error y no intenta migrarla. Debe realizarla la persona responsable de instalar el proyecto.')
    x.h('Mensajes frecuentes')
    x.table(['Mensaje o situación','Acción'],[
        ('Archivo TOML ausente','Revisar la ruta indicada en --config o ejecutar desde la carpeta del proyecto.'),
        ('Faltan campos o anticipación inválida','Revisar el archivo de configuración con el responsable del proyecto.'),
        ('No hay pantalla o Tkinter no está disponible','Usar el diagnóstico y solicitar revisión del entorno gráfico.'),
        ('Base con otro esquema o versión','Detener la inicialización y consultar al equipo; no borrar el archivo para continuar.'),
    ],[2.8,4.2],size=10.5)
    x.page('Operación y revisión del manual')
    x.h('Pantallas disponibles')
    x.p('La ventana inicial muestra pestañas Cartera, Clientes e Histórico con un aviso de preparación. El botón Cerrar termina la ventana. Estas pestañas todavía no leen ni escriben registros.')
    x.h('Procedimientos que faltan integrar')
    for t in ['Registrar y editar un asegurado y sus contactos.','Registrar pólizas de autos, daños y flotillas.','Combinar filtros y revisar fechas próximas.','Actualizar un cobro y registrar una renovación.','Consultar vigencias anteriores y vencidas en histórico.']:x.li(t)
    x.h('Capturas y validación')
    x.p('Agregar capturas reales de las operaciones anteriores y sus mensajes después de implementarlas. El boceto del análisis no sustituye una captura del sistema terminado. Aurora deberá revisar las instrucciones y el equipo registrará las observaciones antes de cerrar el manual.')
    x.p('Revisó por la empresa: ___________________  Fecha: _____________________')
    x.p('Responsable del manual: _________________  Versión: ___________________')
    x.save(Path('E4/PF_AlfaConsultora_Manual.docx'))


def resumen():
    x=Doc('Resumen ejecutivo para Urdiales Asesores','E4 Resumen')
    x.p('Alfa Consultora | Universidad Regiomontana | '+FECHA)
    resumen_texto(x)
    x.save(Path('E4/PF_AlfaConsultora_Resumen_Ejecutivo.docx'))


def bitacora():
    x=Doc('Bitácora de uso de inteligencia artificial','Anexo C de la actividad')
    x.p('Alfa Consultora | Universidad Regiomontana')
    x.p('Registro de apoyos documentados en esta conversación. El equipo debe completar quién revisó cada resultado y qué ajustes realizó; no se atribuyen revisiones personales no registradas.')
    x.table(['Fecha e integrante','Herramienta y uso','Ajustes y verificación'],[
        ('Preparación de visita\nFecha e integrante por registrar','Codex y generación de imágenes: identidad de Alfa Consultora y formatos de visita.','Se incorporaron datos de empresa, universidad y equipo; revisar y registrar responsable.'),
        ('17/11/2026\nRevisor por registrar','Codex: organizar notas, requerimientos, historias, UML y esquema propuesto.','Se acotó el seguimiento a datos y fechas y se separaron marcas actuales del diseño; verificar con la empresa.'),
        ('17/11/2026\nRevisor por registrar','Codex: esqueleto Python, README y publicación privada en GitHub.','Nueve pruebas de infraestructura y diagnóstico correctos; no acreditan funciones de negocio.'),
        ('17/11/2026\nRevisor por registrar','Codex: minuta y carta de validación.','Se corrigieron asistentes y lugar; exportación y respaldos quedaron excluidos. Firma pendiente.'),
        ('17/11/2026\nRevisor por registrar','Codex: estructurar entregables de la actividad.','Se conservaron originales, se actualizaron historias y escenarios, se verificaron referencias y se revisó la maquetación. Registrar revisión humana final.'),
    ],[1.35,2.75,2.9],size=10)
    x.p('Las conclusiones individuales no se redactan con IA. Todo integrante debe poder explicar y modificar cualquier parte del código, como indica la actividad.',size=10.5)
    x.save(Path('Anexos/Bitacora_Uso_IA.docx'))


def acta():
    x=Doc('Acta de entrega y aceptación','Anexo D de la actividad')
    x.p('Consultora: Alfa Consultora\nEmpresa cliente: Urdiales Asesores\nFecha y lugar: _____________________________________________________')
    x.h('Elementos entregados')
    x.table(['Elemento','Recibido y observaciones'],[(t,'________________________________') for t in ['Informe','UML editable e imágenes','Código y datos de muestra','Manual','Presentación','Video']],[3.0,4.0])
    x.h('Escenarios ejecutados')
    x.table(['Escenario','Resultado','Observaciones'],[('EA-___','________________','___________________') for _ in range(3)],[1.2,2.0,3.8])
    x.h('Decisión del cliente')
    x.p('Marcar una:  [  ] Aceptada   [  ] Aceptada con observaciones   [  ] Rechazada')
    x.p('Observaciones: _____________________________________________________\n__________________________________________________________________')
    x.p('Por el cliente: ______________________  Por Alfa Consultora: ______________')
    x.p('Nombre y cargo: ___________________  Nombre: _______________________')
    x.p('Se completa al terminar la presentación. Imprimir dos ejemplares.',size=10)
    x.save(Path('Anexos/Acta_Entrega_Aceptacion.docx'))


def guion_entrevista():
    x=Doc('Guion de entrevista y validación de requerimientos','Anexo de E2')
    x.p('Urdiales Asesores | Alfa Consultora')
    x.p('Preguntas consolidadas del levantamiento y de las definiciones que permanecen abiertas. Las respuestas recabadas se encuentran en la minuta y en E2; este guion no acredita por sí solo que una respuesta haya sido confirmada.')
    x.h('Proceso y datos')
    for t in [
        '1. ¿Dónde registran a los asegurados y las pólizas después de emitirlas y quién mantiene esos datos?',
        '2. ¿Cómo buscan actualmente un registro y qué consulta les toma más tiempo? Medir una búsqueda de ejemplo.',
        '3. ¿Qué datos comparten autos y daños y cuáles son específicos del vehículo o del riesgo?',
        '4. ¿Cómo se relacionan varios contactos y medios de contacto con el asegurado y sus pólizas?',
        '5. ¿Cómo distinguen la póliza matriz, los incisos y las series en una flotilla?',
        '6. ¿Qué cambia al renovar: número de póliza, vigencia, riesgos y forma de pago?',
    ]:x.p(t)
    x.h('Fechas y consultas')
    for t in [
        '7. ¿Qué combinaciones de asegurado, aseguradora, fechas y cobranza o renovación necesitan consultar?',
        '8. ¿A qué casos aplican los 30 días de anticipación y qué calendario inhábil se utiliza?',
        '9. ¿Qué información debe conservarse en el histórico y quién puede corregirla?',
    ]:x.p(t)
    x.page('Validación de alcance y cierre')
    for t in [
        '10. ¿En qué casos se cancela una póliza y cómo debe aplicarse la restricción de reactivación?',
        '11. ¿Qué datos se capturan para cada cobro y cómo se confirma su estado?',
        '12. ¿En qué equipo y sistema operativo se instalará la solución y quién será su usuario principal?',
        '13. ¿Los ejemplos sintéticos representan sus casos de autos, daños, contactos y flotillas?',
        '14. ¿Los cinco escenarios de E2 reflejan el resultado que esperan? Registrar cambios concretos.',
        '15. ¿Se confirma el alcance acotado, con exportación a Excel y respaldos fuera de esta entrega?',
        '16. ¿Qué observaciones tienen sobre la carta y minuta y cuándo se realizará la siguiente validación?',
    ]:x.p(t)
    x.h('Registro de la validación')
    x.p('Fecha: ___________________ Participantes: _____________________________')
    x.p('Acuerdos: _________________________________________________________\n__________________________________________________________________\n__________________________________________________________________')
    x.p('Pendientes y responsables: ___________________________________________\n__________________________________________________________________')
    x.p('Confirmó por la empresa: ___________________ Medio o firma: ____________')
    x.save(Path('Anexos/Guion_Entrevista_Validacion.docx'))


def guion_entregas():
    x=Doc('Guion de revisión de avance y entrega formal','E3 y E4')
    x.h('E3 Revisión de avance de diez minutos')
    x.p('La guía exige al menos 60 % de los Must funcionando. Con 11 RF Must, se requieren al menos siete RF completos. La infraestructura actual no satisface todavía ese umbral.')
    x.table(['Tiempo','Contenido'],[
        ('0 a 1 min','Presentar el problema y el alcance acotado.'),
        ('1 a 2 min','Mostrar qué siete RF o más están terminados y cómo se verificaron.'),
        ('2 a 8 min','Demostrar esos casos con registros sintéticos y relaciones coherentes.'),
        ('8 a 10 min','Precisar lo pendiente y recoger observaciones del docente.'),
    ],[1.25,5.75])
    x.p('Antes de ensayar, completar una lista RF por RF con evidencia operativa. No contar módulos vacíos, diagramas ni pruebas de infraestructura como funciones terminadas.')
    x.h('Video de respaldo de cinco minutos como máximo')
    x.p('Preparar con el sistema funcionando: problema y alcance, recorrido por los casos principales, filtros y fechas, renovación e histórico y cierre. Grabar datos sintéticos, identificar la versión y verificar que se abre el archivo. El video sigue pendiente y no se sustituye por este guion.')
    x.page('E4 Presentación y paquete final')
    x.p('La actividad permite un máximo de 15 diapositivas. Todos los integrantes exponen y deben poder responder preguntas. Los roles de exposición se acuerdan en equipo; no se asignan responsabilidades individuales nuevas.')
    x.table(['Bloque','Tiempo','Material'],[
        ('Apertura','2 min','Consultora, equipo, objetivo y agenda.'),
        ('Negocio','3 min','AS-IS, problema e impacto medido.'),
        ('Análisis y diseño','6 min','RF, casos de uso, clases y una secuencia.'),
        ('Arquitectura y paradigmas','5 min','Componentes y evidencia del código.'),
        ('Demostración','7 min','Tres escenarios elegidos por el cliente.'),
        ('Cierre','2 min','Beneficios, implantación y siguientes pasos.'),
        ('Preguntas y cambio','5 min','Responder y analizar un cambio pequeño.'),
    ],[2.0,.8,4.2],size=10.5)
    x.p('La entrega digital se realiza 24 horas antes: informe PDF, UML editable e imágenes, código y datos de muestra sin entorno virtual, manual PDF, presentación PDF y video MP4. Se usa AlfaConsultora como identificador a petición del equipo; verificar que la plataforma acepte ese nombre en lugar de Equipo#.',size=10.5)
    x.p('El día de entrega: resumen ejecutivo impreso, acta por duplicado y sistema instalado con datos de demostración. Llegar diez minutos antes y comprobar el equipo. Diapositivas, video, aceptación y paquete de código final quedan por preparar.',size=10.5)
    x.save(Path('E3_y_E4/Guion_Revision_Presentacion_Video.docx'))


def copiar_fuentes():
    destino=OUT/'Fuentes_originales';destino.mkdir(parents=True,exist_ok=True)
    fuentes=[*sorted((WORK/'output/analisis').glob('*.docx'))]
    if (FUENTES/'documentacion/Disenos_Urdiales_v1.docx').exists():fuentes.append(FUENTES/'documentacion/Disenos_Urdiales_v1.docx')
    manifiesto=[]
    for f in fuentes:
        copia=destino/f.name;shutil.copy2(f,copia)
        manifiesto.append({'archivo':str(f.relative_to(WORK)), 'copia':str(copia.relative_to(OUT)), 'sha256':sha256(f.read_bytes()).hexdigest()})
    if manifiesto:(destino/'Inventario_Originales.json').write_text(json.dumps(manifiesto,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (destino/'LEEME.txt').write_text('Documentos fuente conservados sin alteración. Son material de consulta e historial de trabajo.\nEl alcance vigente y los criterios consolidados están en E1 y E2. Los estados literales R/C y RF-12 de análisis anteriores no rigen esta versión.\n',encoding='utf-8')
    anexos=OUT/'Anexos';anexos.mkdir(exist_ok=True)
    for f in (WORK/'output/documentos_firma_urdiales').glob('*'):
        if f.suffix in ('.docx','.pdf'):shutil.copy2(f,anexos/f.name)
    uml=OUT/'E4/PF_AlfaConsultora_UML.zip';uml.parent.mkdir(exist_ok=True,parents=True)
    with ZipFile(uml,'w',ZIP_DEFLATED) as z:
        for sub in ('uml','imagenes'):
            for f in sorted((REPO/'docs/diseno'/sub).iterdir()):z.write(f,Path(sub)/f.name)
        z.write(REPO/'docs/diseno/Matriz_Trazabilidad.csv','Matriz_Trazabilidad.csv')


def indice():
    (OUT/'LEEME.md').write_text('''# Documentos de la actividad de Alfa Consultora

La información de análisis y diseño se conserva y se organiza según la guía. Abrir E1 para la propuesta; E2 para el Componente 1 consolidado y E4 para el informe técnico, manual y resumen.

| Carpeta | Documento y uso |
| --- | --- |
| E1 | Propuesta de servicio con campos del Anexo A y participación conjunta del equipo |
| E2 | Levantamiento, 11 RF, 5 RNF, seis historias actualizadas, reglas, datos, tres CU, trazabilidad, aceptación y UML |
| E3_y_E4 | Guion de la revisión de avance, presentación y video pendientes de ejecución |
| E4 | Informe en desarrollo, manual de la versión inicial, resumen ejecutivo y paquete UML |
| Anexos | Carta, minuta, guion consolidado, bitácora de IA y acta sin completar |
| Fuentes_originales | Análisis base y catálogo de diseños conservados sin cambios con sus hashes |

## Estado y uso

Los Word son editables. Los PDF corresponden al contenido revisado visualmente. El PDF del informe incluye los anexos; la versión Word mantiene los anexos como archivos separados para editar. No se presenta el conjunto como una entrega final aceptada.

La propuesta tiene 3 páginas y E2 tiene 25. El informe cuenta con 21 páginas de cuerpo, una de índice de anexos y 35 de anexos, para un total de 57 en PDF. El manual inicial tiene 3 páginas. Las instrucciones para regenerar estos documentos están en herramientas/documentacion/README.md del repositorio.

Faltan las firmas o confirmaciones de carta y minuta, validaciones abiertas con empresa y docente, casos de uso operativos, 300 datos de muestra, fichas completas con código real, capturas y resultados de aceptación. Cada integrante redacta 150–250 palabras de conclusión individual sin IA. Las diapositivas y el video se preparan con el sistema funcionando; el guion no los sustituye.

Exportación a Excel y funciones de respaldo/restauración de datos quedan excluidas. El video de respaldo sí es un entregable obligatorio. La evidencia académica de carga/limpieza e indicadores se conserva pendiente de conciliación, sin presumir una excepción del docente.

Se usa AlfaConsultora como identificador a petición del equipo. Confirmar la nomenclatura permitida al subir los archivos a la plataforma. Consultar Inventario_Entregables.csv para los requisitos de cada entrega y su estado.
''',encoding='utf-8')
    rows=[
        ('E1','Campos del Anexo A','E1/E1_AlfaConsultora_Propuesta','Preparados; tamaño, contacto y visto bueno pendientes'),
        ('E1','Carta de validación','Anexos/Carta_Membretada_Validacion_Alcance_Urdiales','Formato completado; firma o confirmación institucional pendiente'),
        ('E2','Guion y minuta','Anexos/Guion_Entrevista_Validacion; Anexos/Minuta_Primera_Sesion_Urdiales_Alcance_Acotado','Guion consolidado y minuta; firma pendiente'),
        ('E2','11 RF y 5 RNF con MoSCoW','E2 secciones 2 y 2 1','Documentados; validación pendiente'),
        ('E2','Seis historias y criterios Dado/Cuando/Entonces','E2 sección 3','Actualizadas sin flujo literal R/C'),
        ('E2','Tres casos detallados y matriz','E2 secciones 4 y 5','Documentados; clases de negocio por implementar'),
        ('E2','UML e imágenes editables','E2 anexo gráfico; E4/PF_AlfaConsultora_UML.zip','Propuestos; actualizar para coincidir con código'),
        ('E3','Demo de diez minutos y 60 % Must','E3_y_E4/Guion_Revision_Presentacion_Video','Pendiente; se requieren al menos siete de once RF Must completos'),
        ('E4','Informe de 15 a 25 páginas sin anexos','E4/PF_AlfaConsultora_Informe','Avance; completar implementación, resultados y conclusiones individuales'),
        ('E4','Seis referencias y dos académicas','Informe sección 2 y Referencias','Seis referencias técnicas/académicas verificadas, incluidas dos académicas'),
        ('E4','Seis fichas de paradigma','Informe sección 4','Estructurado y declarativo parciales; las demás pendientes de código real'),
        ('E4','Manual de 3 a 6 páginas con capturas','E4/PF_AlfaConsultora_Manual','Manual inicial; capturas y operación completa pendientes'),
        ('E4','Cinco escenarios; tres al azar en presentación','E2 sección 5 1 y 5 2; Informe sección 5','Definidos con datos concretos; no ejecutados en la aplicación'),
        ('E4','Código y al menos 300 registros','Repositorio de la solución','Esqueleto disponible; funciones y datos suficientes pendientes'),
        ('E4','Presentación PDF y video de cinco minutos máximo','Guion E3_y_E4','Guion preparado; diapositivas y video pendientes'),
        ('E4','Resumen impreso y acta por duplicado','E4/PF_AlfaConsultora_Resumen_Ejecutivo; Anexos/Acta_Entrega_Aceptacion','Resumen preparado; acta en blanco para la presentación'),
        ('Anexos','Bitácora breve de IA','Anexos/Bitacora_Uso_IA','Registro preparado; completar revisores y modificaciones humanas'),
    ]
    with (OUT/'Inventario_Entregables.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Entrega','Requisito','Ubicación','Estado']);w.writerows(rows)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    propuesta();analisis();informe();manual();resumen();bitacora();acta();guion_entrevista();guion_entregas()
    copiar_fuentes();indice()
    (OUT/'Documentos_Generados.json').write_text(json.dumps([str(p.relative_to(OUT)) for p in ARCHIVOS],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Generados',len(ARCHIVOS),'documentos editables. Falta renderizar y revisar antes de entregar.')
