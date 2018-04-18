use sindicato;

CREATE TABLE afiliados (
	legajo varchar(22) UNSIGNED NOT NULL PRIMARY KEY, # El legajo deberia ser un entero de 8 y no deberia permitir poner signos. Formato: 01002595
    dni varchar(8) UNSIGNED UNIQUE KEY,
    tipo_afiliado varchar(20) ,
		activo smallint(1),
    cuil varchar(11) UNSIGNED UNIQUE KEY,
    apellido varchar(50), # Podemos poner 10 mas? por las dudas!! no recuerdo bien, pero creo que hay gente con doble apellido y largos encima. Por ejemplo: Lagos fuentealba Cristian Juan Jose
    nombre varchar(50), # Podemos poner 10 mas? por las dudas!! no recuerdo bien, pero creo que hay gente con doble apellido y largos encima. Por ejemplo: Lagos fuentealba Cristian Juan Jose
    fecha_nacimiento date,
    edad int(3),
    estado_civil varchar(20),
    nacionalidad varchar(20),
    calle varchar(80),
    altura varchar(8),
    piso varchar(10),
    depto varchar(4),
    cod_postal varchar(20), # Aca con un largo de 4 esta bien.
    barrio varchar(30),
    localidad varchar(50),
	telefono_particular varchar(20),  # El telefono deberia ser un varchar porque suele tener este formato: (0220)482-8844
	telefono_laboral varchar(20),  # El telefono deberia ser un varchar porque suele tener este formato: (0220)482-8844
    celular varchar(20), # El celular deberia ser un varchar porque suele tener este formato: 11-6030-0122
    email varchar(80),
	lugar_trabajo varchar(40),
	jerarquia varchar(40),
	fecha_ingreso date,
	antiguedad int(2),
	nivel_estudios varchar(40),
	id_banco int(8),
    sucursal varchar(32),
	cbu varchar(22)
);

CREATE TABLE familiares(
	dni int(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    relacion varchar(40),
    nombre varchar(50),  # idem nombre afiliado
    apellido varchar(50), # idem apellido afiliado
    fecha_nacimiento date,
    edad int(2),
    nivel_estudios varchar(40),
    legajo_afiliado int(8) UNSIGNED NOT NULL,  # El legajo deberia ser un entero de 8 y no deberia permitir poner signos. Formato: 01002595


    CONSTRAINT `constr_familiar_fk`
		FOREIGN KEY `familiar_fk` (`legajo_afiliado`) REFERENCES `afiliados` (`legajo`)
		ON DELETE CASCADE ON UPDATE CASCADE
    #Crear clave foránea
);

CREATE TABLE servicios(
	id int(16) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50)
    # Falta el detalle del Proveedor creo?? Es un detalle en el que va a ir:  Direccion y Numero de telefono. Todo en una solo linea.. es decir un texto plano a modo informativo
);

CREATE TABLE servicios_afiliado(
	id_servicio int(8) UNSIGNED NOT NULL,
    legajo_afiliado int(8) UNSIGNED NOT NULL,
    fecha date,
    cantidad int(20),
    detalle varchar(80),

    PRIMARY KEY (id_servicio, legajo_afiliado),
	CONSTRAINT `constr_servicio_fk`
		FOREIGN KEY `servicio_fk` (`id_servicio`) REFERENCES `servicios` (`id`)
		ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT `constr_afiliado_fk`
        FOREIGN KEY `afiliado_fk` (`legajo_afiliado`) REFERENCES `afiliados` (`legajo`)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE debitos(
    id int UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    legajo_afiliado varchar(22) UNSIGNED NOT NULL,
    fecha_descuento date, # (Mes de descuento)
		fecha_carga_inicial date, # FIJARSE SI FUNCIONA

    proveedor_id int(8) UNSIGNED NOT NULL,
    cuota_actual int(2),
    total_cuotas int(2),
		importe_actual decimal(8,2),
		importe_total decimal(8,2),
		n_credito varchar(22)

);

CREATE TABLE bancos(
	id int(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(20)
);

CREATE TABLE proveedores(
	id int(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50),
    servicios varchar(100),
    calle varchar(80),
    altura int(8) DEFAULT NULL,
    localidad varchar(50),
		telefono varchar(20),
    celular varchar(20),
    email varchar(80),
    cuit varchar(11) UNSIGNED UNIQUE KEY,
    razon_social varchar(60),
    cbu varchar(22), #solo un largo de 22. El CBU contiene 22 numeros y deberia poderse guardar siempre y cuando tenga los 22 numeros, de otra forma no tiene que ser posible guardar. Esto achicaria mucho el margen de error.
    banco varchar(60),
    cuenta varchar(16),
    comision varchar(40),
    responsable varchar(40),
    forma_pago varchar(40),
    notas text

);

CREATE TABLE usuarios(
	id int(8) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(50),
    apellido varchar(50),
    legajo int(8) UNSIGNED NOT NULL UNIQUE KEY,
    secretariia varchar(50)
);
