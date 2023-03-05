from re import compile, sub
from excepciones import ClienteExistente, CuentaExistente, CredencialesInvalidas, CuentaConSaldo
from modelo import Escritor, Lector, Logger
from os import mkdir,listdir
from os.path import exists

class Controlador:
    def __init__(self, 
                 base_path: str = "Clientes/", 
                 password = "contraseña"):
        self.__base_path = base_path
        if not exists(base_path):
            mkdir(base_path)
        self.__escritor: Escritor = Escritor(base_path=base_path, password=password)
        self.__lector: Lector = Lector(base_path=base_path, password=password)
        self.__logger: Logger = Logger()

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
            
    def crear_cliente(self,num_cliente: int, nombre: str, num_cuenta: int, saldo: float = 0.0):
        self.__validar_credenciales(num_cliente = num_cliente, num_cuenta= num_cuenta, nombre= nombre, saldo= saldo)

        if str(num_cliente) in listdir(self.__base_path):
            raise ClienteExistente(f"Cliente #{num_cliente} ya registrado")
         
        self.__escritor.registrar_cliente({"numCliente": num_cliente,"nombre": nombre})
        self.__logger.log_cliente_nuevo(num_cliente)
        self.crear_cuenta(num_cliente, num_cuenta, saldo)

    def crear_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float = 0.0):
        for cliente in [cliente for cliente in listdir(self.__base_path) if cliente != "log.txt"]:
            lista_cuentas = [sub(".json","",cuenta) for cuenta in listdir(f"{self.__base_path}{cliente}/")]
            if num_cuenta in lista_cuentas:
                raise CuentaExistente(f"Cuenta #{num_cuenta} ya registrada")
        self.__escritor.registrar_cuenta({"numCuenta":num_cuenta,"saldo":saldo},num_cliente)
        self.__logger.log_cuenta_nueva(num_cuenta)

    def actualizar_cliente(self, num_cliente: int, nombre: str):
        patron_num = compile("^\d{16}$")
        patron_nombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")

        if patron_num.search(str(num_cliente)) and patron_nombre.search(nombre):
            self.__escritor.actualizar_cliente(num_cliente,nombre, self.__lector.leer_cliente(num_cliente))
            self.__logger.log_cliente_actualizado(num_cliente,"Nombre",nombre)
        else:
            if not patron_num.search(str(num_cliente)):
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor = num_cliente)
            raise CredencialesInvalidas(credencial = "Nombre", valor = nombre)

    def actualizar_cuenta(self, num_cliente: int, num_cuenta: int, saldo: float):
        patron_num = compile("^\d{16}$")
        patron_saldo = compile("^\d*.\d*$")

        if patron_num.search(str(num_cliente)) and patron_num.search(str(num_cuenta)) and patron_saldo.search(str(saldo)):
            self.__escritor.actualizar_cuenta(num_cliente,num_cuenta,"saldo",saldo,self.__lector.leer_cuenta(num_cliente,num_cuenta))
            self.__logger.log_cuenta_actualizado(num_cuenta,"Saldo",saldo)
        else:
            if not patron_num.search(str(num_cuenta)):
                raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
            if not patron_num.search(str(num_cliente)):
                raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)
            if not patron_saldo.search(str(saldo)):
                raise CredencialesInvalidas(credencial = "Saldo", valor= saldo)

    def eliminar_cuenta(self,num_cliente: int, num_cuenta: int):
        patron_num = compile("^\d{16}$")

        if patron_num.search(str(num_cliente)) and patron_num.search(str(num_cuenta)):
            saldo: float = self.__lector.leer_cuenta(num_cliente,num_cuenta).get("saldo")
            if saldo == 0.0:
                self.__escritor.eliminar_cuenta(num_cliente,num_cuenta)
                self.__logger.log_cuenta_borrada(num_cuenta)
            else:
                raise CuentaConSaldo(f"Imposible eliminar la cuenta #{num_cuenta} con saldo {saldo}")
        else:
            if not patron_num.search(num_cuenta):
                raise CredencialesInvalidas(credencial= "Num. Cuenta", valor = num_cuenta)
            raise CredencialesInvalidas(credencial = "Num. Cliente", valor= num_cliente)