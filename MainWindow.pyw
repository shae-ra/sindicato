

import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton
from PyQt5 import uic


#Clase heredada de QMainWindow (Constructor de ventanas)
class menuPrincipal(QMainWindow): 
 	#Método constructor de la clase
 	def __init__(self):  
  	#Iniciar el objeto QMainWindow
  		QMainWindow.__init__(self)
  		#Cargar la configuración del archivo .ui en el objeto
  		uic.loadUi("gui/menuPrincipal.ui", self)
  		self.setWindowTitle("Sindicato de Trabajadores Municipales de Merlo")
  		#Mostrar la ventana maximizada
  		self.showMaximized()

  
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = menuPrincipal()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()