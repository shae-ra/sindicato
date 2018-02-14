from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloBancos(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloBancos, self).__init__()

        self.__esquemaBancos = {
            'id' : {'type' : 'integer', 'maxlength' : 8 },
            'nombre' : { 'type': 'string', 'maxlength' : 20},  
        }
