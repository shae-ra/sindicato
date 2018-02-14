from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloFamiliares(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloFamiliares, self).__init__()

        self.__esquemaFamiliares = {
            'dni' : {'type' : 'integer', 'maxlength' : 8 },
            'relacion' : { 'type' : 'string', 'maxlength' : 40 },
            'nombre' : { 'type' : 'string', 'maxlength' : 50 },
            'apellido' : { 'type' : 'string', 'maxlength' : 50 },
    		'fecha_nacimiento' : { 'type': 'date'},
    		'edad' : { 'type': 'integer', 'maxlength' : 3 },
    		'nivel_estudios' : { 'type': 'string', 'maxlength' : 40 }
            'legajo_afiliado' : {'type' : 'integer', 'maxlength' : 8 },    
        }


 