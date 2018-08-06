# querier.py
import mysql.connector
import socket
from mysql.connector import errorcode
from configparser import ConfigParser

class Querier(object):
    _instance = None

    def __new__(self, user = None, password = None, host = None, database = None, prefijo = "", *args, **kwargs):
        if not self._instance:
            self._instance = super(Querier, self).__new__(self, *args, **kwargs)

            self._instance.__cargarConfiguracion()
            self._instance.setConexion(user, password, host, database)
            self.tablas = []
            self.tablas = self._instance.getTablas()
            self.prefijo = prefijo

        return self._instance

    def actualizarElemento(self, tabla, elemento, condiciones = None):
        if tabla not in self.tablas:
            return False
        consulta = "UPDATE {} SET ".format(tabla)

        donde = ""

        total = len(elemento)-1

        for index, columna in enumerate(elemento.keys()):
            if (self.prefijo + "id") in columna.lower():
                # print("La columna: " + columna + " fue ignorada")
                donde = self.__agregarFiltros([(columna, " = ", elemento[columna])])
            consulta += "{}{} = %({}{})s".format(self.prefijo, columna, self.prefijo, columna)
            if index < total:
                consulta += ", "

        if condiciones:
            donde = self.__agregarFiltros(condiciones)

        consulta += donde

        print("\nDEBUG - Consulta actualizar elemento a mysql: ", consulta , "\n")
        self.__consultar_e(consulta, elemento)
        return True

    def agregarUsuario(self, user, password):
        # password = hash(password)

        hostname = socket.gethostname()

        grant = "GRANT SELECT, INSERT, UPDATE ON {}.* TO '{}'@'{}' IDENTIFIED BY '{}'".format(self.database, user, hostname, password)

    def borrarElemento(self, tabla, pkeyElemento, idElemento):
        if not tabla or not pkeyElemento:
            return False
        consulta = "DELETE FROM {} WHERE {} = '%s'".format(tabla, pkeyElemento)

        db = self.__conectar()
        cursor = db.cursor()

        cursor.execute(consulta, (idElemento,))
        db.commit()

        cursor.close()
        db.close()

        return True

    def consultaManual(self, consulta):
        db = self.__conectar()
        cursor = db.cursor()
        cursor.execute(consulta)
        db.commit()
        cursor.close()
        db.close()

    def getTablas(self):
        consulta = "SHOW TABLES;"
        try:
            rawTablas = self.__consultar(consulta)
            self.tablas = []
            for tabla in rawTablas:
                self.tablas.append(tabla[0])
        except:
            self.tablas = []
        return self.tablas

    def getConfig(self):
        config = {
            'user' : self.user,
            'pass' : self.password,
            'host' : self.host,
            'database' : self.database
        }

        return config

    def guardarConfiguracion(self):
        config = ConfigParser()

        config['DEFAULT']['user'] = self.user
        config['DEFAULT']['password'] = self.password
        config['DEFAULT']['host'] = self.host
        config['DEFAULT']['database'] = self.database

        with open('database.ini', 'w') as configFile:
            config.write(configFile)

# Esta funcion recibe un diccionario donde key = columna y value = valor
    def insertarElemento(self, tabla, elemento):
        if tabla not in self.tablas:
            return False
        consulta = "INSERT INTO {} (".format(tabla)
        valores = "VALUES ("

        for index, columna in enumerate(elemento.keys()):
            consulta += self.prefijo + columna
            valores += "%({})s".format(columna)
            if len(elemento) - 1 != index:
                consulta += ", "
                valores += ", "
        valores += ")"
        consulta += ") " + valores

        print("\nDEBUG - Consulta de insertar elemento:\n", consulta, "\n\n", elemento, "\n")
        self.__consultar_e(consulta, elemento)
        return True

    def setConexion(self, user = None, password = None , host = None , database = None):
        if user:
            self.user = user
        if password:
            self.password = password
        if host:
            self.host = host
        if database:
            self.database = database
        self._conectable = self.probarConexion()

    def traerElementos(self, campos = None, condiciones = None, limite = None, uniones = None, orden = None, tabla = None):
        # union debe ser una tupla o lista con dos elementos: union[0] es el nombre de la tablas, union[1] es
        # el conjunto de campos que deben conincidir en la union, ejemplo "`proveedores`.`prov_id` = `articulos_de_proveedores`.`proveedor`"
        donde = ""
        consulta = "SELECT "

        consulta += self.__encampar(campos)
        print(self.tablas)
        consulta += " FROM {} ".format(tabla)
        if uniones:
            for union in uniones:
                consulta += self.__unirTabla(union[0], union[1])

        if condiciones:
            donde = self.__agregarFiltros(condiciones)
        consulta += donde

        if orden:
            consulta += " ORDER BY {} {}".format(orden[0], orden[1])

        if limite:
            consulta += " LIMIT {}".format(limite)

        print("DEBUG - CONSULTA PARA VER ELEMENTOS: ", consulta)

        db = self.__conectar()
        cursor = db.cursor()

        cursor.execute(consulta)
        respuesta = cursor.fetchall()

        # print (respuesta)

        cursor.close()
        db.close()

        return respuesta

    def __agregarFiltros(self, filtros):
        donde = "\nWHERE "

        totalFiltros = len(filtros)

        for index, filtro in enumerate(filtros):
            campo, condicion, valor = filtro
            donde += "{} {} {}".format(campo, condicion, valor)
            # campo + condicion + valor
            if index < totalFiltros-1:
                donde += "\nAND "
        # donde += campo + condicion + "%({})s".campo

        return donde

    def __conectar(self):
        try:
            con = mysql.connector.connect(
                user = self.user, password = self.password,
                host = self.host, database = self.database)
            return con
        except:
            return False

    def __consultar_e(self, consulta, elemento):
        if not self._conectable:
            return
        db = self.__conectar()
        cursor = db.cursor()
        try:
            if (type(elemento) != type({})):
                cursor.executemany(consulta, elemento)
            else:
                cursor.execute(consulta, elemento)
            db.commit()
            print("Se logro hacer la consulta correctamente")
        except mysql.connector.Error as error:
            print("No se logro hacer la consulta: ", error)
            db.rollback()

        cursor.close()
        db.close()

    def __consultar(self, consulta):
        if not self._conectable:
            return
        db = self.__conectar()
        cursor = db.cursor()
        resultado = []

        try:
            cursor.execute(consulta)
            resultado = cursor.fetchall()
        except:
            resultado = None

        cursor.close()
        db.close()
        return resultado

    def __encampar(self, campos):
        listaDeCampos = ""
        if campos:
            totalCampos = len(campos)
            for index, campo in enumerate(campos):
                listaDeCampos += "{}".format(campo)

                if index < totalCampos -1:
                    listaDeCampos += ", "
        else:
            listaDeCampos = " * "
        return listaDeCampos

    def probarConexion(self):
        db = self.__conectar()
        if db:
            db.close()
            return True

        return False

    def __cargarConfiguracion(self):
        config = ConfigParser()

        if config.read('database.ini'):
            try:
                self.user = config['DEFAULT']['user']
            except:
                self.user = self.user if self.user else "root"
            try:
                self.password = config['DEFAULT']['password']
            except:
                self.password = self.password if self.password else "admin1234"
            try:
                self.database = config['DEFAULT']['database']
            except:
                self.database = self.database if self.database else "database"
            try:
                self.host = config['DEFAULT']['host']
            except:
                self.host = self.host if self.host else "127.0.0.1"

    def __unirTabla(self, tablas, on):
        union = "JOIN {} ON {} ".format(tablas, on)
        return union
