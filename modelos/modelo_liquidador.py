from PyQt5 import QtCore
from libs.db import querier
from datetime import date
import cerberus

class ModeloLiquidador(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

        # La idea ahora es separar el esquema de validación de los datos y campos que se van a usar, nosotros no vamos a usar
        # todos los campos en la tabla, habíamos definido los que se encuentran en el archivo 'cosas para hacer.md'
        # | Mes | Proveedor | Importe | Cuota N° | Total Cuotas

    def __init__(self, propiedades = None, parent = None):
        super(ModeloLiquidador, self).__init__()
        if parent:
            self.__parent = parent
        self.__propiedades = [
            'debitos.id', 'operacion', 'fecha_descuento',
            'legajo_afiliado', 'banco', 'cbu', 'importe_actual',
            'cuit', 'movimiento', 'empresa'
        ]

        if propiedades:
            self.__propiedades = self.validarPropiedades(propiedades)

        self.listaDebitos = [] # Los valores de prueba los saco del archivo fuente
        self.__afiliado = []

        self.setConfig(banco = "P", cuit = "30561600194", empresa = "SIND T MUN MERLO")

    def setConfig(self, banco, cuit, empresa):
        self.operacion = "71"
        self.banco = banco
        self.cuit = cuit
        self.empresa = empresa

    def setPrefijoOrden(self, prefijo):
        if self.jubilado:
            prefijo = "1400008" # CONSULTAR CON CLAUDIO!
        else:
            prefijo = "14"
        self.prefijoOrden = prefijo

    def setTipoAfiliado(self, tipo):
        if tipo == "ACTIVO":
            self.jubilado = False
        else:
            self.jubilado = True

    def verListaLiquidacionJub(self, fechasCobro, condiciones = None):
        self.listaDebitos = self.__querier.traerElementos(
            campos = ['debitos.id', 'legajo_afiliado', 'cbu', 'importe_actual', 'dni'],
            tabla = 'debitos',
            uniones = [("afiliados", "legajo_afiliado = afiliados.legajo")],
            condiciones = condiciones)

        for index, fechaCobro in enumerate(fechasCobro):
            fechaCobro = fechaCobro.strftime("%d%m%Y")
            fechasCobro[index] = fechaCobro

        orden = 1
        newListaDebitos = []

        for index, debito in enumerate(self.listaDebitos):
            debito = list(debito)
            legajo = debito[1]
            cbu = debito[2]
            dni = debito.pop(4)

            if len(legajo) != 8:
                continue
            if len(cbu) != 22:
                continue

            if int(dni[-1]) == 0:
                fechaCobro = fechasCobro[0]
            elif int(dni[-1]) <= 3:
                fechaCobro = fechasCobro[1]
            elif int(dni[-1]) <= 6:
                fechaCobro = fechasCobro[2]
            elif int(dni[-1]) <= 9:
                fechaCobro = fechasCobro[3]

            debito.insert(1, self.operacion)
            debito.insert(2, fechaCobro)
            debito.insert(4, self.banco)
            debito.insert(7, self.cuit)
            debito.insert(8, orden)
            debito.insert(9, self.empresa)

            newListaDebitos.append(debito)
            orden += 1

        self.listaDebitos = newListaDebitos

        self.__setTotales(6)

        self.__toString(2)
        self.__toString(6)


        if self.listaDebitos:
            self.layoutChanged.emit()
            return True
        return False

    def verListaLiquidacion(self, fechaCobro, condiciones = None):
        self.listaDebitos = self.__querier.traerElementos(
            campos = ['debitos.id', 'legajo_afiliado', 'cbu', 'importe_actual'],
            tabla = 'debitos',
            uniones = [("afiliados", "legajo_afiliado = afiliados.legajo")],
            condiciones = condiciones)
        fechaCobro = fechaCobro.strftime("%d%m%Y")

        orden = 1
        newListaDebitos = []
        for index,debito in enumerate(self.listaDebitos):
            debito = list(debito)
            legajo = debito[1]
            cbu = debito[2]
            if len(legajo) != 8:
                continue
            if len(cbu) != 22:
                continue

            debito.insert(1, self.operacion)
            debito.insert(2, fechaCobro)
            debito.insert(4, self.banco)
            debito.insert(7, self.cuit)
            debito.insert(8, orden)
            debito.insert(9, self.empresa)
            orden += 1

            newListaDebitos.append(debito)

        self.listaDebitos = newListaDebitos

        self.__setTotales(6)

        self.__toString(2)
        self.__toString(6)


        if self.listaDebitos:
            self.layoutChanged.emit()
            return True
        return False

    def actualizarDebito(self, debito, condiciones):
        self.__querier.actualizarElemento(
            tabla = "debitos",
            elemento = debito,
            condiciones = condiciones
        )

    def esProcesable(self):
        resultado = self.__querier.traerElementos(
            tabla = 'debitos',
            condiciones = [('id_temporal','IS NOT','NULL')],
            limite = 1
        )

        if resultado:
            return False
        return True

    def __setTotales(self, indexImporte):
        self.total_debitos = len(self.listaDebitos)
        self.importe_total = 0
        if self.total_debitos > 0:
            for debito in self.listaDebitos:
                self.importe_total += debito[indexImporte]

    def __toString(self, index):
        for debito in self.listaDebitos:
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
        return len(self.listaDebitos)

    def columnCount(self, parent):
        if self.listaDebitos:
            return len(self.listaDebitos[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.listaDebitos[row][column] # value contiene la lista de listas que contiene los afiliados

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
