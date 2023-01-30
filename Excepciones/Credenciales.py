class CredencialesInvalidasExcepcion(Exception):
    def __init__(self, credencial: str, valor) -> None:
        super()
        self.credencial = credencial
        self.valor = valor
    
    def __str__(self) -> str:
        return f"ERROR: Credencial '{self.credencial}' invalida: {self.valor}"
