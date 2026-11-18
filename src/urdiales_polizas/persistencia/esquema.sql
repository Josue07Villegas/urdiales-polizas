-- Diseño SQLite propuesto. No contiene datos reales ni colores de Excel.
PRAGMA foreign_keys = ON;

CREATE TABLE asegurados (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0)
);

CREATE TABLE contactos (
    id INTEGER PRIMARY KEY,
    asegurado_id INTEGER NOT NULL REFERENCES asegurados(id),
    nombre TEXT,
    rol TEXT NOT NULL DEFAULT 'general' CHECK (rol IN ('general', 'referente'))
);

CREATE TABLE medios_contacto (
    id INTEGER PRIMARY KEY,
    contacto_id INTEGER NOT NULL REFERENCES contactos(id),
    tipo TEXT NOT NULL CHECK (tipo IN ('telefono', 'correo')),
    valor TEXT NOT NULL CHECK (length(trim(valor)) > 0),
    UNIQUE (contacto_id, tipo, valor)
);

CREATE TABLE aseguradoras (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE CHECK (length(trim(nombre)) > 0)
);

CREATE TABLE polizas (
    id INTEGER PRIMARY KEY,
    asegurado_id INTEGER NOT NULL REFERENCES asegurados(id),
    aseguradora_id INTEGER NOT NULL REFERENCES aseguradoras(id),
    tipo TEXT NOT NULL CHECK (tipo IN ('autos', 'danios')),
    estado TEXT NOT NULL DEFAULT 'en_vigor' CHECK (estado IN ('en_vigor', 'cancelada')),
    modalidad_auto TEXT CHECK (modalidad_auto IN ('individual', 'flotilla')),
    descripcion_riesgo TEXT,
    CHECK (
        (tipo = 'autos' AND modalidad_auto IS NOT NULL)
        OR (tipo = 'danios' AND modalidad_auto IS NULL)
    )
);

CREATE TRIGGER no_reactivar_cancelada
BEFORE UPDATE OF estado ON polizas
WHEN OLD.estado = 'cancelada' AND NEW.estado <> 'cancelada'
BEGIN
    SELECT RAISE(ABORT, 'Una poliza cancelada no puede reactivarse');
END;

CREATE TABLE vigencias (
    id INTEGER PRIMARY KEY,
    poliza_id INTEGER NOT NULL REFERENCES polizas(id),
    numero_poliza TEXT NOT NULL CHECK (length(trim(numero_poliza)) > 0),
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT NOT NULL,
    forma_pago TEXT NOT NULL CHECK (forma_pago IN ('mensual', 'trimestral', 'semestral', 'anual')),
    archivada INTEGER NOT NULL DEFAULT 0 CHECK (archivada IN (0, 1)),
    renueva_a_id INTEGER UNIQUE REFERENCES vigencias(id),
    CHECK (length(fecha_inicio) = 10 AND date(julianday(fecha_inicio)) IS NOT NULL
        AND date(julianday(fecha_inicio)) = fecha_inicio),
    CHECK (length(fecha_fin) = 10 AND date(julianday(fecha_fin)) IS NOT NULL
        AND date(julianday(fecha_fin)) = fecha_fin),
    CHECK (fecha_fin > fecha_inicio),
    CHECK (renueva_a_id IS NULL OR renueva_a_id <> id),
    UNIQUE (poliza_id, fecha_inicio)
);

-- Una única vigencia de trabajo por póliza; las anteriores quedan conservadas.
CREATE UNIQUE INDEX una_vigencia_de_trabajo
ON vigencias(poliza_id) WHERE archivada = 0;

CREATE TRIGGER conservar_poliza_de_vigencia
BEFORE UPDATE OF poliza_id ON vigencias
WHEN NEW.poliza_id <> OLD.poliza_id
BEGIN
    SELECT RAISE(ABORT, 'Una vigencia no puede trasladarse a otra poliza');
END;

CREATE TRIGGER validar_antecesora_insertar
BEFORE INSERT ON vigencias WHEN NEW.renueva_a_id IS NOT NULL
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM vigencias anterior
        WHERE anterior.id = NEW.renueva_a_id
          AND anterior.poliza_id = NEW.poliza_id
          AND anterior.archivada = 1
          AND NEW.fecha_inicio >= anterior.fecha_fin
    ) THEN RAISE(ABORT, 'La vigencia anterior no corresponde o no esta archivada') END;
