from PyQt5 import QtWidgets, uic


class VistaRed(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(VistaRed, self).__init__(parent)

        self.vista = uic.loadUi("gui/utilidades/red.ui")
