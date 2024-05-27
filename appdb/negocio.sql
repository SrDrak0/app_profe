CREATE DATABASE negocio;
USE negocio;

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio INT(10) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);
CREATE TABLE compras (
    id_compra INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    fecha_compra DATE NOT NULL,
    total INT(10) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE compras_productos (
    id_compra INT,
    id_producto INT,
    cantidad INT NOT NULL,
    precio_unitario INT(10) NOT NULL,
    PRIMARY KEY (id_compra, id_producto),
    FOREIGN KEY (id_compra) REFERENCES compras(id_compra),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

INSERT INTO productos (nombre, precio, stock) VALUES
('Manzana', 2500, 100),
('Leche', 5000, 50),
('Pan', 4000, 30),
('Huevos', 12000, 60),
('Arroz', 5000, 80),
('Pasta', 6000, 40),
('Azucar', 4500, 70),
('Sal', 3000, 90),
('Cafe', 15000, 25),
('Te', 10000, 20),
('Jugo de Naranja', 6000, 35),
('Carne de Res', 35000, 20),
('Pollo', 20000, 25),
('Pescado', 30000, 15),
('Queso', 20000, 30);
