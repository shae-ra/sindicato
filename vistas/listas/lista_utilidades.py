#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from vistas.utilidades import red

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase listaProveedores
class ListaUtilidades(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(ListaUtilidades, self).__init__(parent)
		# QWidget.__init__(self)
		#Configuracion del archivo .ui
		listaUtilidades = uic.loadUi("gui/listas/listaUtilidades.ui", self)

		# vadb =
		vred = red.VistaRed(self)
		# vela =

		self.vistas = [ vred ]
		self.stacked = listaUtilidades.findChild(QtWidgets.QStackedWidget)

		for index, vista in enumerate(self.vistas):
			self.stacked.insertWidget(index, vista)

		self.seleccionarConfigurarRed()

	def seleccionarActDB(self):
		pass

	def seleccionarExportarListado(self):
		pass

	def seleccionarConfigurarRed(self):
		self.stacked.setCurrentIndex(0)
