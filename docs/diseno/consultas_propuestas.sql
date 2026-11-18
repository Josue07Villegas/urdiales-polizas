-- Parámetros de aplicación. Las consultas son diseño; no una interfaz implementada.
-- :hoy fecha ISO, :asegurado texto o '', :aseguradora_id entero o NULL,
-- :tipo todos/renovacion/cobranza, :desde y :hasta fecha ISO o NULL.

-- 1. Cartera y filtros combinados. Una fila por vigencia actual.
WITH siguiente_cobro AS (
    SELECT vigencia_id, MIN(fecha_vencimiento) AS fecha_cobro
    FROM cobros WHERE estado = 'pendiente' GROUP BY vigencia_id
), base AS (
    SELECT v.id, a.nombre AS asegurado, s.nombre AS aseguradora,
           p.aseguradora_id, p.tipo AS tipo_seguro, v.numero_poliza,
           v.fecha_fin AS fecha_renovacion, c.fecha_cobro,
           CASE WHEN :tipo = 'renovacion' THEN v.fecha_fin
                WHEN :tipo = 'cobranza' THEN c.fecha_cobro
                WHEN c.fecha_cobro IS NULL THEN v.fecha_fin
                ELSE MIN(v.fecha_fin, c.fecha_cobro) END AS fecha_orden
    FROM vigencias v
    JOIN polizas p ON p.id = v.poliza_id
    JOIN asegurados a ON a.id = p.asegurado_id
    JOIN aseguradoras s ON s.id = p.aseguradora_id
    LEFT JOIN siguiente_cobro c ON c.vigencia_id = v.id
    WHERE v.archivada = 0 AND v.fecha_fin >= :hoy AND p.estado = 'en_vigor'
)
SELECT * FROM base
WHERE (:asegurado = '' OR instr(lower(asegurado), lower(:asegurado)) > 0)
  AND (:aseguradora_id IS NULL OR aseguradora_id = :aseguradora_id)
  AND fecha_orden IS NOT NULL
  AND (:desde IS NULL OR fecha_orden >= :desde)
  AND (:hasta IS NULL OR fecha_orden <= :hasta)
ORDER BY fecha_orden ASC, asegurado ASC, id ASC;

-- 2. Histórico: se conservan vigencias anteriores, vencidas y canceladas.
-- La ubicación de canceladas en histórico es propuesta para validar.
SELECT v.*, a.nombre AS asegurado, p.estado
FROM vigencias v
JOIN polizas p ON p.id = v.poliza_id
JOIN asegurados a ON a.id = p.asegurado_id
WHERE v.archivada = 1 OR v.fecha_fin < :hoy OR p.estado = 'cancelada'
ORDER BY v.fecha_fin DESC, v.id DESC;

-- 3. Detalle de contactos y medios opcionales.
SELECT c.id, c.nombre, c.rol, m.tipo, m.valor
FROM contactos c
LEFT JOIN medios_contacto m ON m.contacto_id = c.id
WHERE c.asegurado_id = :asegurado_id ORDER BY c.id, m.id;

-- 4. Consulta técnica de comprobación de relaciones; no se añade un reporte a la UI.
SELECT p.id, COUNT(DISTINCT v.id) AS vigencias, COUNT(DISTINCT x.id) AS vehiculos
FROM polizas p
LEFT JOIN vigencias v ON v.poliza_id = p.id
LEFT JOIN vehiculos_asegurados x ON x.vigencia_id = v.id
GROUP BY p.id;
