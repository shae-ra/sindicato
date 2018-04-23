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


    def guardarDebito(self, debito):
        print(debito['total_cuotas'])

        for cuota_actual in range(debito['total_cuotas']): # El 1 indica desde que numero arrancar
            debito['cuota_actual'] = cuota_actual + 1
            print(debito)
            self.__querier.insertarElemento('debitos', debito)
