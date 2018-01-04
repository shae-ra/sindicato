

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
from vistas.detalles import detalle_usuarios
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase listaProveedores
class ListaUsuarios(QtWidgets.QWidget): 
	def __init__(self):  
		QWidget.__init__(self)  
		#Configuracion del archivo .ui
		listadodeusuarios = uic.loadUi("gui/listas/listaUsuarios.ui", self)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.widgetdelusuario = detalle_usuarios.DetalleUsuarios()

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		listadodeusuarios.btn_nuevo.clicked.connect(self.mostrarDetalledelUsuario)

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================
	
	def mostrarDetalledelUsuario(self):
		self.widgetdelusuario.show()