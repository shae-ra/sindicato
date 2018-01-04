

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
from vistas.cargas import carga_debito
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic
from PyQt5.QtCore import Qt


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class DetalleAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		# Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		# Agregamos 'self.' al objeto así podemos acceder a él en el resto de las funciones
		self.widgetafiliado = uic.loadUi("gui/detalles/detalleAfiliados.ui", self)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.widgetdecarga = carga_debito.CargaDebito()

	def showEvent(self, event):
		self.widgetafiliado.tabWidget.setCurrentIndex(0)
		self.widgetafiliado.pushButton_ingresarDebito.clicked.connect(self.mostrarCarga)
		# Accedo al objeto 'tabWidget' que es hijo de el objeto 'widgetafiliado' y además llamo a la función setCurrentIndex()
		# la funcion setCurrentIndex pertence al último hijo llamado.

	def mostrarCarga(self):
		self.widgetdecarga.show()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
