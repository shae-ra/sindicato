from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloDescuentos(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloDescuentos, self).__init__()

        self.__esquemaDescuentos = {
            'id' : {'type' : 'integer', 'maxlength' : 32 },
            'mes_descuento' : {'type' : 'date' },
            'proveedor_id' : { 'type': 'integer', 'maxlength' : 16},
            'cuota_actual' : {'type' : 'integer', 'maxlength' : 2 },
            'total_cuotas' : {'type' : 'integer', 'maxlength' : 2 },
            'fecha_carga_actual' : {'type' : 'date' },  
        }
