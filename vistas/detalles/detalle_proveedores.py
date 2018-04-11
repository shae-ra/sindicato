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
from PyQt5.QtCore import Qt
from modelos.modelo_proveedor import ModeloProveedor

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class DetalleProveedores(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		self.vd_proveedor = uic.loadUi("gui/detalles/detalleProveedor.ui", self)
		self.setWindowTitle("Consulta del Proveedor")

		self.model = ModeloProveedor()

		self.vd_proveedor.btn_guardar.clicked.connect(self.guardarProveedor)

		self.setValidationRules()

	def guardarProveedor(self):
		proveedor = self.getProveedor()
		self.model.guardarProveedor(proveedor)

	def getProveedor(self):
		try:
			id = int(self.vd_proveedor.prov_id.text())
		except:
			id = 0
		try:
			altura = int(self.vd_proveedor.prov_altura.text())
		except:
			altura = 0
		try:
			cuit = int(self.vd_proveedor.prov_cuit.text())
		except:
			cuit = 0
		try:
			cuenta = int(self.vd_proveedor.prov_cuenta.text())
		except:
			cuenta = 0

		proveedor = {
			'id' : id,
			'nombre' : self.vd_proveedor.prov_nombre.text(),
			'servicios' : self.vd_proveedor.prov_servicios.text(),
			'calle' : self.vd_proveedor.prov_calle.text(),
			'altura' : altura,
			'localidad' : self.vd_proveedor.prov_localidad.text(),
			'telefono' : self.vd_proveedor.prov_telefono.text(),
			'celular' : self.vd_proveedor.prov_celular.text(),
			'email' : self.vd_proveedor.prov_email.text(),
			'cuit' : cuit,
			'razon_social' : self.vd_proveedor.prov_razon_social.text(),
			'cbu' : self.vd_proveedor.prov_cbu.text(),
			'banco' : self.vd_proveedor.prov_banco.text(),
			'cuenta' : cuenta,
			'comision' : self.vd_proveedor.prov_comision.text(),
			'responsable' : self.vd_proveedor.prov_responsable.text(),
			'forma_pago' : self.vd_proveedor.prov_forma_pago.text(),
			'notas' : self.vd_proveedor.prov_notas.toPlainText()
		}

		return proveedor

	def setProveedor(self, proveedor):
		self.vd_proveedor.prov_id.setText(str(proveedor[0])),
		self.vd_proveedor.prov_nombre.setText(proveedor[1]),
		self.vd_proveedor.prov_servicios.setText(proveedor[2]),
		self.vd_proveedor.prov_calle.setText(proveedor[3]),
		self.vd_proveedor.prov_altura.setText(str(proveedor[4])),
		self.vd_proveedor.prov_localidad.setText(proveedor[5]),
		self.vd_proveedor.prov_telefono.setText(proveedor[6]),
		self.vd_proveedor.prov_celular.setText(proveedor[7]),
		self.vd_proveedor.prov_email.setText(proveedor[8]),
		self.vd_proveedor.prov_cuit.setText(str(proveedor[9])),
		self.vd_proveedor.prov_razon_social.setText(proveedor[10]),
		self.vd_proveedor.prov_cbu.setText(proveedor[11]),
		self.vd_proveedor.prov_banco.setText(proveedor[12]),
		self.vd_proveedor.prov_cuenta.setText(str(proveedor[13])),
		self.vd_proveedor.prov_comision.setText(proveedor[14]),
		self.vd_proveedor.prov_responsable.setText(proveedor[15]),
		self.vd_proveedor.prov_forma_pago.setText(proveedor[16]),
		self.vd_proveedor.prov_notas.setText(proveedor[17])

	def setValidationRules(self):
		pass

	def resetProveedor(self):
		self.vd_proveedor.prov_id.setText(''),
		self.vd_proveedor.prov_nombre.setText(''),
		self.vd_proveedor.prov_servicios.setText(''),
		self.vd_proveedor.prov_calle.setText(''),
		self.vd_proveedor.prov_altura.setText(''),
		self.vd_proveedor.prov_localidad.setText(''),
		self.vd_proveedor.prov_telefono.setText(''),
		self.vd_proveedor.prov_celular.setText(''),
		self.vd_proveedor.prov_email.setText(''),
		self.vd_proveedor.prov_cuit.setText(''),
		self.vd_proveedor.prov_razon_social.setText(''),
		self.vd_proveedor.prov_cbu.setText(''),
		self.vd_proveedor.prov_banco.setText(''),
		self.vd_proveedor.prov_cuenta.setText(''),
		self.vd_proveedor.prov_comision.setText(''),
		self.vd_proveedor.prov_responsable.setText(''),
		self.vd_proveedor.prov_forma_pago.setText(''),
		self.vd_proveedor.prov_notas.setText('')

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
