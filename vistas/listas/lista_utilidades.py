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
from vistas.listas import lista_usuarios

from PyQt5 import uic

from vistas.utilidades import red, nodisponible, impresora

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
		vusuarios = lista_usuarios.ListaUsuarios()
		vnodisponible = nodisponible.NoDisponible()
		vimpresora = impresora.VistaImpresora(self)
		# vela =

		self.vistas = [ vred.vista, vusuarios, vnodisponible, vimpresora.vista]
		self.stacked = listaUtilidades.stackedWidget

		for index, vista in enumerate(self.vistas):
			self.stacked.insertWidget(index, vista)

		self.gestion_usuarios.clicked.connect(self.seleccionarListadeUsuarios)
		self.configurar_red.clicked.connect(self.seleccionarConfigurarRed)
		self.configurar_impresora.clicked.connect(self.seleccionarConfigurarImpresora)
		self.pushButton_2.clicked.connect(self.seleccionarNoDisponible)
		self.pushButton_5.clicked.connect(self.seleccionarNoDisponible)
		self.pushButton_6.clicked.connect(self.seleccionarNoDisponible)
		self.pushButton_7.clicked.connect(self.seleccionarNoDisponible)
		self.pushButton.clicked.connect(self.seleccionarNoDisponible)

	def seleccionarActDB(self):
		pass

	def seleccionarExportarListado(self):
		pass

	def seleccionarConfigurarRed(self):
		self.stacked.setCurrentIndex(0)

	def seleccionarListadeUsuarios(self):
		self.stacked.setCurrentIndex(1)

	def seleccionarNoDisponible(self):
		self.stacked.setCurrentIndex(2)

	def seleccionarConfigurarImpresora(self):
		self.stacked.setCurrentIndex(3)
