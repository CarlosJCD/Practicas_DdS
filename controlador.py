from re import compile, sub
from excepciones import ClienteExistente, CuentaExistente, CredencialesInvalidas, CuentaConSaldo
from modelo import Escritor, Lector
from os import listdir, mkdir
from os.path import exists

class Controlador:
    def __init__(self):
        self.base_path = "Clientes/"
        self.escritor: Escritor = Escritor()
        self.lector: Lector = Lector()

    def __validar_credenciales(self, num_cliente: int, num_cuenta: int, nombre: str, saldo: float):
        patron_num = compile("^\d{16}$")
        patron_saldo = compile("^\d*.\d*$")
        patron_nombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")
        
        if not patron_num.search(str(num_cuenta)):
            raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
        if not patron_num.search(str(num_cliente)):
            raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)
        if not patron_saldo.search(str(saldo)):
            raise CredencialesInvalidas(credencial = "Saldo", valor= saldo)
        if not patron_nombre.search(nombre):
            raise CredencialesInvalidas(credencial = "Nombre", valor= nombre)
            
    def crear_cliente(self,num_cliente: int, nombre: str, num_cuenta: int = None, saldo: float = 0.0):
        self.__validar_credenciales(num_cliente = num_cliente, num_cuenta= num_cuenta, nombre= nombre, saldo= saldo)

        if str(num_cliente) in listdir(self.base_path):
            raise ClienteExistente(f"Cliente #{num_cliente} ya registrado")
         
        self.escritor.registrar_cliente({"numCliente": num_cliente,"nombre": nombre,})
        self.crear_cuenta(num_cliente, num_cuenta, saldo)       

    def crear_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float = 0.0):
        for cliente in [cliente for cliente in listdir(self.base_path) if cliente != "log.txt"]:
            lista_cuentas = [sub(".json","",cuenta) for cuenta in listdir(f"{self.base_path}{cliente}/")]
            if num_cuenta in lista_cuentas:
                raise CuentaExistente(f"Cuenta #{num_cuenta} ya registrada")
        self.escritor.registrar_cuenta({"numCuenta":num_cuenta,"saldo":saldo},num_cliente)

    def actualizar_cliente(self, num_cliente: int, nombre: str):
        patron_num = compile("^\d{16}$")
        patron_nombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")

        if patron_num.search(str(num_cliente)) and patron_nombre.search(nombre):
            self.escritor.actualizar_cliente(num_cliente,nombre)
        else:
            if not patron_num.search(str(num_cliente)):
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor = num_cliente)
            raise CredencialesInvalidas(credencial = "Nombre", valor = nombre)

    def actualizar_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float):
        patron_num = compile("^\d{16}$")
        patron_saldo = compile("^\d*.\d*$")

        if patron_num.search(num_cliente) and patron_num.search(num_cuenta) and patron_saldo.search(saldo):
            self.escritor.actualizar_cuenta(num_cliente,num_cuenta,"saldo",saldo)
        else:
            if not patron_num.search(num_cuenta):
                raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
            if not patron_num.search(num_cliente):
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)
            if not patron_saldo.search(saldo):
                raise CredencialesInvalidas(credencial = "Saldo", valor= saldo)

    def eliminar_cuenta(self,num_cliente: int, num_cuenta: int):
        patron_num = compile("^\d{16}$")

        if patron_num.search(str(num_cliente)) and patron_num.search(str(num_cuenta)):
            saldo: float = self.lector.leer_cuenta(num_cliente,num_cuenta).get("saldo")
            if saldo == 0.0:
                self.escritor.eliminar_cuenta(num_cliente,num_cuenta)
            else:
                raise CuentaConSaldo(f"Imposible eliminar la cuenta #{num_cuenta} con saldo {saldo}")
        else:
            if not patron_num.search(num_cuenta):
                raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
            else:
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)