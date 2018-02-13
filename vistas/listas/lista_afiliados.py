

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
# Importamos los archivos .py necesarios de la carpeta: vistas
from vistas.detalles import detalle_afiliados
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from modelos.modelo_afiliado import ModeloAfiliado

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase vistaLista
class ListaAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "listaAfiliados" y la alojamos dentro de la variable "vistaLista"
		listadoafiliados = uic.loadUi("gui/listas/listaAfiliados.ui", self)

		self.model = ModeloAfiliado()

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.widgetdelafiliado = detalle_afiliados.DetalleAfiliados()

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		listadoafiliados.btn_nuevo.clicked.connect(self.mostrarDetalleAfiliado)

		self.tbl_articulos.doubleClicked.connect(self.model.verDetallesAfiliado)


	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def mostrarDetalleAfiliado(self):
		self.widgetdelafiliado.show()
