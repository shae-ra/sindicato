

import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
from vistas import listaAfiliados, listaProveedores, liquidador
from PyQt5 import uic

#Creacion de la clase menuPrincipal. Objeto tipo QMainWindow
class menuPrincipal(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		#Importamos la vista "menuPrincipal"
		vista_principal = uic.loadUi("gui/menuPrincipal.ui", self)

		self.stacked = vista_principal.findChild(QStackedWidget)
		
		#variable que aloja la vista de lista afiliados
		vla = listaAfiliados.listaAfiliados()
		vlp = listaProveedores.listaProveedores()
		vliq = liquidador.liquidador()

		
		#Creamos una lista que guardara la vista
		self.Vistas = [ vla, vlp, vliq ]

		#se crea un ciclo for que indexara la lista con las vistas
		for index, vista in enumerate(self.Vistas):
			self.stacked.insertWidget(index, vista)

		#Tomamos el evento click del boton:	
		self.pushButton_afiliados.clicked.connect(self.seleccionar_afiliados)
		self.pushButton_proveedores.clicked.connect(self.seleccionar_proveedores)
		self.pushButton_liquidaciones.clicked.connect(self.seleccionar_liquidacion)
		self.setWindowTitle("Sindicato de Trabajadores Municipales de Merlo")
		self.showMaximized()

	def seleccionar_afiliados(self):
		self.stacked.setCurrentIndex(0)

	def seleccionar_proveedores(self):
		self.stacked.setCurrentIndex(1)

	def seleccionar_liquidacion(self):
		self.stacked.setCurrentIndex(2)

  
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = menuPrincipal()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()