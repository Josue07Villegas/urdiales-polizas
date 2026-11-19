# Alcance de la solución

## Contexto

Urdiales Asesores comercializa seguros de diferentes aseguradoras. Actualmente utiliza un archivo de Excel y un calendario para organizar clientes, pólizas, renovaciones y cobranza. La búsqueda y el filtrado de información consumen tiempo.

El equipo Alfa Consultora propone una aplicación local pequeña para centralizar esos registros. En este contexto, seguimiento significa conservar y consultar datos, fechas y estados; las comunicaciones con el cliente continúan fuera del sistema.

## Funciones previstas

- Registrar y editar asegurados, contactos y medios de contacto opcionales.
- Relacionar un asegurado con varias pólizas de autos o daños.
- Representar vehículos individuales y los incisos de flotillas según el diseño por validar.
- Conservar número de póliza, vigencia y forma de pago por periodo.
- Consultar cartera e histórico por separado.
- Combinar filtros por asegurado, aseguradora, fechas y renovación o cobranza.
- Mostrar las fechas más próximas primero.
- Resaltar casos que requieran atención, con una anticipación acordada de 30 días y aplicabilidad por validar.
- Registrar manualmente el estado de un cobro y la nueva vigencia de una renovación.

## Criterios que guían el diseño

- Pólizas, series de vehículos y teléfonos se almacenan como texto.
- Daños comparte los datos generales de una póliza y tiene descripción del riesgo; los datos de vehículo corresponden a autos.
- La nueva vigencia conserva la anterior en histórico. Las vigencias vencidas quedan fuera de la consulta principal.
- Se conservan fechas contractuales. Un ajuste por día inhábil debe afectar la atención interna, según la regla pendiente de validar.
- Vencimiento y cancelación son conceptos diferentes. No se presupone una cancelación automática ni una regla legal validada.
- R, C, colores, tachas y asteriscos documentan el proceso actual; no obligan a reproducir sus marcas como estados del sistema nuevo.

## Exclusiones del alcance comercial

- Contactar clientes, enviar correos o mensajes y administrar campañas.
- Generar cotizaciones o comparar precios de aseguradoras.
- Crear tableros, gráficas de crecimiento o reportes comerciales.
- Importar archivos de Excel desde la interfaz del usuario.
- Exportar registros a Excel.
- Respaldar y restaurar la base de datos desde el sistema.

Se conservan RF-01 a RF-11 y cinco RNF; no se requiere una función adicional para alcanzar el mínimo académico. Los requisitos académicos de carga de datos e indicadores se deben conciliar con el docente; consulta [entregables y paradigmas](entregables.md).

La priorización propuesta es ocho RF Must y tres Should (RF-03, RF-09 y RF-11). Se prevé completar ambos grupos; Should establece una secuencia y no elimina compromisos de alcance. OP-01 Could es el uso opcional de colores por aseguradora acompañados de texto. Las exclusiones anteriores se identifican como EX-01 a EX-06 Won’t de esta versión. Debe validarse esta priorización con la empresa.

## Estado de esta base

Se puede comprobar la configuración, inicializar una base SQLite vacía y abrir una ventana inicial. Las funciones previstas de captura, filtros, renovación, histórico y avisos todavía no están conectadas ni implementadas como casos de uso.
