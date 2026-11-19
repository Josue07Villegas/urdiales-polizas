"""Contenido común de los entregables académicos; versión de trabajo del equipo."""

FECHA = '19 de noviembre de 2026'
EQUIPO = [
    ('Josue Abel Villegas Garcia', '747198'),
    ('Scarlett Alvarado Urdiales', '738933'),
    ('Emiliano Ramirez Gonzalez', '736987'),
    ('David Alejandro Carrillo Cázares', '738586'),
]
CONTEXTO = (
    'Urdiales Asesores comercializa seguros de distintas aseguradoras. El personal organiza los '
    'registros de asegurados y pólizas en un archivo de Excel con tres pestañas y utiliza Google '
    'Calendar para consultar fechas de renovación y cobranza. José Urdiales Pérez es el dueño '
    'de la empresa y Aurora fue identificada como usuaria principal de la solución.'
)
PROBLEMA = (
    'La búsqueda y combinación de información por asegurado, aseguradora y fechas exige revisar '
    'controles separados. Esto consume tiempo al localizar pólizas y reconocer próximas renovaciones '
    'o cobros. El impacto descrito es operativo; todavía no se ha medido una duración promedio de '
    'búsqueda ni un costo económico. La necesidad prioritaria es centralizar y consultar los datos.'
)
OBJETIVO = (
    'Desarrollar una aplicación local en Python que centralice asegurados, contactos y pólizas de '
    'autos y daños, permita consultar y editar registros con filtros combinables y facilite revisar '
    'fechas próximas, conservando las vigencias anteriores y vencidas en un histórico.'
)
OBJETIVOS = [
    'Estructurar los datos de asegurados, contactos, pólizas, vigencias, vehículos y cobros con relaciones consistentes.',
    'Facilitar búsquedas combinadas y mostrar las fechas más próximas primero.',
    'Conservar los periodos anteriores al registrar una renovación y separar el histórico de la cartera actual.',
    'Identificar atención por fechas con 30 días de anticipación en los casos que valide la empresa.',
    'Aplicar y justificar los seis paradigmas exigidos por la actividad, con evidencia del código real.',
]
ALCANCE = (
    'Registro y edición de asegurados y contactos opcionales; pólizas de autos y daños; vehículos '
    'individuales e incisos de flotilla; vigencias y formas de pago; consulta principal e histórico; '
    'filtros combinables por asegurado, aseguradora, fechas y renovación o cobranza; orden por '
    'proximidad; estados manuales de cobranza y atención visual basada en fechas.'
)
EXCLUSIONES = (
    'Quedan fuera la generación de cotizaciones, el envío de mensajes y comunicaciones desde el '
    'sistema, campañas, tableros, gráficas de crecimiento, reportes comerciales, importación de Excel '
    'desde la interfaz, exportación a Excel y funciones de respaldo o restauración de la base de datos.'
)
ACLARACION = (
    'La guía académica exige carga y limpieza CSV o Excel, al menos tres reportes o indicadores '
    'útiles y un motor lógico consultable desde la interfaz. Debe conciliarse cómo cumplir esa '
    'evidencia con el alcance comercial acotado. No existe una excepción aprobada ni se afirma que '
    'esas funciones estén implementadas. La carga de demostración puede proponerse separada de '
    'la interfaz, sujeta a revisión con el docente.'
)
ACTUAL = [
    'Después de la emisión de una póliza se registran sus datos en Excel.',
    'Las fechas de renovación y cobranza se organizan en Google Calendar a partir del control existente.',
    'El personal busca al asegurado, la compañía y las fechas para preparar el trabajo previo correspondiente.',
    'Al avanzar o completar la actividad se actualizan las marcas del registro actual.',
]
MARCAS = (
    'En el proceso actual R indica renovación y C cobranza. Rojo significa que aún no se trabaja, '
    'verde que ya se trabajó y la tacha que se completó. El asterisco resalta la importancia de la '
    'renovación anual. Son convenciones del control actual; los requerimientos nuevos usan datos, '
    'fechas, vigencias y estados de cobro y no obligan a reproducir esas marcas.'
)
PROPUESTO = [
    'Abrir la cartera actual y, si se requiere, combinar filtros.',
    'Recuperar los registros relacionados y calcular las próximas fechas de atención.',
    'Presentar resultados ordenados de la fecha más próxima a la más lejana.',
    'Capturar o editar datos válidos, actualizar un cobro o registrar una nueva vigencia.',
    'Guardar los cambios de forma consistente y conservar el periodo anterior cuando se renueva.',
]
RNF = [
    ('RNF-01', 'Persistencia', 'M', 'Los registros y cambios confirmados permanecen después de cerrar y volver a abrir la aplicación.'),
    ('RNF-02', 'Integridad', 'M', 'Se rechazan fechas inexistentes, relaciones inválidas y campos obligatorios vacíos sin guardar cambios parciales; los opcionales admiten ausencia.'),
    ('RNF-03', 'Usabilidad', 'M', 'Aurora puede registrar, consultar y editar mediante etiquetas claras y mensajes comprensibles; cualquier color se acompaña de texto.'),
    ('RNF-04', 'Instalación local', 'M', 'La solución se ejecuta en otro equipo siguiendo el README en no más de cinco pasos; sistema operativo y equipo definitivo por confirmar.'),
    ('RNF-05', 'Datos de demostración', 'M', 'La demostración utiliza datos sintéticos o anonimizados y los archivos de clientes reales no se publican en el repositorio.'),
]
REGLAS = [
    ('RB-01', 'Si un asegurado tiene varias pólizas, entonces cada una conserva su aseguradora, datos y vigencias vinculados al mismo titular.'),
    ('RB-02', 'Si se registra una nueva vigencia, entonces se conserva la anterior en el histórico y la escritura se confirma completa o se revierte.'),
    ('RB-03', 'Si una vigencia está vencida o archivada por renovación, entonces se consulta fuera de la cartera principal.'),
    ('RB-04', 'Si el caso está sujeto a anticipación y su fecha está dentro de los próximos 30 días, entonces requiere atención visual; aplicabilidad y calendario por validar.'),
    ('RB-05', 'Si una póliza se cancela, entonces se impide reactivarla según la regla recabada; confirmar su aplicación antes de cerrar la validación.'),
]
REGLAS_LOGICAS = [
    ('RL-01', 'Si una vigencia está vencida o archivada, entonces corresponde a la consulta del histórico.'),
    ('RL-02', 'Si una póliza está en vigor, aplica anticipación y faltan de 0 a 30 días para renovar, entonces requiere atención por renovación.'),
    ('RL-03', 'Si un cobro está pendiente, aplica anticipación y faltan de 0 a 30 días para cobrar, entonces requiere atención por cobranza.'),
]
DATOS = [
    ('Asegurado', 'Nombre y relación con varias pólizas.', 'Texto y clave interna. No confundir el nombre con una clave única.'),
    ('Contacto', 'Nombre, teléfonos, correos y datos del referente, si existen.', 'Texto; varios medios opcionales. Ubicación y rol por validar.'),
    ('Aseguradora', 'Compañía que emite la póliza.', 'Catálogo de nombres por confirmar; no operación bancaria.'),
    ('Póliza', 'Asegurado, aseguradora, tipo autos o daños y estado administrativo.', 'Número alfanumérico conservado por vigencia si cambia al renovar.'),
    ('Vigencia', 'Número, fecha de inicio y fin, año, forma de pago y relación con la anterior.', 'Fechas completas; pago mensual, trimestral, semestral o anual.'),
    ('Vehículo', 'Descripción, modelo y serie.', 'Modelo entero; serie alfanumérica como texto; solo para autos.'),
    ('Flotilla', 'Póliza matriz e incisos de vehículos como -1 y -2.', 'Varios vehículos por vigencia; datos compartidos por validar.'),
    ('Daños', 'Descripción del bien o riesgo asegurado y datos generales de póliza.', 'Sin campos obligatorios de vehículo, modelo o serie.'),
    ('Cobro', 'Fecha de vencimiento y estado pendiente o pagado.', 'Se captura o actualiza manualmente; no procesa pagos.'),
    ('Atención', 'Próxima fecha y motivo de atención.', 'Resultado derivado de las fechas; no es un mensaje enviado al cliente.'),
]
HISTORIAS = [
    ('HU-01', 'Como Aurora quiero registrar un asegurado y sus contactos para consultar su información desde un solo lugar.', 'RF-01, RF-03', [
        ('Dado un asegurado nuevo con nombre válido y contactos disponibles', 'cuando guardo su ficha', 'entonces puedo recuperarla con sus medios de contacto asociados.'),
        ('Dado un asegurado sin teléfono ni correo', 'cuando guardo los datos obligatorios válidos', 'entonces el registro se conserva sin inventar medios de contacto.'),
    ]),
    ('HU-02', 'Como Aurora quiero vincular varias pólizas a un asegurado para distinguir sus seguros y vehículos.', 'RF-04, RF-05', [
        ('Dado un asegurado existente', 'cuando registro una póliza de autos y otra de daños', 'entonces ambas conservan sus datos específicos bajo el mismo titular.'),
        ('Dada una póliza de flotilla con incisos -1 y -2', 'cuando consulto sus unidades', 'entonces identifico cada vehículo por su inciso y serie sin mezclarlos.'),
    ]),
    ('HU-03', 'Como Aurora quiero combinar filtros para localizar los registros que necesito.', 'RF-06, RF-07', [
        ('Dados registros de dos asegurados y dos compañías', 'cuando filtro por asegurado y compañía simultáneamente', 'entonces aparecen únicamente coincidencias de ambos criterios, con las fechas próximas primero.'),
        ('Dada una combinación sin coincidencias', 'cuando la aplico', 'entonces se informa que no hay resultados y puedo limpiar los filtros.'),
    ]),
    ('HU-04', 'Como Aurora quiero reconocer fechas próximas para revisar renovaciones y cobranza con anticipación.', 'RF-06, RF-10', [
        ('Dado el 17 de noviembre de 2026 y casos aplicables al plazo de 30 días', 'cuando consulto fechas del 16 y 18 de diciembre de 2026', 'entonces se resalta la del día 16, a 29 días, y no la del día 18, a 31 días.'),
        ('Dado un caso señalado para atención', 'cuando reviso la lista', 'entonces puedo leer la fecha y el motivo aunque no distinga un color.'),
    ]),
    ('HU-05', 'Como Aurora quiero registrar renovaciones y actualizar cobros para mantener los periodos y estados al día.', 'RF-08, RF-09', [
        ('Dada una póliza con una vigencia de trabajo', 'cuando registro una renovación válida', 'entonces la nueva vigencia queda actual y la anterior se conserva en histórico.'),
        ('Dado un cobro pendiente', 'cuando lo marco pagado', 'entonces cambia ese cobro sin alterar otros cobros ni las fechas contractuales de la póliza.'),
    ]),
    ('HU-06', 'Como Aurora quiero corregir datos guardados para mantener fichas confiables.', 'RF-02, RF-04, RF-11; RNF-01, RNF-02', [
        ('Dada una ficha existente', 'cuando corrijo y guardo un dato válido y reabro la aplicación', 'entonces recupero el cambio y sus relaciones.'),
        ('Dada una póliza cancelada y confirmada la regla de no reactivación', 'cuando intento cambiarla a en vigor', 'entonces se rechaza el cambio con un mensaje comprensible.'),
    ]),
]
ESCENARIOS = [
    ('EA-01', 'Filtros combinables', 'HU-03; RF-06, RF-07',
     'Cliente Ficticio A con aseguradoras Demo A y Demo B; Cliente Ficticio B con Demo A. Fechas de A/Demo A: 22 y 28 de noviembre de 2026.',
     'Filtrar Cliente Ficticio A y Demo A.',
     'Solo aparecen sus dos registros de Demo A, en orden 22/11 y 28/11; se excluyen A/Demo B y B/Demo A.'),
    ('EA-02', 'Atención por fechas', 'HU-04; RF-10',
     'Fecha de referencia 17/11/2026; tres casos aplicables vencen 17/11, 16/12 y 18/12; diferencia de 0, 29 y 31 días.',
     'Consultar la atención con anticipación de 30 días.',
     'Se identifican los casos de 0 y 29 días, con texto del motivo; el de 31 días no se resalta. La prueba no presupone ajuste por inhábiles.'),
    ('EA-03', 'Relaciones entre entidades', 'HU-01, HU-02; RF-01, RF-03, RF-04, RF-05',
     'Un asegurado con póliza de daños y flotilla F-DEMO. La flotilla tiene incisos -1/SERIE-DEMO-1 y -2/SERIE-DEMO-2.',
     'Consultar ambas pólizas y las unidades de la flotilla.',
     'Las pólizas se relacionan con el mismo asegurado y cada inciso conserva su serie; daños no exige datos de vehículo.'),
    ('EA-04', 'Edición y renovación', 'HU-05, HU-06; RF-02, RF-08, RF-09, RF-11',
     'Póliza P-DEMO con vigencia 10/12/2025 a 10/12/2026, un cobro pendiente y una ficha editable.',
     'Editar un dato, marcar el cobro pagado y renovar a 10/12/2026–10/12/2027. Después intentar una renovación con fin anterior al inicio.',
     'Persisten edición y cobro; se conserva la vigencia anterior y solo una nueva vigente. El intento inválido no deja cambios parciales. Verificar cancelación por separado al validar su regla.'),
    ('EA-05', 'Persistencia', 'HU-01, HU-06; RNF-01',
     'Guardar Cliente Ficticio C, dos contactos y una póliza; editar un teléfono como texto +52 00 0000 0000.',
     'Cerrar y abrir la aplicación y recuperar la ficha.',
     'Se conservan el teléfono, la póliza y sus relaciones, sin duplicados introducidos por la reapertura.'),
]
PENDIENTES = [
    ('P-01', 'Empresa y equipo', 'Aplicabilidad de los 30 días y calendario de días inhábiles; conservar fecha contractual.'),
    ('P-02', 'Empresa y equipo', 'Relación de contactos y referentes, campos compartidos de flotilla y catálogo de aseguradoras.'),
    ('P-03', 'Empresa y equipo', 'Canceladas en histórico, edición de periodos anteriores y aplicación de la regla de no reactivación.'),
    ('P-04', 'Equipo', 'Medir una búsqueda real, confirmar equipo y sistema operativo y acordar la sesión de validación.'),
    ('P-05', 'Empresa', 'Revisar y firmar carta y minuta o confirmar por un medio aceptado por la guía.'),
    ('P-06', 'Docente y equipo', 'Conciliar carga/limpieza, tres indicadores y módulo lógico con el alcance; no hay dispensa aprobada.'),
    ('P-07', 'Equipo y empresa', 'Construir y revisar al menos 300 registros realistas de muestra; todavía no están disponibles.'),
]
PARADIGMAS = [
    ('Imperativo', 'datos/carga_demo.py', 'Cargar y limpiar datos de muestra paso a paso con contadores y lista de errores.', 'Pendiente de implementar y conciliar la carga académica.'),
    ('Estructurado', '__main__.py; aplicacion/servicios.py; interfaz/', 'Coordinar el flujo con funciones de responsabilidad clara, secuencia, selección e iteración.', 'Arranque disponible; casos de uso pendientes.'),
    ('Orientado a objetos', 'dominio/clientes.py, polizas.py, cobros.py', 'Representar asegurados, pólizas especializadas, vigencias y cobros mediante entidades.', 'Entidades e implementación de herencia pendientes.'),
    ('Declarativo', 'persistencia/esquema.sql; configuracion.py', 'Definir relaciones y restricciones en SQL y separar parámetros mediante TOML.', 'Esquema y lectura TOML disponibles; consultas de negocio por conectar.'),
    ('Funcional', 'consultas/transformaciones.py', 'Clasificar, filtrar y ordenar mediante funciones puras y composición; indicadores académicos por conciliar.', 'Pendiente de implementar.'),
    ('Lógico', 'reglas/atencion.py', 'Consultar hechos y reglas de atención por fechas con kanren o sympy.logic.', 'Motor, hechos, reglas y consultas pendientes.'),
]
DIAGRAMAS = [
    ('01_actividad_actual', 'Proceso actual', False),
    ('02_actividad_propuesta', 'Proceso propuesto', False),
    ('03_casos_uso', 'Casos de uso del sistema', True),
    ('04_clases_polizas', 'Clases del dominio de pólizas', True),
    ('05_clases_detalle', 'Clases de contactos vehículos y cobros', True),
    ('06_modelo_relacional', 'Modelo relacional propuesto', False),
    ('07_secuencia_consulta', 'Secuencia de consulta y filtros', True),
    ('08_secuencia_renovacion', 'Secuencia de renovación con histórico', True),
    ('09_componentes', 'Componentes y paradigmas propuestos', True),
    ('10_boceto_cartera', 'Boceto de la cartera', True),
]
REFERENCIAS = [
    ('Kowalski, R. A. (1974). Predicate logic as programming language. En Information Processing 74 (pp. 569–574). North-Holland.', 'https://www.doc.ic.ac.uk/~rak/papers/IFIP74.pdf'),
    ('Python Software Foundation. (s. f.-a). abc — Abstract base classes. Python 3.11 documentation.', 'https://docs.python.org/3.11/library/abc.html'),
    ('Python Software Foundation. (s. f.-b). dataclasses — Data classes. Python 3.11 documentation.', 'https://docs.python.org/3.11/library/dataclasses.html'),
    ('Python Software Foundation. (s. f.-c). sqlite3 — DB-API 2.0 interface for SQLite databases. Python 3.11 documentation.', 'https://docs.python.org/3.11/library/sqlite3.html'),
    ('Python Software Foundation. (s. f.-d). tomllib — Parse TOML files. Python 3.11 documentation.', 'https://docs.python.org/3.11/library/tomllib.html'),
    ('Van Roy, P. (2009). Programming paradigms for dummies: What every programmer should know. En G. Assayag y A. Gerzso (Eds.), New computational paradigms for computer music (pp. 9–47). IRCAM/Delatour France.', 'https://webperso.info.ucl.ac.be/~pvr/VanRoyChapter.pdf'),
]
