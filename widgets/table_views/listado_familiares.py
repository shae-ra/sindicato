from PyQt5 import QtWidgets, QtGui

class ListadoFamiliaresContextM(QtWidgets.QTableView):

	def __init__(self, parent = None):
		super(ListadoFamiliaresContextM, self).__init__(parent)
		self.parent = parent

	def contextMenuEvent(self, event):
		self.menu = QtWidgets.QMenu(self)

		eliminarFamiliar = QtWidgets.QAction('Eliminar', self)

		eliminarFamiliar.triggered.connect(lambda: self.borrarFamiliar(event))

		self.menu.addAction(eliminarFamiliar)

		# add other required actions
		if self.selectedIndexes():
			self.menu.popup(QtGui.QCursor.pos())

	def borrarFamiliar(self, event):
		row = self.currentIndex().row()

		idFamiliarIndex = self.model().index(row, 0)
		idFamiliar = self.model().itemData(idFamiliarIndex)[0]

		if self.confirmarOperacion():
			self.model().borrarFamiliar(idFamiliar)
			self.model().refrescarTabla()

	def confirmarOperacion(self):
		msg = QtWidgets.QMessageBox()

		reply = msg.question(self, "Confirmar operación", "¿Está seguro de realizar esta operación?",
			QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

		msg.show()

		if reply == QtWidgets.QMessageBox.Yes:
			return True
		else:
			return False
