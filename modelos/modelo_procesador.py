from PyQt5 import QtCore
from libs.db import querier
from datetime import date
import cerberus

class ModeloProcesador(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

        # La idea ahora es separar el esquema de validación de los datos y campos que se van a usar, nosotros no vamos a usar
        # todos los campos en la tabla, habíamos definido los que se encuentran en el archivo 'cosas para hacer.md'
        # | Mes | Proveedor | Importe | Cuota N° | Total Cuotas

    def __init__(self, propiedades = None, parent = None):
        super(ModeloProcesador, self).__init__()
        if parent:
            self.__parent = parent
        self.__propiedades = ["Estado", "Fecha", "Legajo", "Banco", "CBU", "Importe", "CUIT", "Orden de movimiento", "Codigo de rechazo", "Motivo de rechazo", "Empresa"
        ]

        if propiedades:
            self.__propiedades = self.validarPropiedades(propiedades)

        self.__debitosAProcesar = [] # Los valores de prueba los saco del archivo fuente

        self.__debitosProcesables = [] # Los valores de acá salen de la base de datos

        self.__codigosDeRechazo = {}

        self.verListaDebitosProcesables()
        self.verListaCodigosDeRechazo()

        # self.setConfig(banco = "P", cuit = "30561600194", empresa = "SIND T MUN MERLO")

    def verListaCodigosDeRechazo(self):

        self.__codigosDeRechazo = self.__querier.traerElementos(
            campos = ["codigo", "descripcion"],
            tabla = "codigos_rechazo"
        )
        codigosDeRechazo = dict( (codigo, descripcion) for codigo, descripcion in self.__codigosDeRechazo)
        self.__codigosDeRechazo = codigosDeRechazo
        # CodigosDeRechazo ahora contiene una lista de tuplas, cada tupla es un registro de la base de datos.

    def verListaDebitosAProcesar(self, lista):

        self.__debitosAProcesar = lista

        for index,item in enumerate(lista):
            codigo = item[8]
            if codigo != "   ":

                # print(descripcion)
                self.__debitosAProcesar[index][9] = self.__codigosDeRechazo[codigo]

        if self.__debitosAProcesar:
            self.layoutChanged.emit()
            return True
        return False

    def verListaDebitosProcesables(self):

        self.__debitosProcesables = self.__querier.traerElementos(
            campos = ["id","id_temporal", "legajo_afiliado", "cbu", "fecha_descuento", "importe_actual"],
            tabla = "debitos",
            uniones = [("afiliados", "afiliados.legajo = debitos.legajo_afiliado")],
            condiciones = [("id_temporal", "IS NOT", "NULL")]
        )

        print(self.__debitosProcesables)

    def apllicarCambios(self):

        for debito in self.__debitosAProcesar:
            print("Estado a actualizar: " + debito[0])
            print("Motivo a actualizar: " + debito[8])
            self.__querier.actualizarElemento(
                tabla = "debitos",
                elemento = { "id_temporal" : None,
                    "estado" : debito[0],
                    "motivo" : debito[8] },
                condiciones = [("id_temporal", "=", int(debito[7]))]
            )

        self.limpiarTabla()

    def actualizarDebito(self, debito, condiciones):
        self.__querier.actualizarElemento(
            tabla = "debitos",
            elemento = debito,
            condiciones = condiciones
        )

    def compararDebitosProcesables(self):

        for debitoAProcesar in self.__debitosAProcesar:
            pass

    def limpiarTabla(self):
        self.__debitosAProcesar = []
        self.layoutChanged.emit()

    def __setTotales(self, indexImporte):
        self.total_debitos = len(self.__debitosAProcesar)
        self.importe_total = 0
        if self.total_debitos > 0:
            for debito in self.__debitosAProcesar:
                self.importe_total += debito[indexImporte]

    def __toString(self, index):
        for debito in self.__debitosAProcesar:
            debito[index] = str(debito[index])

    def validarPropiedades(self, propiedades):
# ahora mi función se asegura que las propieades existan en la lista, debería encontrar si hay alguna forma mas elegante de hacer esto
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

# Estas son las funciones específicas de Qt para las tablas
    def rowCount(self, parent):
        return len(self.__debitosAProcesar)

    def columnCount(self, parent):
        if self.__debitosAProcesar:
            return len(self.__debitosAProcesar[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__debitosAProcesar[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla

    def setData(self, index, value, role = QtCore.Qt.EditRole):
# Esta función no la estoy usando
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.articulos[row][column]

            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
# Los objetos tipo diccionario no ordenan sus elementos, por eso usar dict.keys() me tira los nombres
# de las columnas en cualquier orden. Acá debería usar la lista propiedades.
# además de salir ordenado, se ajusta la cantidad de columnas correspondiente
                keys = list(self.__propiedades)
                return keys[section]
