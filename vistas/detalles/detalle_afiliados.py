#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QTabWidget, QMessageBox
from vistas.cargas import carga_debito
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate, QRegExp
from modelos.modelo_afiliado import ModeloAfiliado
from modelos.modelo_debito import ModeloDebito
from modelos.modelo_familiares import ModeloFamiliares
from modelos.modelo_servicios import ModeloServicios
from modelos.modelo_servicios_afiliados import ModeloServiciosAfiliados

from datetime import date


#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase detalleAfiliados
class DetalleAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)
		# Importamos la vista "detalleAfiliados" y la alojamos dentro de la variable "vistaDetalle"
		# Agregamos 'self.' al objeto así podemos acceder a él en el resto de las funciones
		self.vd_afiliado = uic.loadUi("gui/detalles/detalleAfiliados.ui", self)

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.v_carga = carga_debito.CargaDebito(self)

		self.setRegex()

		self.model = ModeloAfiliado(parent = self)
		self.model_debito = ModeloDebito(propiedades = [
			"debitos.id",
			"fecha_descuento",
			"nombre",
			"n_orden",
			# "proveedor_id",
			"importe_actual",
			"cuota_actual",
			"total_cuotas",
			"fecha_carga_inicial"
			])
		self.model_historial = ModeloDebito(propiedades = [
			"fecha_descuento",
			"nombre",
			"n_orden",
			# "proveedor_id",
			"importe_actual",
			"cuota_actual",
			"total_cuotas",
			"fecha_carga_inicial",
			"estado",
			"motivo",
		])

		self.model_familiares = ModeloFamiliares()
		self.model_servicios = ModeloServicios()
		self.model_servicios_afiliado = ModeloServiciosAfiliados()

		self.vd_afiliado.tbl_debitos.setModel(self.model_debito)
		self.vd_afiliado.tbl_historial_debitos.setModel(self.model_historial)
		self.vd_afiliado.tbl_familiares.setModel(self.model_familiares)
		self.vd_afiliado.tbl_servicios.setModel(self.model_servicios_afiliado)
		self.vd_afiliado.serv_tipo.setModel(self.model_servicios)

		self.vd_afiliado.fam_fecha_nacimiento.dateChanged.connect(self.setEdadFamiliar)
		self.vd_afiliado.af_fecha_nacimiento.dateChanged.connect(self.setEdadAfiliado)
		self.vd_afiliado.af_fecha_ingreso.dateChanged.connect(self.setAntiguedad)

		self.btn_asociar_servicio.clicked.connect(self.asociarServicio)
		self.btn_guardar_afiliado.clicked.connect(self.guardarAfiliado)
		self.btn_guardar_cbu.clicked.connect(self.guardarAfiliado)
		self.btn_guardar_familiar.clicked.connect(self.guardarFamiliar)
		self.btn_guardar_servicio.clicked.connect(self.guardarServicio)

	def asociarServicio(self):
		id_servicio = self.model_servicios.getId(self.vd_afiliado.serv_tipo.currentText())
		fecha = self.vd_afiliado.serv_fecha.date()
		fecha = self.__convertirFecha(fecha)
		servicio = {
			'id_servicio' : id_servicio,
			'legajo_afiliado' : self.vd_afiliado.af_legajo.text(),
			'fecha' : fecha,
			'cantidad' : self.vd_afiliado.serv_cantidad.text(),
			'detalle' :self.vd_afiliado.serv_detalles.text()
		}
		self.model_servicios_afiliado.asociarServicio(servicio)

	def confirmarOperacion(self):
		msg = QtWidgets.QMessageBox()

		reply = msg.question(self, "Confirmar operación", "¿Está seguro de realizar esta operación?",
			QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

		msg.show()

		if reply == QtWidgets.QMessageBox.Yes:
			return True
		else:
			return False

	def guardarAfiliado(self):
		afiliado = self.getAfiliado()
		self.model.guardarAfiliado(afiliado)
		cdiag = self.operacionCompletada()
		close = self.close()

	def guardarFamiliar(self):
		fechaNacimiento = self.vd_afiliado.fam_fecha_nacimiento.date()
		fechaNacimiento = self.__convertirFecha(fechaNacimiento)

		familiar = {
			'familiares.dni' : self.vd_afiliado.fam_dni.text(),
			'familiares.relacion' : self.vd_afiliado.fam_relacion.currentText(),
			'familiares.nombre' : self.vd_afiliado.fam_nombre.text(),
	        'familiares.apellido' : self.vd_afiliado.fam_apellido.text(),
			'familiares.fecha_nacimiento' : fechaNacimiento,
	        'familiares.edad' : self.vd_afiliado.fam_edad.text(),
			'familiares.nivel_estudios' : self.vd_afiliado.fam_nivel_estudios.currentText(),
			'familiares.legajo_afiliado' : self.vd_afiliado.af_legajo.text()
		}

		condiciones = [("afiliados.legajo", "=", familiar['familiares.legajo_afiliado'])]

		self.model_familiares.guardarFamiliar(familiar)
		self.resetFamiliar()

	def guardarCbu(self):
		cbu = self.vd_afiliado.af_cbu.text()
		self.model.modificarCbu(cbu)

	def guardarServicio(self):
		servicio = {
			'nombre' : self.vd_afiliado.serv_nombre.text()
		}

		if self.confirmarOperacion():
			self.model_servicios.guardarServicio(servicio)
			self.vd_afiliado.serv_nombre.setText('')

	def getAfiliado(self):
		f_ingreso = self.vd_afiliado.af_fecha_ingreso.date()
		f_ingreso = date(f_ingreso.year(), f_ingreso.month(), f_ingreso.day() )

		f_nacimiento = self.vd_afiliado.af_fecha_nacimiento.date()
		f_nacimiento = date(f_nacimiento.year(), f_nacimiento.month(), f_nacimiento.day() )

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

		'legajo' : self.vd_afiliado.af_legajo.text(),
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

	def operacionCompletada(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Operación Exitosa     ")
		msg.setWindowTitle("...")
		retval = msg.exec_()

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
		self.vd_afiliado.btn_ingresar_debito.clicked.connect(self.mostrarCarga)
		self.verListaDebitos()
		self.verListaFamiliares()
		self.verHistorialDebitos()
		self.model_servicios.verListaServicios()
		self.model_servicios_afiliado.verTablaServicios(self.vd_afiliado.af_legajo.text())

		self.vd_afiliado.serv_tipo.setCurrentIndex(0)

		# Accedo al objeto 'tabWidget' que es hijo de el objeto 'vd_afiliado' y además llamo a la función setCurrentIndex()
		# la funcion setCurrentIndex pertence al último hijo llamado.

	def verListaDebitos(self):
		condiciones = [
			("legajo_afiliado", "=", "'{}'".format(self.vd_afiliado.af_legajo.text())),
			("estado", "IS", "NULL")
			]
		orden = ("fecha_descuento", "ASC")
		self.model_debito.verTablaDebitos(condiciones, orden, fechas = [1, 7])
		self.tbl_debitos.setColumnHidden(0, True)

	def verListaFamiliares(self):
		condiciones = [
			("legajo_afiliado", "=", "'{}'".format(self.vd_afiliado.af_legajo.text())),
		]
		self.model_familiares.verListaFamiliares(condiciones)

	def verHistorialDebitos(self):
		condiciones = [
			("legajo_afiliado", "=", "'{}'".format(self.vd_afiliado.af_legajo.text())),
			("estado", "IS NOT", "NULL"),
			]
		orden = ("fecha_descuento", "DESC")
		self.model_historial.verTablaDebitos(condiciones, orden, fechas = [0, 6])

	def mostrarCarga(self):
		# if self.model.tieneCbu():
		if len(self.vd_afiliado.af_cbu.text()) != 22:

			msg = QtWidgets.QMessageBox()

			reply = msg.question(self, "Alerta", "El CBU del afiliado no tiene 22 caracteres",
				QtWidgets.QMessageBox.Ok)
			msg.show()
			return False
		self.v_carga.show()

	def setEdad(self, fecha):
		hoy = date.today()
		fecha = self.__convertirFecha(fecha)
		edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
		return str(edad)

	def setEdadFamiliar(self):

		# today = date.today()
		fechaNacimiento = self.vd_afiliado.fam_fecha_nacimiento.date()
		# self.vd_afiliado.fam_edad.setText(str(edad))

		self.vd_afiliado.fam_edad.setText(self.setEdad(fechaNacimiento))

	def setAntiguedad(self):
		fechaIngreso = self.vd_afiliado.af_fecha_ingreso.date()
		self.vd_afiliado.af_antiguedad.setText(self.setEdad(fechaIngreso))

	def setEdadAfiliado(self):
		fechaNacimiento = self.vd_afiliado.af_fecha_nacimiento.date()
		self.vd_afiliado.af_edad.setText(self.setEdad(fechaNacimiento))

	def __convertirFecha(self, fecha):
		return date(fecha.year(), fecha.month(), fecha.day())

	def resetFamiliar(self):
		self.vd_afiliado.fam_dni.setText(''),
		self.vd_afiliado.fam_relacion.setCurrentIndex(0),
		self.vd_afiliado.fam_nombre.setText(''),
		self.vd_afiliado.fam_apellido.setText(''),
		self.vd_afiliado.fam_edad.setText(''),
		self.vd_afiliado.fam_nivel_estudios.setCurrentIndex(0),
		self.vd_afiliado.af_legajo.setText('')

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()

	def setRegex(self):
		rxCbu = QRegExp("[0-9]{22}")
		rxLegajo = QRegExp("[0-9]{8,8}")
		rxDni = QRegExp("\d{8,8}")
		rxCuil = QRegExp("[0-9]{11,11}")
		rxNombreApellido = QRegExp("[A-Z\s]{50}")
		rxCalle = QRegExp("[A-Z0-9.\s]{80}") #("\D{50}")
		rxAltura = QRegExp("\d{8}")
		rxPiso = QRegExp(".{10}")
		rxDepto = QRegExp(".{4}")
		rxCodPostal = QRegExp(".{20}")
		rxBarrio = QRegExp("[A-Z0-9.\s]{80}")
		rxTelefono = QRegExp("[\d\s()-]{20}")
		rxEmail = QRegExp("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[A-Z]{2,4}")
		rxLugarTrabajo = QRegExp("[A-Z0-9.\s]{80}")
		rxJerarquia = QRegExp("[A-Z0-9.\s]{80}")

		self.vd_afiliado.af_cbu.setValidator(QtGui.QRegExpValidator(rxCbu))
		self.vd_afiliado.af_apellido.setValidator(QtGui.QRegExpValidator(rxNombreApellido))
		self.vd_afiliado.af_legajo.setValidator(QtGui.QRegExpValidator(rxLegajo))
		self.vd_afiliado.af_dni.setValidator(QtGui.QRegExpValidator(rxDni))
		self.vd_afiliado.af_nombre.setValidator(QtGui.QRegExpValidator(rxNombreApellido))
		self.vd_afiliado.af_cuil.setValidator(QtGui.QRegExpValidator(rxCuil))
		self.vd_afiliado.af_calle.setValidator(QtGui.QRegExpValidator(rxCalle))
		self.vd_afiliado.af_altura.setValidator(QtGui.QRegExpValidator(rxAltura))
		self.vd_afiliado.af_piso.setValidator(QtGui.QRegExpValidator(rxPiso))
		self.vd_afiliado.af_depto.setValidator(QtGui.QRegExpValidator(rxDepto))
		self.vd_afiliado.af_codigo_postal.setValidator(QtGui.QRegExpValidator(rxCodPostal))
		self.vd_afiliado.af_barrio.setValidator(QtGui.QRegExpValidator(rxBarrio))
		self.vd_afiliado.af_tel_laboral.setValidator(QtGui.QRegExpValidator(rxTelefono))
		self.vd_afiliado.af_tel_particular.setValidator(QtGui.QRegExpValidator(rxTelefono))
		self.vd_afiliado.af_celular.setValidator(QtGui.QRegExpValidator(rxTelefono))
		self.vd_afiliado.af_email.setValidator(QtGui.QRegExpValidator(rxEmail))
		self.vd_afiliado.af_lugar_trabajo.setValidator(QtGui.QRegExpValidator(rxLugarTrabajo))
		self.vd_afiliado.af_jerarquia.setValidator(QtGui.QRegExpValidator(rxJerarquia))

	def setRegexFamiliar(self):
		rxDni = QRegExp("\d{8,8}")
		rxNyA = QRegExp("[A-Z\s]{50}")

		self.vd_afiliado.fam_dni.setValidator(QtGui.QRegExpValidator(rxDni))
		self.vd_afiliado.fam_apellido.setValidator(QtGui.QRegExpValidator(rxNyA))
		self.vd_afiliado.fam_nombre.setValidator(QtGui.QRegExpValidator(rxNyA))
