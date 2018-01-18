CREATE TABLE afiliados (
	legajo int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    dni int(8) UNSIGNED UNIQUE KEY,
    tipo_afiliado varchar(20) ,
    cuil int(11) UNSIGNED UNIQUE KEY,
    apellido varchar(40),
    nombre varchar(40),
    fecha_nacimiento date,
    edad int(2),
    estado_civil varchar(20),
    nacionalidad varchar(20),
    
    calle varchar(80),
    altura int(8),
    piso varchar(10),
    depto varchar(4),
    cod_postal varchar(20),
    barrio varchar(30),
    localidad varchar(50),
    
    telefono int(13),
    celular int(16),
    email varchar(80)
    
);

CREATE TABLE familiares(
	dni int(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    relacion varchar(40),
    nombre varchar(40),
    apellido varchar(40),
    fecha_nacimiento date,
    edad int(2),
    nivel_estudios varchar(20),
    
    legajo_afiliado int(16) UNSIGNED NOT NULL
);

CREATE TABLE servicios(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(20)
);

CREATE TABLE servicios_afiliado(
	id_servicio int(16) UNSIGNED NOT NULL,
    legajo_afiliado int(16) UNSIGNED NOT NULL,
    
    fecha date,
    cantidad int(20),
    detalle varchar(80),
    
    PRIMARY KEY (id_servicio, legajo_afiliado),
	CONSTRAINT `constr_servicio_fk`
		FOREIGN KEY `servicio_fk` (`id_servicio`) REFERENCES `servicios` (`id`)
		ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `constr_afiliado_fk`
        FOREIGN KEY `afiliado_fk` (`afiliado`) REFERENCES `afiliados` (`legajo`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE debitos(  
    legajo_afiliado int(16) UNSIGNED NOT NULL,
    banco int(16) UNSIGNED NOT NULL,
    
    sucursal varchar(30),
    cbu varchar(30)    

);

CREATE TABLE bancos(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(20)
);

CREATE TABLE descuentos(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE proveedores(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    nombre varchar(40),
    servicios varchar(100),
    direccion varchar(80),
    altura int(8),
    telefono int(16),
    celular int(16),
    email varchar(80),

    
    cuit int(11) UNSIGNED UNIQUE KEY,
    razon_social varchar(60),
    cbu varchar(30),
    banco int(16) UNSIGNED NOT NULL,
    cuenta int(16),
    comision varchar(40),
    responsable varchar(40),
    forma_pago varchar(40)   
    
);

CREATE TABLE usuarios(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    nombre varchar(40),
    apellido varchar(40),
    
    legajo int(16) UNSIGNED NOT NULL UNIQUE KEY
);