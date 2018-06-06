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
from PyQt5.QtCore import Qt, QRegExp
from modelos.modelo_proveedor import ModeloProveedor

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleproveedors
class DetalleProveedores(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleproveedors" y la alojamos dentro de la variable "vistaDetalle"
		self.vd_proveedor = uic.loadUi("gui/detalles/detalleProveedor.ui", self)
		self.setRegex()
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


	def setRegex(self):
		rxNombre = QRegExp("[a-z0-9]{50}")
		rxServicios = QRegExp("[a-z0-9]{100}")
		#rxDni = QRegExp("\d{8,8}")
		#rxCuil = QRegExp("[0-9]{11,11}")
		#rxNombreApellido = QRegExp("[A-Z\s]{50}")
		rxCalle = QRegExp("[a-z0-9]{80}")
		rxAltura = QRegExp("\d{8}")
		rxLocalidad = QRegExp("[a-z0-9]{50}")
		#rxPiso = QRegExp(".{10}")
		#rxDepto = QRegExp(".{4}")
		#rxCodPostal = QRegExp(".{20}")
		#rxBarrio = QRegExp("[a-z0-9]{80}")
		rxTelefono = QRegExp("[\d\s()-]{20}")
		rxCelular = QRegExp("[\d\s()-]{20}")
		rxEmail = QRegExp("[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}")
		rxCuit = QRegExp("[0-9]{11,11}")
		rxRazon_social = QRegExp("[a-z0-9]{50}")
		rxCbu = QRegExp("[0-9]{22}")
		rxBanco = QRegExp("[a-z0-9]{60}")
		rxCuenta = QRegExp("[0-9]{16}")
		rxComision = QRegExp("[a-z0-9]{40}")
		rxResponsable = QRegExp("[a-z0-9]{40}")
		rxForma_pago = QRegExp("[a-z0-9]{80}")
		#rxNotas = QRegExp("[a-z0-9]{500}")

		self.vd_proveedor.prov_nombre.setValidator(QtGui.QRegExpValidator(rxNombre))
		self.vd_proveedor.prov_servicios.setValidator(QtGui.QRegExpValidator(rxServicios))
		self.vd_proveedor.prov_calle.setValidator(QtGui.QRegExpValidator(rxCalle))
		self.vd_proveedor.prov_altura.setValidator(QtGui.QRegExpValidator(rxAltura))
		self.vd_proveedor.prov_localidad.setValidator(QtGui.QRegExpValidator(rxLocalidad))
		self.vd_proveedor.prov_telefono.setValidator(QtGui.QRegExpValidator(rxTelefono))
		self.vd_proveedor.prov_celular.setValidator(QtGui.QRegExpValidator(rxCelular))
		self.vd_proveedor.prov_email.setValidator(QtGui.QRegExpValidator(rxEmail))
		self.vd_proveedor.prov_cuit.setValidator(QtGui.QRegExpValidator(rxCuit))
		self.vd_proveedor.prov_razon_social.setValidator(QtGui.QRegExpValidator(rxRazon_social))
		self.vd_proveedor.prov_cbu.setValidator(QtGui.QRegExpValidator(rxCbu))
		self.vd_proveedor.prov_banco.setValidator(QtGui.QRegExpValidator(rxBanco))
		self.vd_proveedor.prov_cuenta.setValidator(QtGui.QRegExpValidator(rxCuenta))
		self.vd_proveedor.prov_comision.setValidator(QtGui.QRegExpValidator(rxComision))
		self.vd_proveedor.prov_responsable.setValidator(QtGui.QRegExpValidator(rxResponsable))
		self.vd_proveedor.prov_forma_pago.setValidator(QtGui.QRegExpValidator(rxForma_pago))
		#self.vd_proveedor.prov_notas.setValidator(QtGui.QRegExpValidator(rxNotas))
