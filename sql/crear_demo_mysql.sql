-- Datos sintéticos para docencia. No modifica ai_customer (Misión 3).
-- Ejecuta este archivo una sola vez en MySQL Workbench.
-- Si la base demo ya contiene estas tablas, la creación se detiene: no borres tu trabajo.
CREATE DATABASE IF NOT EXISTS ai_customer_m4_demo CHARACTER SET utf8mb4;
USE ai_customer_m4_demo;
CREATE TABLE clientes (
 id_cliente INT PRIMARY KEY, nombre VARCHAR(80) NOT NULL, ciudad VARCHAR(80),
 antiguedad_meses INT NOT NULL, abandono INT NOT NULL
);
CREATE TABLE operaciones (
 id_operacion INT PRIMARY KEY, id_cliente INT NOT NULL, fecha DATE NOT NULL,
 importe DECIMAL(10,2), canal VARCHAR(20),
 FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
INSERT INTO clientes VALUES
(101, 'Cliente 101', 'Madrid', 12, 0),
(102, 'Cliente 102', 'Sevilla', 4, 1),
(103, 'Cliente 103', 'Valencia', 24, 0),
(104, 'Cliente 104', 'Madrid', 2, 1),
(105, 'Cliente 105', 'Sevilla', 36, 0),
(106, 'Cliente 106', 'Valencia', 8, 1),
(107, 'Cliente 107', 'Madrid', 18, 0),
(108, 'Cliente 108', 'Sevilla', 6, 1),
(109, 'Cliente 109', 'Valencia', 30, 0),
(110, 'Cliente 110', 'Madrid', 10, 1),
(111, 'Cliente 111', 'Sevilla', 15, 0),
(112, 'Cliente 112', 'Valencia', 3, 1);
INSERT INTO operaciones VALUES
(1, 101, '2026-09-01', 60, 'web'),
(2, 101, '2026-09-02', 60, 'tienda'),
(3, 101, '2026-09-03', 60, 'web'),
(4, 102, '2026-09-01', 30, 'web'),
(5, 103, '2026-09-01', 120, 'web'),
(6, 103, '2026-09-02', 120, 'tienda'),
(7, 105, '2026-09-01', 100, 'web'),
(8, 105, '2026-09-02', 100, 'tienda'),
(9, 105, '2026-09-03', 100, 'web'),
(10, 105, '2026-09-04', 100, 'tienda'),
(11, 106, '2026-09-01', 30, 'web'),
(12, 106, '2026-09-02', 30, 'tienda'),
(13, 108, '2026-09-01', 45, 'web'),
(14, 109, '2026-09-01', 90, 'web'),
(15, 109, '2026-09-02', 90, 'tienda'),
(16, 109, '2026-09-03', 90, 'web'),
(17, 110, '2026-09-01', 50, 'web'),
(18, 110, '2026-09-02', 50, 'tienda'),
(19, 111, '2026-09-01', 80, 'web');
