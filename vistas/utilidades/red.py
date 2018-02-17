from PyQt5 import QtWidgets, uic
from libs.db.querier import Querier

class VistaRed(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(VistaRed, self).__init__(parent)

        self.vista = uic.loadUi("gui/utilidades/red.ui")
        self.q = Querier()

        self.vista.btn_guardar.clicked.connect(self.guardarConfig)
        self.vista.btn_probar.clicked.connect(self.probarConfig)

        self.loadConfig()

    def loadConfig(self):
        config = self.q.getConfig()

        self.vista.config_user.setText(config['user'])
        self.vista.config_host.setText(config['host'])
        self.vista.config_pass.setText(config['pass'])
        self.vista.config_database.setText(config['database'])

    def guardarConfig(self):
        self.setConfig()
        self.q.guardarConfiguracion()

    def probarConfig(self):
        self.setConfig()
        if self.q.probarConexion():
            print("Anda")
        else:
            print("No anda")

    def setConfig(self):
        self.q.setConexion(
            user = self.vista.config_user.text(),
            host = self.vista.config_host.text(),
            database = self.vista.config_database.text(),
            password = self.vista.config_pass.text()
        )
