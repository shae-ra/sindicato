#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
# Importamos los archivos .py necesarios de la carpeta: vistas
from vistas.detalles import detalle_proveedores
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from modelos.modelo_proveedor import ModeloProveedor

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase listaProveedores
class ListaProveedores(QtWidgets.QWidget):
	def __init__(self):
		QWidget.__init__(self)
		#Configuracion del archivo .ui
		listadoproveedor = uic.loadUi("gui/listas/listaProveedores.ui", self)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.vd_proveedor = detalle_proveedores.DetalleProveedores()

		self.model = ModeloProveedor(
			propiedades = ['id', 'nombre', 'servicios', 'razon_social', 'calle', 'altura', 'localidad', 'email', 'comision', 'responsable',]
		)

		self.tbl_proveedores.setModel(self.model)
		self.ajustarTabla()

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		self.tbl_proveedores.doubleClicked.connect(self.mostrarDetalleProveedor)
		listadoproveedor.btn_nuevo.clicked.connect(self.mostrarDetalleProveedor)

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def showEvent(self,event):
		self.model.verTablaProveedores()

	def mostrarDetalleProveedor(self, proveedor):
		if proveedor:
			proveedor = self.model.verDetallesProveedor(proveedor)
			self.vd_proveedor.setProveedor(proveedor)
		else:
			self.vd_proveedor.resetProveedor()
		self.vd_proveedor.show()

	def buscarProveedores(self):
		busqueda = self.ln_buscar.text()
		try:
			busqueda = int(busqueda)
			condiciones =  [("id", "LIKE", "'%{}%'".format(busqueda))]
		except:
			condiciones = [("nombre", "LIKE", "'%{}%'".format(busqueda))]

		self.model.verTablaProveedores(condiciones)
		self.ajustarTabla()

	def ajustarTabla(self):
		header = self.tbl_proveedores.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
