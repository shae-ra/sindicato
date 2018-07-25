from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloServiciosAfiliados(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloServiciosAfiliados, self).__init__()

        self.__esquemaServiciosAfiliados = {
            'id_servicio' : {'type' : 'integer', 'maxlength' : 8 },
            'legajo_afiliado' : {'type' : 'integer', 'maxlength' : 8 },
            'fecha' : { 'type': 'date'},
            'cantidad' : { 'type': 'integer', 'maxlength' : 20},
            'detalle' : { 'type': 'string', 'maxlength' : 80},
        }

        self.__propiedades = ['fecha', 'nombre', 'cantidad', 'detalle' ]

        self.__tablaServicios = []

    def asociarServicio(self, servicio):
        self.__querier.insertarElemento('servicios_afiliado', servicio)
        self.verTablaServicios(servicio['legajo_afiliado'])
        return True

    def verTablaServicios(self, legajo):
        if not legajo:
            legajo = "0"
        self.__tablaServicios = self.__querier.traerElementos(
            tabla = 'servicios_afiliado',
            campos = ['fecha', 'nombre', 'detalle', 'cantidad'],
            uniones = [('servicios', 'servicios.id = id_servicio')],
            condiciones = [('legajo_afiliado', '=', legajo)],
            orden = ("fecha", "DESC")
        )

        self.__tablaServicios = self.__toList()
        self._setDates(0)

        if self.__tablaServicios:
            self.layoutChanged.emit()
            return True
        return False

    def _setDates(self, dateIndex):
        for servicio in self.__tablaServicios:
            servicio[dateIndex] = QtCore.QDate(servicio[dateIndex])

    def __toList(self):
        listaServicios = []
        for index, debito in enumerate(self.__tablaServicios):
            listaServicios.append(list(debito))
        return listaServicios

# Estas son las funciones específicas de Qt para las tablas
    def rowCount(self, parent):
        return len(self.__tablaServicios)

    def columnCount(self, parent):
        if self.__tablaServicios:
            return len(self.__tablaServicios[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__tablaServicios[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
# Los objetos tipo diccionario no ordenan sus elementos, por eso usar dict.keys() me tira los nombres
# de las columnas en cualquier orden. Acá debería usar la lista propiedades.
# además de salir ordenado, se ajusta la cantidad de columnas correspondiente
                keys = list(self.__propiedades)
                return keys[section]
