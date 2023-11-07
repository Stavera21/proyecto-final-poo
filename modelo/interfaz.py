import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QWidget
from PyQt5 import QtCore, uic
from acciones_inventario import Inventario
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QRegExpValidator, QDoubleValidator
from producto_existente_error import ProductoExistenteError
from producto_no_encontrado_error import ProductoNoEncontradoError
from PyQt5.QtCore import QRegExp

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi("gui/mainwindow.ui", self)
        self.setFixedSize(self.size())
        self.dialogo_agregar_producto = DialogoAgregarProducto()
        self.dialogo_eliminar_producto = DialogoEliminarProducto()
        self.inventario = Inventario()
        self.configurar()
        self.cargar_datos()

    def configurar(self):
        # configurar el QListview
        self.listView_inventario.setModel(QStandardItemModel())

        # enlazar los eventos de los botones
        self.pushButton_agregar.clicked.connect(self.abrir_dialogo_agregar_producto)
        self.pushButton_eliminar.clicked.connect(self.abrir_dialogo_eliminar_producto)

        

    def cargar_datos(self):
        productos = list(self.inventario.productos.values())
        for producto in productos:
            item = QStandardItem(str(producto))
            item.producto = producto
            item.setEditable(False)
            self.listView_inventario.model().appendRow(item)


    
    def abrir_dialogo_eliminar_producto(self):
        resp = self.dialogo_eliminar_producto.exec()
        if resp == QDialog.Accepted:
            codigo = self.dialogo_eliminar_producto.lineEdit_codigo_eliminar.text()
        try:
            producto_eliminado = self.inventario.eliminar_producto(codigo)
        except ProductoNoEncontradoError as err:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText(err.mensaje)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()
        else:
            model = self.listView_inventario.model()
            for row in range(model.rowCount()):
                item = model.item(row)
                if item.producto.codigo == producto_eliminado.codigo:
                    model.removeRow(row)
                    break
        self.dialogo_eliminar_producto.limpiar()


    def abrir_dialogo_agregar_producto(self):
        resp = self.dialogo_agregar_producto.exec()
        if resp == QDialog.Accepted:
            codigo = self.dialogo_agregar_producto.lineEdit_codigo.text()
            nombre = self.dialogo_agregar_producto.lineEdit_nombre.text()
            precio = float(self.dialogo_agregar_producto.lineEdit_precio.text())
            cantidad = int(self.dialogo_agregar_producto.lineEdit_cantidad.text())
            fecha = self.dialogo_agregar_producto.lineEdit_fecha.text()
            try:
                producto = self.inventario.agregar_producto(codigo, nombre, precio, cantidad, fecha)
            except ProductoExistenteError as err:
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Error")
                msg_box.setIcon(QMessageBox.Warning)
                msg_box.setText(err.mensaje)
                msg_box.setStandardButtons(QMessageBox.Ok)
                msg_box.exec()
            else:
                model = self.listView_inventario.model()
                item = QStandardItem(str(producto))
                item.producto = producto
                item.setEditable(False)
                model.appendRow(item)
        
        self.dialogo_agregar_producto.limpiar()


class DialogoAgregarProducto(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/dialogoAgregarProducto.ui", self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.lineEdit_codigo.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.lineEdit_codigo))
        self.lineEdit_precio.setValidator(QDoubleValidator(0, 999999, 2, self.lineEdit_precio))

    def limpiar(self):
        self.lineEdit_codigo.clear()
        self.lineEdit_nombre.clear()
        self.lineEdit_precio.clear()
        self.lineEdit_cantidad.clear()
        self.lineEdit_fecha.clear()


    def accept(self) -> None:
        if self.lineEdit_codigo.text() != "" and self.lineEdit_nombre.text() != "" and self.lineEdit_precio.text() != "" and self.lineEdit_cantidad.text() != "" and self.lineEdit_fecha.text() != "":
            super(DialogoAgregarProducto, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()


class DialogoEliminarProducto(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("gui/dialogoEliminarProducto.ui", self)
        self.setFixedSize(self.size())
        self.configurar()

    def configurar(self):
        self.lineEdit_codigo_eliminar.setValidator(QRegExpValidator(QRegExp("\\d{6}"), self.lineEdit_codigo_eliminar))

    def limpiar(self):
        self.lineEdit_codigo_eliminar.clear()

    def accept(self) -> None:
        if self.lineEdit_codigo_eliminar.text() != "":
            super(DialogoEliminarProducto, self).accept()
        else:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Error")
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Debe ingresar todos los datos del formulario")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

 

