#El nombre de la clase, tendra el mismo nombre que el archivo.


import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
from vistas import detalleAfiliados
from PyQt5 import uic


#Creacion de la clase vistaLista
class listaAfiliados(QtWidgets.QWidget):
	def __init__(self):
		QWidget.__init__(self)
		#Configuracion del archivo .ui
		vista = uic.loadUi("gui/listas/listaAfiliados.ui", self)
		#Titulo de la ventana
		self.setWindowTitle("Busqueda de afiliados")

		#declaramos una variable para alojar a la clase "detalleAfiliados()" dentro del archivo "detalleAfiliados"
		self.detalle = detalleAfiliados.detalleAfiliados()

		#se ejecuta la funcion "motrarDetalle" al presionar btn_nuevo
		vista.btn_nuevo.clicked.connect(self.mostrarDetalle)

	#Creamos la funcion que ejecutara la pantalla DetalleAfiliados
	def mostrarDetalle(self):
		self.detalle.show()
