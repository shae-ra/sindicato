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
            'apellido' : { 'type' : 'string', 'maxlength' : 50 },
    		'nombre' : { 'type': 'string', 'maxlength' : 50 },
    		'fecha_nacimiento' : { 'type': 'date'},
    		'edad' : { 'type': 'integer', 'maxlength' : 3 },
    		'estado_civil' : { 'type': 'string', 'maxlength' : 20 },    
    		'nacionalidad' : { 'type': 'string', 'maxlength' : 20 },
    		'calle' : { 'type': 'string', 'maxlength' : 80 }, 
    		'altura' : { 'type': 'integer', 'maxlength' : 8 },
    		'piso' : { 'type': 'string', 'maxlength' : 10 },
    		'depto' : { 'type': 'string', 'maxlength' : 4 },
    		'cod_postal' : { 'type': 'string', 'maxlength' : 4 },
            'barrio' : { 'type': 'string', 'maxlength' : 30 },
            'localidad' : { 'type': 'string', 'maxlength' : 50 },
            'telefono' : { 'type': 'string', 'maxlength' : 20 },
            'celular' : { 'type': 'string', 'maxlength' : 20 },
            'email' : { 'type': 'string', 'maxlength' : 80 },
        }


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
