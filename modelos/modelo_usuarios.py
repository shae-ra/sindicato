from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloUsuario(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloUsuario, self).__init__()

        self.__esquemaUsuario = {
            'id' : { 'type': 'integer', 'maxlength' : 8 },
            'apellido' : { 'type' : 'string', 'maxlength' : 50 },
    		'nombre' : { 'type': 'string', 'maxlength' : 50 },
    		'legajo' : { 'type': 'integer', 'maxlength' : 8 },
    		'secretaria' : { 'type': 'string', 'maxlength' : 50 },
        }

