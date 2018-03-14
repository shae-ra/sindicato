

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

from modelos.modelo_proveedores import ModeloProveedores

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
		self.widgetdelproveedor = detalle_proveedores.DetalleProveedores()

		self.model = ModeloProveedores(
			propiedades = ['nombre', 'servicios', 'razon_social', 'email']
		)
		self.tbl_proveedores.setModel(self.model)

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		listadoproveedor.btn_nuevo.clicked.connect(self.mostrarDetalleProveedor)

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def showEvent(self,event):
		self.model.verListaProveedores()

	def mostrarDetalleProveedor(self):
		self.widgetdelproveedor.show()
