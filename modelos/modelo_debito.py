from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloDebito(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloDebito, self).__init__()

        self.__esquemaDebitos = {
            'legajo_afiliado' : {'type' : 'integer', 'maxlength' : 8 },
            'id_banco' : {'type' : 'integer', 'maxlength' : 8 },
            'cbu' : { 'type': 'integer', 'maxlength' : 22},

#Importado de ModeloDescuentos
            'id' : {'type' : 'integer', 'maxlength' : 32 },
            'mes_descuento' : {'type' : 'date' },
            'proveedor_id' : { 'type': 'integer', 'maxlength' : 16},
            'cuota_actual' : {'type' : 'integer', 'maxlength' : 2 },
            'total_cuotas' : {'type' : 'integer', 'maxlength' : 2 },
            'fecha_carga_actual' : {'type' : 'date' },
        }


    def guardarDebito(self, debito):
        self.__querier.insertarElemento('debitos', debito)
