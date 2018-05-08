

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget, QStackedWidget
# Importamos los archivos .py necesarios de la carpeta: detalles
from vistas.liquidadores import liquidador_afiliados, liquidador_jubilados
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class DetalleLiquidacion(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		widgetliquidacion = uic.loadUi("gui/detalles/detalleLiquidacion.ui", self)

		#Tomamos el objeto stackedWidget del widget de liquidacion y lo alojamos en una variable
		self.stk = widgetliquidacion.findChild(QStackedWidget)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		liqafi = liquidador_afiliados.LiquidadorAfiliados()
		liqjub = liquidador_jubilados.LiquidadorJubilados()

		#Creamos una variable del tipo lista que guardara las variables anteriormente declaradas
		self.subwidgets = [ liqafi, liqjub]

		#se crea un ciclo for que indexara las variables
		for index, vista in enumerate(self.subwidgets):
			self.stk.insertWidget(index, vista)

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		self.pushButton_activos.clicked.connect(self.seleccionarActivos)
		self.pushButton_jubilados.clicked.connect(self.seleccionarJubilados)

		self.seleccionarActivos()

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def seleccionarActivos(self):
		self.stk.setCurrentIndex(0)

	def seleccionarJubilados(self):
		self.stk.setCurrentIndex(1)
