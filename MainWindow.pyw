

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
from vistas.listas import lista_afiliados, lista_proveedores, lista_usuarios, lista_procesador, lista_utilidades
# Importamos los archivos .py necesarios de la carpeta: detalles
from vistas.detalles import detalle_liquidacion
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic



#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase menuPrincipal. Objeto tipo QMainWindow
class MenuPrincipal(QMainWindow):
	#Inicializacion del Objeto MainWindow
	def __init__(self):
		QMainWindow.__init__(self)		
		
		#Importamos la vista "menuPrincipal" y la alojamos dentro de la variable "vistaprincipal"
		vistaprincipal = uic.loadUi("gui/menuPrincipal.ui", self)

		#Tomamos el objeto stackedWidget de la vista principal y lo alojamos en una variable
		self.stacked = vistaprincipal.findChild(QStackedWidget)
		
		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		vla = lista_afiliados.ListaAfiliados()
		vlp = lista_proveedores.ListaProveedores()
		vliq = detalle_liquidacion.DetalleLiquidacion()
		vproc = lista_procesador.ListaProcesador()
		vuser = lista_usuarios.ListaUsuarios()
		vutil = lista_utilidades.ListaUtilidades()

		
		#Creamos una variable del tipo lista que guardara las variables anteriormente declaradas
		self.Vistas = [ vla, vlp, vliq, vuser, vproc, vutil]

		#se crea un ciclo for que indexara las variables
		for index, vista in enumerate(self.Vistas):
			self.stacked.insertWidget(index, vista)
		
		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		self.pushButton_afiliados.clicked.connect(self.seleccionarAfiliados)
		self.pushButton_proveedores.clicked.connect(self.seleccionarProveedores)
		self.pushButton_liquidaciones.clicked.connect(self.seleccionarLiquidacion)
		self.pushButton_procesador.clicked.connect(self.seleccionarProcesador)
		self.pushButton_usuarios.clicked.connect(self.seleccionarUsuarios)
		self.pushButton_utilidades.clicked.connect(self.seleccionarUtilidades)

		#Propiedades de la ventana
		self.showMaximized()
		self.setWindowTitle("Sindicato de Trabajadores Municipales de Merlo")


	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def seleccionarAfiliados(self):
		self.stacked.setCurrentIndex(0)

	def seleccionarProveedores(self):
		self.stacked.setCurrentIndex(1)

	def seleccionarLiquidacion(self):
		self.stacked.setCurrentIndex(2)

	def seleccionarUsuarios(self):
		self.stacked.setCurrentIndex(3)

	def seleccionarProcesador(self):
		self.stacked.setCurrentIndex(4)

	def seleccionarUtilidades(self):
                self.stacked.setCurrentIndex(5)



#======================
#EJECUTAR LA APLICACION
#======================
 
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = MenuPrincipal()
#Mostra la ventana
_ventana.show()
#Ejecutar la aplicación
app.exec_()
