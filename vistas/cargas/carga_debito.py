

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from modelos.modelo_proveedor import ModeloProveedor
from modelos.modelo_debito import ModeloDebito

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase CargaDebito
class CargaDebito(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		# Importamos la vista "carga_debito" y la alojamos dentro de la variable "carga"
		self.v_carga = uic.loadUi("gui/cargas/carga_debito.ui", self)

		self.model_prov = ModeloProveedor(['id'])
		self.model = ModeloDebito()

		self.v_carga.prov_id.setModel(self.model_prov)
