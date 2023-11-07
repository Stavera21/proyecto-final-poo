from producto_error import ProductoError

class ProductoExistenteError(ProductoError):
    def __init__(self, mensaje, codigo):
        super().__init__(mensaje)
        self.codigo = codigo

   
    
