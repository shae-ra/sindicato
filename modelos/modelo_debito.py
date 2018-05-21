from PyQt5 import QtCore
from libs.db import querier
import cerberus

from datetime import date

class ModeloDebito(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloDebito, self).__init__()

        self.__esquemaDebitos = {
            'id' : {'type' : 'integer', 'maxlength' : 32 },
            'legajo_afiliado' : { 'type' : 'string', 'maxlength' : 22 },
            'fecha_descuento' : { 'type' : 'date' },
            'fecha_carga_inicial' : { 'type' : 'date' },
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
            'fecha_carga_inicial',
            'proveedor_id',
            'cuota_actual',
            'total_cuotas',
            'importe_actual',
            'importe_total'
        ]
        self.__propiedades = self.validarPropiedades(propiedades)

        self.__listaDebitos = []

    def guardarDebito(self, debito):
        # print(debito['total_cuotas'])
        mes = debito['fecha_descuento'].month
        for indexCuota in range(debito['total_cuotas']): # El 1 indica desde que numero arrancar
            debito['cuota_actual'] = indexCuota + 1

            newMonth = mes + indexCuota
            if newMonth > 12:
                newYear = debito['fecha_descuento'].year + 1
                newMonth = debito['fecha_descuento'].month % 12
                newDate = date(newYear, newMonth, 1)
            else:
                newDate = date(debito['fecha_descuento'].year, newMonth, 1)

            debito['fecha_descuento'] = newDate

            self.__querier.insertarElemento('debitos', debito)

    def verTablaDebitos(self, condiciones):
        self.__listaDebitos = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'debitos',
            condiciones = condiciones
        )

        self.__listaDebitos = self.__toList()
        self._setDates(0)
        self._setDates(5)

        self.layoutChanged.emit()

    def __incrementMonth(self, date):
        if date.month() < 12:
            incrementedDate = date(date.year(), date.month() + 1 , date.day())
        else:
            incrementedDate = date(date.year() + 1, 0, date.day())
        print("DEBUG - Incremented Date : {}".format(incrementedDate))

        return incrementedDate

    def __toList(self):
        listaDebitos = []
        for index, debito in enumerate(self.__listaDebitos):
            listaDebitos.append(list(debito))

        return listaDebitos

    def _setDates(self, dateIndex):
        for debito in self.__listaDebitos:
            debito[dateIndex] = QtCore.QDate(debito[dateIndex])

    def validarPropiedades(self, propiedades):
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

    def consultarUltimoNumeroDeOrden(self, proveedor, fecha):
        respuesta = self.__querier.traerElementos(
            tabla = "debitos",
            campos = ["n_orden"],
            condiciones = [
                ('proveedor_id' ,'=' , proveedor),
                ('fecha_carga_inicial' ,'=' , fecha),
            ],
            limite = 1
        )

        if respuesta:
            return respuesta[0][-4]

        else:
            return 0

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
