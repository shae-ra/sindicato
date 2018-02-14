from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloServicios(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloServicios, self).__init__()

        self.__esquemaServicios = {
            'id' : {'type' : 'integer', 'maxlength' : 16 },
            'nombre' : { 'type' : 'string', 'maxlength' : 50 }, 
        }


 