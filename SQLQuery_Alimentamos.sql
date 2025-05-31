CREATE DATABASE AlimentamosDB;
GO

USE AlimentamosDB;
GO

--tabla Ciudades
CREATE TABLE Ciudad (
    id_ciudad UNIQUEIDENTIFIER PRIMARY KEY,
	nombre VARCHAR(100),
);

-- Tabla Ruta
CREATE TABLE Ruta (
    id_ruta UNIQUEIDENTIFIER,
	id_ciudad UNIQUEIDENTIFIER,
	id_ciudadOrigen UNIQUEIDENTIFIER,
	nombre VARCHAR(100),
    fecha_apertura DATE,
    costo DECIMAL(10,2),
    fecha_cambio_costo DATE
	CONSTRAINT PK_Ruta PRIMARY KEY (id_ruta, id_ciudad),
	FOREIGN KEY (id_ciudad) REFERENCES Ciudad(id_ciudad),
	FOREIGN KEY (id_ciudadOrigen) REFERENCES Ciudad(id_ciudad)
	);

-- Tabla Proveedor
CREATE TABLE Proveedor (
    nit_proveedor VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    persona_contacto VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(200)
);

-- Tabla Producto
CREATE TABLE Producto (
    id_producto UNIQUEIDENTIFIER  PRIMARY KEY,
	nit_proveedor VARCHAR(20),
    nombre VARCHAR(100),
    descripcion VARCHAR(200),
    precio_unitario DECIMAL(10,2),
    fecha_vencimiento DATE
    FOREIGN KEY (nit_proveedor) REFERENCES Proveedor(nit_proveedor)
);

-- Tabla Conductor
CREATE TABLE Conductor (
    id_conductor UNIQUEIDENTIFIER  PRIMARY KEY,
	id_ciudad UNIQUEIDENTIFIER,
	id_ruta UNIQUEIDENTIFIER,
    nombres VARCHAR(100),
    apellidos VARCHAR(100),
    telefono VARCHAR(20),
    fecha_ingreso DATE
);

ALTER TABLE Conductor
ADD CONSTRAINT FK_Conductor_Ruta
FOREIGN KEY (id_ruta, id_ciudad)
REFERENCES Ruta(id_ruta, id_ciudad);

-- Tabla Cliente
CREATE TABLE Cliente (
    id_cliente UNIQUEIDENTIFIER,
    id_ciudad UNIQUEIDENTIFIER,
    nombre VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    CONSTRAINT PK_Cliente PRIMARY KEY (id_cliente, id_ciudad),
	FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad)
);

-- Tabla Venta
CREATE TABLE Venta (
    id_venta UNIQUEIDENTIFIER  PRIMARY KEY,
    id_cliente UNIQUEIDENTIFIER,
	id_ciudad UNIQUEIDENTIFIER,
	id_ruta UNIQUEIDENTIFIER,
    fecha_venta DATE,
    total_venta DECIMAL(10,2),
    FOREIGN KEY (id_cliente,id_ciudad) REFERENCES Cliente(id_cliente,id_ciudad),
	FOREIGN KEY (id_ruta,id_ciudad) REFERENCES ruta(id_ruta,id_ciudad)
);

-- Tabla DetalleVenta
CREATE TABLE DetalleVenta (
    id_detalle UNIQUEIDENTIFIER PRIMARY KEY,
    id_venta UNIQUEIDENTIFIER,
    id_producto UNIQUEIDENTIFIER,
    cantidad INT,
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_venta) REFERENCES Venta(id_venta),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
);

--trigger

