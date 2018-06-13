import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
# Importamos el modulo uic necesario para levantar un archivo .ui

class NoDisponible(QtWidgets.QWidget): 
	def __init__(self):  
		QWidget.__init__(self)  
		#Configuracion del archivo .ui
		noDisponible = uic.loadUi("gui/utilidades/modulo_nodisponible.ui", self)