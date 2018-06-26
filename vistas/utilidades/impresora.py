from PyQt5 import QtWidgets, uic, QtCore
from configparser import ConfigParser
import win32print

class VistaImpresora(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(VistaImpresora, self).__init__(parent)

        self.vista = uic.loadUi("gui/utilidades/impresora.ui")

        self.vista.btn_guardar.clicked.connect(self.guardarConfig)

        self.model = ModeloImpresora(self)
        self.vista.config_impresora.setModel(self.model)

        self.model.listarImpresoras()

        self.loadConfig()

    def loadConfig(self):
        config = ConfigParser()

        impresora = ""
        bonoArchivoImagen = ""
        bonoArchivoExcel = ""
        if config.read('impresora.ini'):
            if 'IMPRESORA' in config.sections():
                impresora = config['IMPRESORA']['nombre_impresora']
            if 'BONO' in config.sections():
                bonoArchivoImagen = config['BONO']['imagen']
                bonoArchivoExcel = config['BONO']['excel']

        self.vista.config_impresora.setCurrentText(impresora)
        self.vista.config_bono_excel.setText(bonoArchivoImagen)
        self.vista.config_bono_imagen.setText(bonoArchivoExcel)

    def guardarConfig(self):
        config = ConfigParser()

        config.read_dict({'IMPRESORA' : {}, 'BONO' : {}})

        config['IMPRESORA']['nombre_impresora'] = self.vista.config_impresora.currentText()
        config['BONO']['imagen'] = self.vista.config_bono_imagen.text()
        config['BONO']['excel'] = self.vista.config_bono_excel.text()

        with open('impresora.ini', 'w') as configFile:
            config.write(configFile)

    def probarConfig(self):
        pass
        # self.setConfig()
        # if self.q.probarConexion():
        #     print("Anda")
        # else:
        #     print("No anda")

# =============================================
# Pequeño modelo en PyQt5 para la impresora
# =============================================

class ModeloImpresora(QtCore.QAbstractListModel):

    def __init__(self, parent = None):
        super(ModeloImpresora, self).__init__()

        self.impresoras = []

    def listarImpresoras(self):
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_NAME)

        for printer in printers:
            self.impresoras.append(printer[2])

        self.layoutChanged.emit()

    def rowCount(self, parent):
        if self.impresoras:
            return len(self.impresoras)
        else:
            return 0

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.impresoras[row]
            return value
