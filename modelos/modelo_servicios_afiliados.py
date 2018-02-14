from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloServiciosAfiliados(QtCore.QAbstractTableModel):
    q = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloServiciosAfiliados, self).__init__()

        self.__esquemaServiciosAfiliados = {
            'id' : {'type' : 'integer', 'maxlength' : 8 },
            'legajo_afiliado' : {'type' : 'integer', 'maxlength' : 8 },
            'fecha' : { 'type': 'date'},
            'cantidad' : { 'type': 'integer', 'maxlength' : 20}, 
            'detalle' : { 'type': 'string', 'maxlength' : 80},  
        }
