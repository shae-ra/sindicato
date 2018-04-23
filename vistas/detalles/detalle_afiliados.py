#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget
from vistas.cargas import carga_debito
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate, QRegExp
from modelos.modelo_afiliado import ModeloAfiliado
from modelos.modelo_debito import ModeloDebito

from datetime import date


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class DetalleAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		rxCbu = QRegExp("[0-9]{22}")


		# Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		# Agregamos 'self.' al objeto así podemos acceder a él en el resto de las funciones
		self.vd_afiliado = uic.loadUi("gui/detalles/detalleAfiliados.ui", self)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.v_carga = carga_debito.CargaDebito(self)

		self.vd_afiliado.af_cbu.setValidator(QtGui.QRegExpValidator(rxCbu))

		self.model = ModeloAfiliado(parent = self)
		self.model_debito = ModeloDebito(propiedades = [
			"id",
			"legajo_afiliado",
			"fecha_descuento",
			"cuota_actual",
			"total_cuotas"			
			])

		self.vd_afiliado.tbl_debitos.setModel(self.model_debito)

		self.btn_guardar_afiliado.clicked.connect(self.guardarAfiliado)
		self.btn_guardar_cbu.clicked.connect(self.guardarAfiliado)

	def guardarAfiliado(self):
		afiliado = self.getAfiliado()
		self.model.guardarAfiliado(afiliado)

	def guardarCbu(self):
		cbu = self.vd_afiliado.af_cbu.text()
		self.model.modificarCbu(cbu)

	def getAfiliado(self):
		f_ingreso = self.vd_afiliado.af_fecha_ingreso.date()
		f_ingreso = date(f_ingreso.year(), f_ingreso.month(), f_ingreso.day() )

		f_nacimiento = self.vd_afiliado.af_fecha_nacimiento.date()
		f_nacimiento = date(f_nacimiento.year(), f_nacimiento.month(), f_nacimiento.day() )

		try:
			legajo = int(self.vd_afiliado.af_legajo.text())
		except:
			legajo = 0
		try:
			dni = int(self.vd_afiliado.af_dni.text())
		except:
			dni = 0
		try:
			edad = int(self.vd_afiliado.af_edad.text())
		except:
			edad = 0
		try:
			altura = int(self.vd_afiliado.af_altura.text())
		except:
			altura = 0
		try:
			antiguedad = int(self.vd_afiliado.af_antiguedad.text())
		except:
			antiguedad = 0
		try:
			cuil = int(self.vd_afiliado.af_cuil.text())
		except:
			cuil = 0

		afiliado = {

		'legajo' : legajo,
		'dni' : dni,
		'tipo_afiliado' : self.vd_afiliado.af_tipo.currentText(),
		'cuil' : cuil,
		'apellido' : self.vd_afiliado.af_apellido.text(),
		'nombre' : self.vd_afiliado.af_nombre.text(),
		'fecha_nacimiento' : f_nacimiento,
		'edad' : edad,
		'estado_civil' : self.vd_afiliado.af_estado_civil.currentText(),
		'nacionalidad' : self.vd_afiliado.af_nacionalidad.currentText(),
		'calle' : self.vd_afiliado.af_calle.text(),
		'altura' : altura,
		'piso' : self.vd_afiliado.af_piso.text(),
		'depto' : self.vd_afiliado.af_depto.text(),
		'cod_postal' : self.vd_afiliado.af_codigo_postal.text(),
		'barrio' : self.vd_afiliado.af_barrio.text(),
		'localidad' : self.vd_afiliado.af_localidad.currentText(),
		'telefono_particular' : self.vd_afiliado.af_tel_particular.text(),
		'telefono_laboral' : self.vd_afiliado.af_tel_laboral.text(),
		'celular' : self.vd_afiliado.af_celular.text(),
		'email' : self.vd_afiliado.af_email.text(),
		'lugar_trabajo' : self.vd_afiliado.af_lugar_trabajo.text(),
		'antiguedad' : antiguedad,
		'fecha_ingreso' : f_ingreso,
		'jerarquia' : self.vd_afiliado.af_jerarquia.text(),
		'nivel_estudios' : self.vd_afiliado.af_nivel_estudios.currentText(),
		'cbu' : self.vd_afiliado.af_cbu.text(),
		'sucursal' : self.vd_afiliado.af_sucursal.currentText(),

		}

		return afiliado

	def setAfiliado(self, afiliado):
		self.vd_afiliado.af_legajo.setText(str(afiliado[0]))
		self.vd_afiliado.af_dni.setText(str(afiliado[1]))
		self.vd_afiliado.af_tipo.setCurrentText(afiliado[2])
		self.vd_afiliado.af_cuil.setText(str(afiliado[4]))
		self.vd_afiliado.af_apellido.setText(afiliado[5])
		self.vd_afiliado.af_nombre.setText(afiliado[6])
		self.vd_afiliado.af_fecha_nacimiento.setDate(QDate(afiliado[7]))
		self.vd_afiliado.af_edad.setText(str(afiliado[8]))
		self.vd_afiliado.af_estado_civil.setCurrentText(afiliado[9])
		self.vd_afiliado.af_nacionalidad.setCurrentText(afiliado[10])
		self.vd_afiliado.af_calle.setText(afiliado[11])
		self.vd_afiliado.af_altura.setText(str(afiliado[12]))
		self.vd_afiliado.af_piso.setText(afiliado[13])
		self.vd_afiliado.af_depto.setText(afiliado[14])
		self.vd_afiliado.af_codigo_postal.setText(afiliado[15])
		self.vd_afiliado.af_barrio.setText(afiliado[16])
		self.vd_afiliado.af_localidad.setCurrentText(afiliado[17])
		self.vd_afiliado.af_tel_particular.setText(afiliado[18])
		self.vd_afiliado.af_tel_laboral.setText(afiliado[19])
		self.vd_afiliado.af_celular.setText(afiliado[20])
		self.vd_afiliado.af_email.setText(afiliado[21])
		self.vd_afiliado.af_lugar_trabajo.setText(afiliado[22])
		self.vd_afiliado.af_jerarquia.setText(afiliado[23])
		self.vd_afiliado.af_fecha_ingreso.setDate(QDate(afiliado[24]))
		self.vd_afiliado.af_antiguedad.setText(str(afiliado[25]))
		self.vd_afiliado.af_nivel_estudios.setCurrentText(afiliado[26])
		self.vd_afiliado.af_sucursal.setCurrentText(afiliado[28])
		self.vd_afiliado.af_cbu.setText(afiliado[29])

	def resetAfiliado(self):
		self.vd_afiliado.af_legajo.setText('')
		self.vd_afiliado.af_dni.setText('')
		self.vd_afiliado.af_tipo.setCurrentIndex(0)
		self.vd_afiliado.af_cuil.setText('')
		self.vd_afiliado.af_apellido.setText('')
		self.vd_afiliado.af_nombre.setText('')
		self.vd_afiliado.af_fecha_nacimiento.setDate(QDate(date.today()))
		self.vd_afiliado.af_edad.setText('')
		self.vd_afiliado.af_estado_civil.setCurrentIndex(0)
		self.vd_afiliado.af_nacionalidad.setCurrentIndex(0)
		self.vd_afiliado.af_calle.setText('')
		self.vd_afiliado.af_altura.setText('')
		self.vd_afiliado.af_piso.setText('')
		self.vd_afiliado.af_depto.setText('')
		self.vd_afiliado.af_codigo_postal.setText('')
		self.vd_afiliado.af_barrio.setText('')
		self.vd_afiliado.af_localidad.setCurrentIndex(0)
		self.vd_afiliado.af_tel_particular.setText('')
		self.vd_afiliado.af_tel_laboral.setText('')
		self.vd_afiliado.af_celular.setText('')
		self.vd_afiliado.af_email.setText('')
		self.vd_afiliado.af_lugar_trabajo.setText('')
		self.vd_afiliado.af_jerarquia.setText('')
		self.vd_afiliado.af_fecha_ingreso.setDate(QDate(date.today()))
		self.vd_afiliado.af_antiguedad.setText('')
		self.vd_afiliado.af_nivel_estudios.setCurrentIndex(0)
		self.vd_afiliado.af_sucursal.setCurrentIndex(0)
		self.vd_afiliado.af_cbu.setText('')

	def showEvent(self, event):
		self.vd_afiliado.tabWidget.setCurrentIndex(0)
		self.vd_afiliado.pushButton_ingresarDebito.clicked.connect(self.mostrarCarga)
		self.verListaDebitos()
		# Accedo al objeto 'tabWidget' que es hijo de el objeto 'vd_afiliado' y además llamo a la función setCurrentIndex()
		# la funcion setCurrentIndex pertence al último hijo llamado.

	def verListaDebitos(self):
		condiciones = [("legajo_afiliado", "=", "'{}'".format(self.vd_afiliado.af_legajo.text()))]
		self.model_debito.verTablaDebitos(condiciones)

	def mostrarCarga(self):
		# if self.model.tieneCbu():
		self.v_carga.show()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
