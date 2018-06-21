from PyQt5 import QtCore
from libs.db import querier
import cerberus
from validadores.validador_afiliado import esquemaAfiliado

class ModeloAfiliado(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

        # La idea ahora es separar el esquema de validación de los datos y campos que se van a usar, nosotros no vamos a usar
        # todos los campos en la tabla, habíamos definido los que se encuentran en el archivo 'cosas para hacer.md'
        # | Legajo | Apellido | Nombre | DNI | Dirección | Teléfono | Ordenado alfabéticamente por apellido
        # Calle + Altura + Piso + Depto + (Localidad)

    def __init__(self, propiedades = None, parent = None):
        super(ModeloAfiliado, self).__init__()
        if parent:
            self.__parent = parent
        self.__propiedades = ['legajo','dni',
            'tipo_afiliado','cuil',
            'apellido','nombre',
            'fecha_nacimiento', 'edad', 'estado_civil',
            'nacionalidad', 'calle', 'altura',
            'piso', 'depto','cod_postal', 'barrio',
            'localidad', 'telefono_particular',
            'telefono_laboral', 'celular','email',
            'lugar_trabajo', 'jerarquia',
            'fecha_ingreso', 'antiguedad',
            'nivel_estudios'
        ]
        if propiedades:
            self.__propiedades = self.validarPropiedades(propiedades)

        self.__listaAfiliados = [] # Los valores de prueba los saco del archivo fuente
        self.__afiliado = []

# =============================================================================================
# Esta lista de listas es la que aparece en la tabla de afiliados apenas arranca
# el programa
# Tengo que hacer que el programa levante esta lista desde la base de datos.
# En la base de datos tengo solamente un objeto que tiene todos los campos vacíos salvo el dni
# El legajo hay que modificarlo porque tiene auto-incremento

# Legajo : 1, dni : 37537040 es lo que tiene que aparecer cuando uso esta función
    def verListaAfiliados(self, condiciones = None, orden = None):
        self.__listaAfiliados = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'afiliados',
            condiciones = condiciones,
            orden = orden)
        if self.__listaAfiliados:
            self.layoutChanged.emit()
            return True
        return False

    def verDetallesAfiliado(self, afiliado = QtCore.QModelIndex()):
        # Extraigo el legajo para buscarlo de esa forma en la base de datos
        # porque la tabla no me muestra todos los datos
        afiliado = self.__listaAfiliados[afiliado.row()]
        legajo = afiliado[0]

        respuesta = self.__querier.traerElementos(
            condiciones = [('legajo', '=', legajo)],
            tabla = 'afiliados',
            limite = 1
            )

        afiliado = list(respuesta[0])
        print(afiliado)

        self.__afiliado = afiliado
        return self.__afiliado

    def guardarAfiliado(self, afiliado):
        respuesta = self.__querier.traerElementos(
            campos = ['legajo'],
            condiciones = [('legajo', '=', afiliado['legajo'])],
            tabla = 'afiliados',
            limite = 1)
        print (respuesta)

        if not (self.__v.validate(afiliado, esquemaAfiliado)):
            errors = self.__v.document_error_tree
            # print(errors)
            for propiedad in esquemaAfiliado:
                try:
                    print("Hay un error en el campo: " + errors[propiedad].errors[0].document_path[0])
                except:
                    pass

            return False

        if respuesta:
            # Si este if evalua en verdadero significa que existe
            # un registro con este legajo, por lo que se usar actualizarElemento
            # en lugar de insertarElemento
            self.__querier.actualizarElemento('afiliados', afiliado, [("dni", "=", afiliado['dni'])])
            self.verListaAfiliados()

        else:
            self.__querier.insertarElemento('afiliados', afiliado)
            self.verListaAfiliados()

        return True

    def bajaAfiliado(self, afiliado):
        tabla = "afiliados"
        self.__querier.actualizarElemento(tabla, afiliado, [("legajo", "=", afiliado['legajo'])])
        self.verListaAfiliados()

    def validarPropiedades(self, propiedades):
# ahora mi función se asegura que las propieades existan en la lista, debería encontrar si hay alguna forma mas elegante de hacer esto
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

# Estas son las funciones específicas de Qt para las tablas
    def rowCount(self, parent):
        return len(self.__listaAfiliados)

    def columnCount(self, parent):
        if self.__listaAfiliados:
            return len(self.__listaAfiliados[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaAfiliados[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla

    def setData(self, index, value, role = QtCore.Qt.EditRole):
# Esta función no la estoy usando
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.articulos[row][column]

            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
# Los objetos tipo diccionario no ordenan sus elementos, por eso usar dict.keys() me tira los nombres
# de las columnas en cualquier orden. Acá debería usar la lista propiedades.
# además de salir ordenado, se ajusta la cantidad de columnas correspondiente
                keys = list(self.__propiedades)
                return keys[section]
