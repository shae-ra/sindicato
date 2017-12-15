

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
from vistas import detalleProveedores
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase listaProveedores
class listaProveedores(QtWidgets.QWidget): 
	def __init__(self):  
		QWidget.__init__(self)  
		#Configuracion del archivo .ui
		vistaListaProveedor = uic.loadUi("gui/listas/listaProveedores.ui", self)
		#Titulo de la ventana
		self.setWindowTitle("Busqueda de Proveedores")

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.detalleProveedor = detalleProveedores.detalleProveedores()

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		vistaListaProveedor.btn_nuevo.clicked.connect(self.mostrarDetalleProveedor)

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================
	
	def mostrarDetalleProveedor(self):
		self.detalleProveedor.show()