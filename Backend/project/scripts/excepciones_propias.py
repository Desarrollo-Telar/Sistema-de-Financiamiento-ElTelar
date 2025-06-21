class MiExcepcionPersonalizada(Exception):
    """
    Excepción personalizada para manejar errores específicos.
    """
    def __init__(self, mensaje, valor):
        self.mensaje = mensaje
        self.valor = valor
        super().__init__(self.mensaje)  # Llama al constructor de la clase base

    def __str__(self):
        return f'{self.mensaje}: {self.valor}'