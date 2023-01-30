class CuentaExistenteExcepcion(Exception):
    def __init__(self,mensaje: str ) -> None:
        self.mensaje = mensaje

    def __str__(self) -> str:
        return repr(self.mensaje)

class NumClienteExistenteExcepcion(Exception):
    def __init__(self,mensaje: str ) -> None:
        self.mensaje = mensaje

    def __str__(self) -> str:
        return repr(self.mensaje)