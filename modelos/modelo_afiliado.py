from PyQt5 import QtCore
from libs.db import querier
import cerberus

class ModeloAfiliado(QtCore.QAbstractTableModel):

    q = querier.Querier()

    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloAfiliado, self).__init__()

        self.__esquemaAfiliado = {
            'legajo' : { 'type' : 'integer' },
            'dni' : {'type' : 'integer' },
            'tipo_afiliado' : { 'type' : 'string', 'maxlength' : 20 },
            'cuil' : { 'type' : 'string', 'maxlength' : 11 },
            'apellido' : { 'type' : 'string', 'maxlength' : 50 }
        }


        # self.__afiliado = {
        #     'legajo' : 382211,
        #     'dni' : 13878052,
        #     'tipo_afiliado' : 'ACTIVO',
        #     ''
        # }

        self.__afiliado = { }

        self.__listaAfiliados = []

    def verDetallesAfiliado(afiliado):
        # respuesta = self.q.traerElementos(condiciones = [ 'legajo', '=', legajo ])
        print(afiliado)
        self.__afiliado = afiliado

    def guardarAfiliado():
        pass

    def borrarAfiliado():
        pass
