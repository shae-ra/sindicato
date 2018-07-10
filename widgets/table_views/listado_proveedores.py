from PyQt5 import QtWidgets, QtGui

class ListadoProveedoresContextM(QtWidgets.QTableView):

	def __init__(self, parent = None):
		super(ListadoProveedoresContextM, self).__init__(parent)
		self.parent = parent

	def contextMenuEvent(self, event):
		self.menu = QtWidgets.QMenu(self)

		deshabilitarProveedor = QtWidgets.QAction('Dar de baja', self)

		deshabilitarProveedor.triggered.connect(lambda: self.deshabilitarProveedor(event))

		self.menu.addAction(deshabilitarProveedor)

		# add other required actions
		if self.selectedIndexes():
			self.menu.popup(QtGui.QCursor.pos())

	def deshabilitarProveedor(self, event):
		row = self.currentIndex().row()

		idProveedorIndex = self.model().index(row, 0)
		idProveedor = self.model().itemData(idProveedorIndex)[0]

		if self.confirmarOperacion():
			self.model().bajaProveedor(idProveedor)
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