END;

CREATE TRIGGER validar_antecesora_actualizar
BEFORE UPDATE OF renueva_a_id, poliza_id, fecha_inicio ON vigencias
WHEN NEW.renueva_a_id IS NOT NULL
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM vigencias anterior
        WHERE anterior.id = NEW.renueva_a_id
          AND anterior.poliza_id = NEW.poliza_id
          AND anterior.archivada = 1
          AND NEW.fecha_inicio >= anterior.fecha_fin
    ) THEN RAISE(ABORT, 'Relacion de renovacion invalida') END;
END;

CREATE TABLE vehiculos_asegurados (
    id INTEGER PRIMARY KEY,
    vigencia_id INTEGER NOT NULL REFERENCES vigencias(id),
    descripcion TEXT NOT NULL CHECK (length(trim(descripcion)) > 0),
    modelo INTEGER NOT NULL CHECK (modelo > 0),
    serie TEXT NOT NULL CHECK (length(trim(serie)) > 0),
    inciso TEXT,
    UNIQUE (vigencia_id, serie),
    UNIQUE (vigencia_id, inciso)
);

CREATE TRIGGER vehiculo_solo_autos_insertar
BEFORE INSERT ON vehiculos_asegurados
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.tipo = 'autos'
    ) THEN RAISE(ABORT, 'Los datos de vehiculo solo aplican a autos') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.modalidad_auto = 'individual'
          AND EXISTS (SELECT 1 FROM vehiculos_asegurados x WHERE x.vigencia_id = v.id)
    ) THEN RAISE(ABORT, 'Una poliza individual admite un vehiculo') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.modalidad_auto = 'flotilla'
          AND (NEW.inciso IS NULL OR length(trim(NEW.inciso)) = 0)
    ) THEN RAISE(ABORT, 'La flotilla requiere un inciso') END;
END;

CREATE TRIGGER vehiculo_solo_autos_actualizar
BEFORE UPDATE ON vehiculos_asegurados
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.tipo = 'autos'
    ) THEN RAISE(ABORT, 'Los datos de vehiculo solo aplican a autos') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.modalidad_auto = 'individual'
          AND EXISTS (SELECT 1 FROM vehiculos_asegurados x
                      WHERE x.vigencia_id = v.id AND x.id <> NEW.id)
    ) THEN RAISE(ABORT, 'Una poliza individual admite un vehiculo') END;
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM vigencias v JOIN polizas p ON p.id = v.poliza_id
        WHERE v.id = NEW.vigencia_id AND p.modalidad_auto = 'flotilla'
          AND (NEW.inciso IS NULL OR length(trim(NEW.inciso)) = 0)
    ) THEN RAISE(ABORT, 'La flotilla requiere un inciso') END;
END;

-- El tipo y modalidad de una póliza se conservan al cambiar de vigencia.
CREATE TRIGGER conservar_tipo_poliza
BEFORE UPDATE OF tipo, modalidad_auto ON polizas
WHEN (NEW.tipo <> OLD.tipo OR NEW.modalidad_auto IS NOT OLD.modalidad_auto)
 AND EXISTS (SELECT 1 FROM vigencias WHERE poliza_id = OLD.id)
BEGIN
    SELECT RAISE(ABORT, 'El tipo de una poliza con vigencias no puede cambiar');
END;

CREATE TABLE cobros (
    id INTEGER PRIMARY KEY,
    vigencia_id INTEGER NOT NULL REFERENCES vigencias(id),
    fecha_vencimiento TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'pagado')),
    CHECK (length(fecha_vencimiento) = 10
        AND date(julianday(fecha_vencimiento)) IS NOT NULL
        AND date(julianday(fecha_vencimiento)) = fecha_vencimiento),
    UNIQUE (vigencia_id, fecha_vencimiento)
);

CREATE INDEX buscar_asegurado ON asegurados(nombre COLLATE NOCASE);
CREATE INDEX buscar_numero ON vigencias(numero_poliza);
CREATE INDEX buscar_fin ON vigencias(fecha_fin);
CREATE INDEX buscar_cobro ON cobros(estado, fecha_vencimiento);

-- El histórico se obtiene por fecha o por renovación; no necesita un proceso en segundo plano.
-- Una fecha vencida no transforma automáticamente la póliza en cancelada.
