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

    def __validar_credenciales(self,registro: dict):
        patronNum = compile("^\d{16}$")
        patronSaldo = compile("^\d*.\d*$")
        patronNombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")

        condicionNumCuenta = patronNum.search(str(registro.get("numCuenta")))
        condicionNumCliente = patronNum.search(str(registro.get("numCliente")))
        condicionSaldo = patronSaldo.search(str(registro.get("saldo")))
        condicionNombre = patronNombre.search(str(registro.get("nombre")))
        
        if not condicionNumCuenta:
            raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = registro.get("numCuenta"))
        elif not condicionNumCliente:
            raise CredencialesInvalidas(credencial = "Num. Cliente", valor= registro.get("numCliente"))
        elif not condicionSaldo:
            raise CredencialesInvalidas(credencial = "Saldo", valor= registro.get("saldo"))
        elif not condicionNombre:
            raise CredencialesInvalidas(credencial = "Nombre", valor= registro.get("nombre"))
            
    def crear_cliente(self,num_cliente: int, nombre: str, num_cuenta: int = None, saldo: float = 0.0):
        registroNuevo = {
            "numCliente": num_cliente,
            "nombre": nombre,
            "numCuenta": num_cuenta,
            "saldo": saldo
        }
        self.__validar_credenciales(registroNuevo)

        lista_clientes: list = listdir(self.base_path)

        if str(num_cliente) in lista_clientes:
            raise ClienteExistente(f"Cliente #{num_cliente} ya registrado")
        else:
            if not exists(f"{self.base_path}{num_cliente}/"):
                self.escritor.registrar_cliente({"numCliente": num_cliente,"nombre": nombre,})
                self.escritor.registrar_cuenta({"numCuenta": num_cuenta,"saldo": saldo}, num_cliente)
            else:
                lista_cuentas: list = [sub(".json","",cuenta) for cuenta in listdir(f"{self.base_path}{num_cliente}/")]
                if num_cuenta in lista_cuentas:
                    raise CuentaExistente(f"Cuenta #{num_cuenta} ya registrada")
                self.escritor.registrar_cuenta({"numCuenta": num_cuenta,"saldo": saldo},num_cliente)        

    def crear_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float = 0.0):
        client_path = f"{self.base_path}{num_cliente}/"
        if exists(client_path):
            lista_cuentas = [sub(".json","",cuenta) for cuenta in listdir(client_path)]
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
            else:
                raise CredencialesInvalidas(credencial = "Nombre", valor = nombre)

    def actualizar_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float):
        patron_num = compile("^\d{16}$")
        patron_saldo = compile("^\d*.\d*$")

        if patron_num.search(num_cliente) and patron_num.search(num_cuenta) and patron_saldo.search(saldo):
            self.escritor.actualizar_cuenta(num_cliente,num_cuenta,"saldo",saldo)
        else:
            if not patron_num.search(num_cuenta):
                raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
            elif not patron_num.search(num_cliente):
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)
            elif not patron_saldo.search(saldo):
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