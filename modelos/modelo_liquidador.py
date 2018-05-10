from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloLiquidador(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

        # La idea ahora es separar el esquema de validación de los datos y campos que se van a usar, nosotros no vamos a usar
        # todos los campos en la tabla, habíamos definido los que se encuentran en el archivo 'cosas para hacer.md'
        # | Mes | Proveedor | Importe | Cuota N° | Total Cuotas

    def __init__(self, propiedades = None, parent = None):
        super(ModeloLiquidador, self).__init__()
        if parent:
            self.__parent = parent
        self.__propiedades = [
            'id','legajo_afiliado',
            'fecha_descuento','fecha_carga_inicial',
            'proveedor_id','cuota_actual',
            'total_cuotas','importe_actual',
            'importe_total','n_credito',
        ]

        if propiedades:
            self.__propiedades = self.validarPropiedades(propiedades)

        self.__listaDebitos = [] # Los valores de prueba los saco del archivo fuente
        self.__afiliado = []

    def verListaLiquidacion(self, condiciones = None):
        self.__listaDebitos = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'debitos',
            condiciones = condiciones)

        for index,debito in enumerate(self.__listaDebitos):
            debito = list(debito)
            self.__listaDebitos[index] = debito

        self.__setTotales()

        self.__toString(1)
        self.__toString(3)

        if self.__listaDebitos:
            self.layoutChanged.emit()
            return True
        return False

    def __setTotales(self):
        self.total_debitos = len(self.__listaDebitos)
        self.importe_total = 0
        for debito in self.__listaDebitos:
            self.importe_total += debito[3]

    def __toString(self, index):
        for debito in self.__listaDebitos:
            debito[index] = str(debito[index])

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
        return len(self.__listaDebitos)

    def columnCount(self, parent):
        if self.__listaDebitos:
            return len(self.__listaDebitos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaDebitos[row][column] # value contiene la lista de listas que contiene los afiliados

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
