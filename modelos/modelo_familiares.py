from PyQt5 import QtCore
from libs.db import querier
from validadores.validador_familiar import esquemaFamiliar
import cerberus

class ModeloFamiliares(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloFamiliares, self).__init__()

        self.__propiedades = [ 'familiares.dni', 'familiares.relacion', 'familiares.nombre',
        'familiares.apellido', 'familiares.fecha_nacimiento',
        'familiares.edad', 'familiares.nivel_estudios', 'familiares.legajo_afiliado']

        self.__listaFamiliares = []

    def borrarFamiliar(self, idFamiliar):
        self.__querier.borrarElemento('familiares', 'dni', idFamiliar)

    def guardarFamiliar(self, familiar):
        self.__querier.insertarElemento('familiares', familiar)
        self.verListaFamiliares()
        return True

    def refrescarTabla(self):
        self.__listaFamiliares = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'familiares',
            uniones = [("afiliados", "legajo_afiliado = afiliados.legajo")],
            condiciones = self.condicionesRefresco,
            orden = self.ordenRefresco)
        if self.__listaFamiliares:
            self.layoutChanged.emit()

    def verListaFamiliares(self, condiciones = None, orden = None):
        self.condicionesRefresco = condiciones
        self.ordenRefresco = orden

        self.__listaFamiliares = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'familiares',
            uniones = [("afiliados", "legajo_afiliado = afiliados.legajo")],
            orden = orden)

        if self.__listaFamiliares:
            self.layoutChanged.emit()
            return True
        return False

# Estas son las funciones específicas de Qt para las tablas
    def rowCount(self, parent):
        return len(self.__listaFamiliares)

    def columnCount(self, parent):
        if self.__listaFamiliares:
            return len(self.__listaFamiliares[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaFamiliares[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
# Los objetos tipo diccionario no ordenan sus elementos, por eso usar dict.keys() me tira los nombres
# de las columnas en cualquier orden. Acá debería usar la lista propiedades.
# además de salir ordenado, se ajusta la cantidad de columnas correspondiente
                keys = list(self.__propiedades)
                return keys[section]
