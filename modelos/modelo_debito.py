from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloDebito(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloDebito, self).__init__()

        self.__esquemaDebitos = {
            'id' : {'type' : 'integer', 'maxlength' : 32 },
            'legajo_afiliado' : { 'type' : 'string', 'maxlength' : 22 },
            'fecha_descuento' : { 'type' : 'date' },
            'fecha_carga_actual' : { 'type' : 'date' },
            'proveedor_id' : {  'type': 'integer' },
            'cuota_actual' : { 'type' : 'integer' },
            'total_cuotas' : { 'type' : 'integer' },
            'importe_actual' : { 'type' : 'integer' },
            'importe_total' : { 'type' : 'integer' }

        }

        self.__propiedades = [
            'id',
            'legajo_afiliado',
            'fecha_descuento',
            'fecha_carga_actual',
            'proveedor_id',
            'cuota_actual',
            'total_cuotas',
            'importe_actual',
            'importe_total'
        ]
        self.__propiedades = self.validarPropiedades(propiedades)

        self.__listaDebitos = []

    def guardarDebito(self, debito):
        print(debito['total_cuotas'])

        for cuota_actual in range(debito['total_cuotas']): # El 1 indica desde que numero arrancar
            debito['cuota_actual'] = cuota_actual + 1
            print(debito)
            self.__querier.insertarElemento('debitos', debito)

    def verTablaDebitos(self, condiciones):
        self.__listaDebitos = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'debitos',
            condiciones = condiciones
        )
        self.layoutChanged.emit()


    def validarPropiedades(self, propiedades):
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

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
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaDebitos[row][column]
            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                keys = list(self.__propiedades)
                return keys[section]
