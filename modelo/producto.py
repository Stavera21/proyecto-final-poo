
class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float, cantidad: int, fecha_ingreso: str):
        self.codigo: str = codigo
        self.nombre: str = nombre
        self.precio: float = precio
        self.cantidad: int = cantidad
        self.fecha_ingreso: str = fecha_ingreso

    def __str__(self):
        return "({}) {} - ${:,.2f}".format(self.codigo, self.nombre, self.precio, self.cantidad, self.fecha_ingreso)