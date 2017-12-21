

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
# Importamos los archivos .py necesarios de la carpeta: vistas 
from vistas import liqAfiliados
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class liquidaciones(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):  
		QWidget.__init__(self)  
		
		#Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		vistaLiquidaciones = uic.loadUi("gui/liquidacion/liquidaciones.ui", self)

		#Tomamos el objeto stackedWidget de la vista principal y lo alojamos en una variable
		self.stk = vistaLiquidaciones.findChild(QStackedWidget)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		liqAf = liqAfiliados.liquidacionParaAfiliados()
