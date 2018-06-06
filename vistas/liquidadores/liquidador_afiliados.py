# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic
#import xlwt
from datetime import date

from modelos.modelo_liquidador import ModeloLiquidador

#Creacion de la clase detalleAfiliados
class LiquidadorAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		self.vistaLiqAfiliado = uic.loadUi("gui/liquidadores/liquidadorAfiliados.ui", self)

		self.vistaLiqAfiliado.liq_fecha.setDate(date.today())

		self.model = ModeloLiquidador(propiedades = [
            'debitos.id', 'operacion', 'fecha_descuento',
            'legajo_afiliado', 'banco', 'cbu', 'importe_actual',
            'cuit', 'movimiento', 'empresa']
			)
		# FALTAN 2 PROPIEDADES QUE NUNCA SE CREARON EN LA BASE DE DATOS. OTRO ERROR DE DISEÑO.

		self.vistaLiqAfiliado.tbl_liq.setModel(self.model)

		self.vistaLiqAfiliado.btn_procesar_liq.clicked.connect(self.buscarDebitosALiquidar)
		self.vistaLiqAfiliado.btn_procesar_liq.clicked.connect(self.setTotales)

		self.vistaLiqAfiliado.btn_exportar.clicked.connect(self.procesarDocumento)

	def getFechaCobro(self):
		fechaCobro = self.vistaLiqAfiliado.liq_fecha.date()
		fechaCobro = date(fechaCobro.year(), fechaCobro.month(), fechaCobro.day())

		return fechaCobro

	def getFechaLiquidacion(self):
		mesALiquidar = self.vistaLiqAfiliado.liq_mes.currentIndex() + 1
		anioALiquidar = int(self.vistaLiqAfiliado.liq_anio.text())
		fechaLiquidacion = date(anioALiquidar, mesALiquidar, 1)

		return fechaLiquidacion

	def buscarDebitosALiquidar(self):
		fechaLiquidacion = self.getFechaLiquidacion()
		fechaCobro = self.getFechaCobro()
		self.model.verListaLiquidacion(fechaCobro,
			condiciones = [
			("YEAR(fecha_descuento)", "=", fechaLiquidacion.year),
			("MONTH(fecha_descuento)", "=", fechaLiquidacion.month),
			("estado", "is", "NULL"),
			("cbu", "<>", "''")
			])

		self.vistaLiqAfiliado.tbl_liq.setColumnHidden(0, True)

	def setTotales(self):
		self.vistaLiqAfiliado.liq_cantidad_total.setText(str(self.model.total_debitos))
		self.vistaLiqAfiliado.liq_importe_total.setText(str(self.model.importe_total))

	def procesarDocumento(self):
		# Abre ventana de dialogo para guardar archivo .ebt
		# El nombre por defecto es la fecha de liquidacion
		# Procesa todos los debitos en la ventana
		# Guarda cada linea procesada en el archivo
		# Guarda el archivo en formato .ebt
		# Actualiza la base de datos con id_temporal para todos los debitos

		# fecha = self.vistaLiqAfiliado.liq_fecha.date()
		# self.model.liquidar(fecha)

		self.handleSaveEbt()

	def handleSaveXls(self):
		path = QtWidgets.QFileDialog.getSaveFileName(
			None, 'Save File', '', 'Excel(*.xls)')

		if not path[0]:
			return
		wb = xlwt.Workbook()
		ws = wb.add_sheet('documento')

	def handleSaveEbt(self):
		fechaCobro = self.getFechaCobro()
		path = QtWidgets.QFileDialog.getSaveFileName(
			None, 'Save File', fechaCobro.strftime("%d%m%Y"), 'Texto plano(*.txt)'
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
				item[3], item[4], item[5],
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
