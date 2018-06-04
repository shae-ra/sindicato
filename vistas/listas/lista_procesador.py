

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


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase listaProveedores
class ListaProcesador(QtWidgets.QWidget):
	def __init__(self):
		QWidget.__init__(self)
		#Configuracion del archivo .ui
		self.listaProcesador = uic.loadUi("gui/listas/listaProcesador.ui", self)

		self.listaProcesador.btn_buscar_bet.clicked.connect(self.handleOpenBet)

	def handleOpenBet(self):

		path = QtWidgets.QFileDialog.getOpenFileName(
			self, 'Open File', "", "Texto plano (*.txt)"
		)

		print(path[0])

		bet_file = open(path[0], "r")

		bet_file.close()
