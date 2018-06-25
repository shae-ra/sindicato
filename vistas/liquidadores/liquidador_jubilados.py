

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic
from datetime import date

from modelos.modelo_liquidador import ModeloLiquidador

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class LiquidadorJubilados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		self.vistaLiqJubilado = uic.loadUi("gui/liquidadores/liquidadorJubilados.ui", self)

		self.vistaLiqJubilado.liqj_fecha_0.setDate(date.today())
		self.vistaLiqJubilado.liqj_fecha_123.setDate(date.today())
		self.vistaLiqJubilado.liqj_fecha_456.setDate(date.today())
		self.vistaLiqJubilado.liqj_fecha_789.setDate(date.today())

		self.model = ModeloLiquidador(propiedades = [
			'debitos.id', 'operacion', 'fecha_descuento',
			'legajo_afiliado', 'banco', 'cbu', 'importe_actual',
			'cuit', 'movimiento', 'empresa'])

		self.tbl_liqj.setModel(self.model)

		self.vistaLiqJubilado.btn_liquidar.clicked.connect(self.buscarDebitosALiquidar)

		self.vistaLiqJubilado.btn_exportar.clicked.connect(self.handleSaveEbt)

	def getFechaLiquidacion(self):
		mesALiquidar = self.vistaLiqJubilado.liqj_mes.currentIndex() + 1
		anioALiquidar = int(self.vistaLiqJubilado.liqj_anio.text()) # si no se ponen numeros esto estalla
		fechaLiquidacion = date(anioALiquidar, mesALiquidar, 1)

		return fechaLiquidacion

	def getFechaCobro(self, terminacion):
		if terminacion == "0":
			fechaCobro = self.vistaLiqJubilado.liqj_fecha_0.date()
		elif terminacion == "123":
			fechaCobro = self.vistaLiqJubilado.liqj_fecha_123.date()
		elif terminacion == "456":
			fechaCobro = self.vistaLiqJubilado.liqj_fecha_456.date()
		elif terminacion == "789":
			fechaCobro = self.vistaLiqJubilado.liqj_fecha_789.date()
		else:
			fechaCobro = date(0, 0, 0)

		fechaCobro = date(fechaCobro.year(), fechaCobro.month(), fechaCobro.day())
		return fechaCobro

	def buscarDebitosALiquidar(self):
		fechaLiquidacion = self.getFechaLiquidacion()
		fechaCobro0 = self.getFechaCobro("0")
		fechaCobro123 = self.getFechaCobro("123")
		fechaCobro456 = self.getFechaCobro("456")
		fechaCobro789 = self.getFechaCobro("789")

		self.model.verListaLiquidacionJub(
			[fechaCobro0,
			fechaCobro123,
			fechaCobro456,
			fechaCobro789],
			condiciones = [
			("YEAR(fecha_descuento)", "=", fechaLiquidacion.year),
			("MONTH(fecha_descuento)", "=", fechaLiquidacion.month),
			("estado", "is", "NULL"),
			("tipo_afiliado", "=", "'Jubilado'"),
			("cbu", "<>", "''")
			])

		self.setTotales()

	def setTotales(self):
		self.vistaLiqJubilado.liqj_cantidad_total.setText(str(self.model.total_debitos))
		self.vistaLiqJubilado.liqj_importe_total.setText(str(self.model.importe_total))

	def handleSaveEbt(self):
		path = QtWidgets.QFileDialog.getSaveFileName(
			None, 'Save File', "", 'Texto plano(*.txt)'
		)

		if not path[0]:
			return

		ebt_file = open(path[0], "w")

		for row in range(self.model.rowCount(None)):
			line = ""
			item = self.model.listaDebitos[row]
			formattedDec = self.formatDec(item[6])
			line = "{}{}{}                  {}{}{}{}CUOTAS 014{}                                        {}\n".format(
				item[1], item[2],
				"{0:010d}".format(int(item[3])), item[4], item[5],
				"{0:010d}".format(formattedDec), item[7], "{0:015d}".format(item[8]),
				item[9]
			)
			ebt_file.write(line)
			condiciones = [
				("id", "=", item[0])]
			self.model.actualizarDebito(
				debito = {
					'id' : item[0],
					'id_temporal' : int(item[8]),
					'estado' : 'procesando'
					},
				condiciones = condiciones)

		ebt_file.close()
		# ebt_file.save(path[0])

	def formatDec(self, decim):
		decim = decim.split('.')
		return int(decim[0] + decim[1])
