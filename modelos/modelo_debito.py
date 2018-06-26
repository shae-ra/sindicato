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
            'importe_total' : { 'type' : 'integer' },
            'estado' : { 'type' : 'string' },
            'motivo' : { 'type' : 'string' },
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
            'importe_total',
            'estado',
            'motivo'
        ]
        self.__propiedades = self.validarPropiedades(propiedades)

        self.listaDebitos = []

    def guardarDebito(self, debito):
        # print(debito['total_cuotas'])
        mes = debito['fecha_descuento'].month
        for indexCuota in range(debito['total_cuotas']): # El 1 indica desde que numero arrancar
            debito['cuota_actual'] = indexCuota + 1

            newMonth = mes + indexCuota
            if newMonth > 12:
                newYear = debito['fecha_descuento'].year + 1
                newMonth = debito['fecha_descuento'].month % 12 + 1
                newDate = date(newYear, newMonth, 1)
            else:
                newDate = date(debito['fecha_descuento'].year, newMonth, 1)

            debito['fecha_descuento'] = newDate

            self.__querier.insertarElemento('debitos', debito)

    def actualizarDebito(self, debito):
        self.__querier.actualizarElemento(tabla = 'debitos', elemento = debito)

    def verTablaDebitos(self, condiciones, orden = None, fechas = None):
        self.__condicionesRefresco = condiciones
        self.__ordenRefresco = orden
        self.__fechasRefresco = fechas
        self.listaDebitos = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'debitos',
            condiciones = condiciones,
            orden = orden
        )

        self.listaDebitos = self.__toList()

        self.__toString(3)

        for fecha in fechas:
            self._setDates(fecha)

        self.layoutChanged.emit()

    def refrescarTabla(self):
        self.verTablaDebitos(
            condiciones = self.__condicionesRefresco,
            orden = self.__ordenRefresco,
            fechas = self.__fechasRefresco)

    def borrarDebito(self, idDebito):

        self.__querier.borrarElemento('debitos', 'id', idDebito)

    def __incrementMonth(self, date):
        if date.month() < 12:
            incrementedDate = date(date.year(), date.month() + 1 , date.day())
        else:
            incrementedDate = date(date.year() + 1, 0, date.day())
        print("DEBUG - Incremented Date : {}".format(incrementedDate))

        return incrementedDate

    def __toList(self):
        listaDebitos = []
        for index, debito in enumerate(self.listaDebitos):
            listaDebitos.append(list(debito))

        return listaDebitos

    def __toString(self, index):
        for debito in self.listaDebitos:
            debito[index] = str(debito[index])

    def _setDates(self, dateIndex):
        for debito in self.listaDebitos:
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
        return len(self.listaDebitos)

    def columnCount(self, parent):
        if self.listaDebitos:
            return len(self.listaDebitos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.listaDebitos[row][column]
            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                keys = list(self.__propiedades)
                return keys[section]
