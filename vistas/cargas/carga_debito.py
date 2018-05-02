

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
from PyQt5.QtCore import Qt
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from datetime import date

from modelos.modelo_proveedor import ModeloProveedor
from modelos.modelo_debito import ModeloDebito

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase CargaDebito
class CargaDebito(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self, parent = None):
		QWidget.__init__(self, parent = None)

		self.parent = parent
		# Importamos la vista "carga_debito" y la alojamos dentro de la variable "carga"
		self.v_carga = uic.loadUi("gui/cargas/carga_debito.ui", self)

		self.model_prov = ModeloProveedor(propiedades = ['id', 'nombre'])
		self.model = ModeloDebito()

		self.v_carga.prov_id.setModel(self.model_prov)
		self.v_carga.prov_id.currentIndexChanged.connect(self.__disableComision)

		self.v_carga.btn_confirmar.clicked.connect(self.guardarDebito)

		self.v_carga.deb_total_cuotas.textChanged.connect(self.__calcularTotalACobrar)
		self.v_carga.deb_importe_cuota.textChanged.connect(self.__calcularTotalACobrar)

	def guardarDebito(self):
		debito = self.getDebito()
		if debito:
			self.model.guardarDebito(debito)
		else:
			#observer.msg("No se puede cargar el debito")
			return

	def getDebito(self):
		if self.v_carga.deb_importe_total.text() != "" and self.v_carga.deb_importe_total.text() != "0":
			print("TRUUUUU")
			debito = {
			"legajo_afiliado" : self.parent.vd_afiliado.af_legajo.text(),
			"fecha_descuento" : date(
				int(self.v_carga.deb_fecha_anio.text()),
				int(self.v_carga.deb_fecha_mes.text()),
				1),
			"fecha_carga_inicial" : date.today(),
			"proveedor_id" : int(self.v_carga.prov_id.currentText().split("-")[0]),
			"total_cuotas" : int(self.v_carga.deb_total_cuotas.text()),
			"importe_actual" : int(self.v_carga.deb_importe_cuota.text()),
			"importe_total" : int(self.v_carga.deb_importe_total.text()),
			"n_credito" : self.v_carga.deb_orden.text()
			}

			print(debito)
			return debito

	def showEvent(self, event):
		self.model_prov.verListaProveedores()

	def __calcularTotalACobrar(self):
		cantidad_cuotas = 0
		importe = 0
		try:
			cantidad_cuotas = int(self.v_carga.deb_total_cuotas.text())
			importe = int(self.v_carga.deb_importe_cuota.text())
		except ValueError:
			total_a_cobrar = 0
		total_a_cobrar = cantidad_cuotas * importe

		self.v_carga.deb_importe_total.setText(str(total_a_cobrar))

	def __disableComision(self):
		if int(self.v_carga.prov_id.currentText().split("-")[0]) == 7:
			self.v_carga.deb_orden.setEnabled(True)
		else:
			self.v_carga.deb_orden.setEnabled(False)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