--Trigger para Requisito vente, si la fecha de vencimiento es menor a la fecha de venta saltar error
GO
CREATE TRIGGER trg_PreventExpiredProductSale
ON DetalleVenta
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM INSERTED i
        JOIN Producto p ON i.id_producto = p.id_producto
        JOIN Venta v ON i.id_venta = v.id_venta
        WHERE p.fecha_vencimiento <= v.fecha_venta
    )
    BEGIN
        RAISERROR ('No se puede vender un producto con fecha de vencimiento menor o igual a la fecha de la venta.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Si todo está bien, se realiza la inserción
    INSERT INTO DetalleVenta (id_detalle, id_venta, id_producto, cantidad, subtotal)
    SELECT id_detalle, id_venta, id_producto, cantidad, subtotal
    FROM INSERTED;
END;
GO

--trigger para comprovar la ciudad

GO
CREATE TRIGGER trg_InsertCiudad
ON Ciudad
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Validar duplicados
    IF EXISTS (
        SELECT 1
        FROM Ciudad c
        JOIN INSERTED i ON c.nombre = i.nombre
    )
    BEGIN
        RAISERROR('Ya existe esta ciudad.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Insertar con NEWID() si no viene id_ciudad
    INSERT INTO Ciudad (id_ciudad, nombre)
    SELECT 
        ISNULL(i.id_ciudad, NEWID()), 
        i.nombre
    FROM INSERTED i;
END;
GO

GO
CREATE PROCEDURE sp_CrearRuta
    @id_ciudad UNIQUEIDENTIFIER,
    @id_ciudadOrigen UNIQUEIDENTIFIER,
    @nombre VARCHAR(100),
    @fecha_apertura DATE,
    @costo DECIMAL(10,2),
    @fecha_cambio_costo DATE,
    @id_ruta UNIQUEIDENTIFIER = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Validar existencia de ciudad destino
    IF NOT EXISTS (SELECT 1 FROM Ciudad WHERE id_ciudad = @id_ciudad)
    BEGIN
        RAISERROR('La ciudad destino no existe.', 16, 1);
        RETURN;
    END

    -- Validar existencia de ciudad origen
    IF NOT EXISTS (SELECT 1 FROM Ciudad WHERE id_ciudad = @id_ciudadOrigen)
    BEGIN
        RAISERROR('La ciudad origen no existe.', 16, 1);
        RETURN;
    END

    -- Generar ID de ruta si no se proporciona
    IF @id_ruta IS NULL
        SET @id_ruta = NEWID();

    -- Validar que no exista la ruta ya registrada
    IF EXISTS (
        SELECT 1 FROM Ruta 
        WHERE id_ruta = @id_ruta AND id_ciudad = @id_ciudad
    )
    BEGIN
        RAISERROR('Ya existe una ruta con este ID y ciudad destino.', 16, 1);
        RETURN;
    END

    -- Insertar ruta
    INSERT INTO Ruta (
        id_ruta,
        id_ciudad,
        id_ciudadOrigen,
        nombre,
        fecha_apertura,
        costo,
        fecha_cambio_costo
    )
    VALUES (
        @id_ruta,
        @id_ciudad,
        @id_ciudadOrigen,
        @nombre,
        @fecha_apertura,
        @costo,
        @fecha_cambio_costo
    );

    PRINT 'Ruta creada exitosamente.';
END;
GO


--vista ventas

GO
CREATE VIEW Vista_VentasDetalle AS
SELECT 
    v.id_venta,
    v.fecha_venta,
    v.total_venta,
    c.nombre AS nombre_cliente,
    dv.cantidad,
    dv.subtotal,
    p.nombre AS nombre_producto,
    r.nombre AS nombre_ruta,
    ciu.nombre AS nombre_ciudad_destino
FROM Venta v
INNER JOIN Cliente c
    ON v.id_cliente = c.id_cliente AND v.id_ciudad = c.id_ciudad
INNER JOIN DetalleVenta dv
    ON v.id_venta = dv.id_venta
INNER JOIN Producto p
    ON dv.id_producto = p.id_producto
INNER JOIN Ruta r
    ON v.id_ruta = r.id_ruta AND v.id_ciudad = r.id_ciudad
INNER JOIN Ciudad ciu
    ON v.id_ciudad = ciu.id_ciudad;
GO
