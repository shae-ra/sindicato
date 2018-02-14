from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloDebitos(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloDebitos, self).__init__()

        self.__esquemaDebitos = {
            'legajo_afiliado' : {'type' : 'integer', 'maxlength' : 8 },
            'id_banco' : {'type' : 'integer', 'maxlength' : 8 },
            'cbu' : { 'type': 'integer', 'maxlength' : 22},  
        }
