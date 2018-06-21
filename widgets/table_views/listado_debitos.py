from PyQt5 import QtWidgets, QtGui

class ListadoDebitosContextM(QtWidgets.QTableView):

	def __init__(self, parent = None):
		super(ListadoDebitosContextM, self).__init__(parent)
		self.parent = parent

	def contextMenuEvent(self, event):
		self.menu = QtWidgets.QMenu(self)

		eliminarDebito = QtWidgets.QAction('Eliminar', self)
		pagoManualDebito = QtWidgets.QAction('Pago manual', self)

		eliminarDebito.triggered.connect(lambda: self.borrarDebito(event))
		pagoManualDebito.triggered.connect(lambda: self.pagoManual(event))

		self.menu.addAction(eliminarDebito)
		self.menu.addAction(pagoManualDebito)

		# add other required actions
		if self.selectedIndexes():
			self.menu.popup(QtGui.QCursor.pos())


	def borrarDebito(self, event):
		pass
		# print ("bajaAfiliado slot called")
		# indexes = self.selectedIndexes()
		# # get the selected row and column
		#
		# legajo = self.model().itemData(indexes[0])[0]
		#
		# afiliado = {
		# 	"legajo" : legajo,
		# 	"activo" : 0
		# }

		# self.model().bajaAfiliado(afiliado)

	def pagoManual(self, event):
		pass
		# print ("bajaAfiliado slot called")
		# indexes = self.selectedIndexes()
		# # get the selected row and column
		#
		# legajo = self.model().itemData(indexes[0])[0]
		#
		# afiliado = {
		# 	"legajo" : legajo,
		# 	"activo" : 0
		# }
		#
		# self.model().bajaAfiliado(afiliado)
