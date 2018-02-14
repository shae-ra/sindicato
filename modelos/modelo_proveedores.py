from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloProveedores(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloProveedores, self).__init__()

        self.__esquemaProveedores = {
            'id' : { 'type' : 'integer', 'maxlength' : 8 },
            'nombre' : { 'type': 'string', 'maxlength' : 50 },
            'servicios' : { 'type': 'string', 'maxlength' : 100 },
    		'calle' : { 'type': 'string', 'maxlength' : 80 }, 
    		'altura' : { 'type': 'integer', 'maxlength' : 8 },
            'localidad' : { 'type': 'string', 'maxlength' : 50 },
            'telefono' : { 'type': 'string', 'maxlength' : 20 },
            'celular' : { 'type': 'string', 'maxlength' : 20 },
            'email' : { 'type': 'string', 'maxlength' : 80 },
            'cuit' : { 'type' : 'string', 'maxlength' : 11 },
            'razon_social' : { 'type': 'string', 'maxlength' : 60 },
            'cbu' : { 'type': 'integer', 'maxlength' : 22 },
            'banco' : { 'type': 'string', 'maxlength' : 60 },
            'cuenta' : { 'type': 'integer', 'maxlength' : 16 },
            'comision' : { 'type': 'string', 'maxlength' : 40 },
            'responsable' : { 'type': 'string', 'maxlength' : 40 },
            'forma_pago' : { 'type': 'string', 'maxlength' : 40 },
            'notas' : { 'type': 'string', 'maxlength' : 1000 }, 
        }
