

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
from vistas import listaAfiliados, listaProveedores, liquidador, procesador
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic



#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase menuPrincipal. Objeto tipo QMainWindow
class menuPrincipal(QMainWindow):
	#Inicializacion del Objeto MainWindow
	def __init__(self):
		QMainWindow.__init__(self)		
		
		#Importamos la vista "menuPrincipal" y la alojamos dentro de la variable "vista_principal"
		vista_principal = uic.loadUi("gui/menuPrincipal.ui", self)

		#Tomamos el objeto stackedWidget de la vista principal y lo alojamos en una variable
		self.stacked = vista_principal.findChild(QStackedWidget)
		
		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		vla = listaAfiliados.listaAfiliados()
		vlp = listaProveedores.listaProveedores()
		vliq = liquidador.liquidador()

		
		#Creamos una variable del tipo lista que guardara las variables anteriormente declaradas
		self.Vistas = [ vla, vlp, vliq]

		#se crea un ciclo for que indexara las variables
		for index, vista in enumerate(self.Vistas):
			self.stacked.insertWidget(index, vista)
		
		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		self.pushButton_afiliados.clicked.connect(self.seleccionar_afiliados)
		self.pushButton_proveedores.clicked.connect(self.seleccionar_proveedores)
		self.pushButton_liquidaciones.clicked.connect(self.seleccionar_liquidacion)

		#Propiedades de la ventana
		self.showMaximized()
		self.setWindowTitle("Sindicato de Trabajadores Municipales de Merlo")


	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def seleccionar_afiliados(self):
		self.stacked.setCurrentIndex(0)

	def seleccionar_proveedores(self):
		self.stacked.setCurrentIndex(1)

	def seleccionar_liquidacion(self):
		self.stacked.setCurrentIndex(2)




#======================
#EJECUTAR LA APLICACION
#======================
 
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = menuPrincipal()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()