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

#Creacion de la clase detalleAfiliados
class LiquidadorAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		self.vistaLiqAfiliado = uic.loadUi("gui/liquidadores/liquidadorAfiliados.ui", self)

		self.vistaLiqAfiliado.liq_fecha.setDate(date.today())

		self.model = ModeloLiquidador(propiedades = [
			'id', 'fecha_descuento',
			'proveedor_id', 'importe_actual',
			'cuota_actual', 'total_cuotas']
			)
		# FALTAN 2 PROPIEDADES QUE NUNCA SE CREARON EN LA BASE DE DATOS. OTRO ERROR DE DISEÑO.

		self.vistaLiqAfiliado.tbl_liq.setModel(self.model)

		self.vistaLiqAfiliado.btn_procesar_liq.clicked.connect(self.buscarDebitosALiquidar)
		self.vistaLiqAfiliado.btn_procesar_liq.clicked.connect(self.setTotales)

	def getFechaCobro(self):
		diaCobro = self.vistaLiqAfiliado.liq_fecha.date()

		return diaCobro

	def getFechaLiquidacion(self):
		mesALiquidar = self.vistaLiqAfiliado.liq_mes.currentIndex() + 1
		anioALiquidar = int(self.vistaLiqAfiliado.liq_anio.text())
		fechaLiquidacion = date(anioALiquidar, mesALiquidar, 1)

		return fechaLiquidacion

	def buscarDebitosALiquidar(self):
		fecha = self.getFechaLiquidacion()
		self.model.verListaLiquidacion(
			condiciones = [
			("YEAR(fecha_descuento)", "=", fecha.year),
			("MONTH(fecha_descuento)", "=", fecha.month)
			])

		self.vistaLiqAfiliado.tbl_liq.setColumnHidden(0, True)

	def setTotales(self):
		self.vistaLiqAfiliado.liq_cantidad_total.setText(str(self.model.total_debitos))
		self.vistaLiqAfiliado.liq_importe_total.setText(str(self.model.importe_total))
