from producto import Producto
import pickle
import csv
from producto_existente_error import ProductoExistenteError
from producto_no_encontrado_error import ProductoNoEncontradoError

class Inventario:
    def __init__(self):
        self.productos: dict = {}
        self.cargar_inventario()


    def cargar_inventario(self):
        with open("data/inventario.csv") as file:
            csv_data = csv.reader(file, delimiter=";")
            productos = map(lambda data: Producto(data[0], data[1], float(data[2]), data[3], data[4]), csv_data)
            self.productos = {prod.codigo: prod for prod in productos}


    
    def agregar_producto(self, codigo, nombre, precio, cantidad, fecha_ingreso):
        if codigo not in self.productos.keys():
            producto = Producto(codigo, nombre, precio, cantidad, fecha_ingreso)
            self.productos[codigo] = producto
            return producto
        else:
            raise ProductoExistenteError(f"El producto con el código {codigo} ya existe.", codigo)

    
    def eliminar_producto(self, codigo):
        if codigo in self.productos:
            producto_eliminado = self.productos.pop(codigo)
            return producto_eliminado
        else:
            raise ProductoNoEncontradoError(f"No se encontró un producto con el código {codigo}.", codigo)


    
                   



