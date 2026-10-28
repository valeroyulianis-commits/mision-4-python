-- Dataset de clientes para IA: una fila por cliente (Misión 3)
-- LEFT JOIN conserva los clientes sin operaciones; COUNT/SUM/AVG agregan sus operaciones.
SELECT c.id_cliente,
       c.antiguedad_meses,
       COUNT(o.id_operacion)        AS num_operaciones,
       COALESCE(SUM(o.importe), 0)  AS gasto_total,
       COALESCE(AVG(o.importe), 0)  AS ticket_medio,
       c.abandono
FROM clientes AS c
LEFT JOIN operaciones AS o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.antiguedad_meses, c.abandono
ORDER BY c.id_cliente;
