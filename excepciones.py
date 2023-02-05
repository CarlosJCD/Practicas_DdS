
class CredencialesInvalidas(Exception):
    def __init__(self, credencial: str, valor) -> None:
        super()
        self.credencial = credencial
        self.valor = valor
    
    def __str__(self) -> str:
        return f"ERROR: Credencial '{self.credencial}' invalida: {self.valor}"

class CuentaExistente(Exception):
    def __init__(self,mensaje: str ) -> None:
        self.mensaje = mensaje

    def __str__(self) -> str:
        return repr(self.mensaje)

class ClienteExistente(Exception):
    def __init__(self,mensaje: str ) -> None:
        self.mensaje = mensaje

    def __str__(self) -> str:
        return self.mensaje

class ClienteNoExistente(Exception):
    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
    
    def __str__(self) -> str:
        return self.mensaje

class CuentaNoExistente(Exception):
    def __init__(self,message: str) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return self.message

class CuentaConSaldo(Exception):
    def __init__(self,message: str) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return self.message