from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloServicios(QtCore.QAbstractListModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloServicios, self).__init__()

        self.__esquemaServicios = {
            'id' : {'type' : 'integer', 'maxlength' : 16 },
            'nombre' : { 'type' : 'string', 'maxlength' : 50 },
        }

        self.__listaServicios = []

    def guardarServicio(self, servicio):
        self.__querier.insertarElemento('servicios', servicio)
        self.verListaServicios()

    def verListaServicios(self):
        self.__listaServicios = self.__querier.traerElementos(
            tabla = 'servicios',
            campos = ['nombre', 'id'],
            orden = ('nombre', 'ASC')
        )

        if self.__listaServicios:
            self.layoutChanged.emit()

        print(self.__listaServicios)

    def rowCount(self, parent):
        return len(self.__listaServicios)

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaServicios[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla
