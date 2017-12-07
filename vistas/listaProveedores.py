#El nombre de la clase, tendra el mismo nombre que el archivo.


import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5 import uic


#Creacion de la clase vistaLista
class listaProveedores(QtWidgets.QWidget): 
	def __init__(self):  
		QWidget.__init__(self)  
		#Configuracion del archivo .ui
		uic.loadUi("gui/listas/listaProveedores.ui", self)
		#Titulo de la ventana
		self.setWindowTitle("Busqueda de Proveedores")
