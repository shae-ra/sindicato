#El nombre de la clase, tendra el mismo nombre que el archivo.


import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
from vistas import detalleAfiliados
from PyQt5 import uic


ventanaNueva = detalleAfiliados.detalleAfiliados()

#Creacion de la clase vistaLista
class listaAfiliados(QtWidgets.QWidget): 
	def __init__(self):  
		QWidget.__init__(self)  
		#Configuracion del archivo .ui
		uic.loadUi("gui/listas/listaAfiliados.ui", self)
		#Titulo de la ventana
		self.setWindowTitle("Busqueda de afiliados")
		self.ventanaNueva = detalleAfiliados()
		self.btn_nvo.clicked.connect(self.mostrarDetalleAfiliados)

	def mostrarDetalleAfiliados(self):
		self.ventanaNueva.exec_() 

