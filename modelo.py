from os import listdir, mkdir
from os.path import exists
from json import load,dump
from time import localtime
from shutil import move
from re import sub
from excepciones import ClienteNoExistente, CuentaNoExistente

class Lector:
    def __init__(self):
        self.base_path = "Clientes/"
        if not exists(self.base_path):
            mkdir(self.base_path)

    def leer_cliente(self,numCliente: int) -> dict:
        cliente_path = f"{self.base_path}{numCliente}"
        if not exists(cliente_path):
            raise ClienteNoExistente(f"Cliente #{numCliente} no existente.")

        with open(f"{cliente_path}/info.json","r") as fp: 
            return load(fp)

    def leer_cuenta(self,num_cliente: int,num_cuenta: int) -> dict:
        cuenta_path = f"{self.base_path}/{num_cliente}/{num_cuenta}.json"
        if not exists(cuenta_path):
            raise CuentaNoExistente(f"Cuenta #{num_cuenta} no existente.")
        with open(cuenta_path) as fp:
            return load(fp)

    def imprimir_registros(self):
        lista_clientes: list = listdir(self.base_path).remove("log.txt")
        for cliente in lista_clientes:
            info_cliente: dict = self.leer_cliente(int(cliente))
            print(f"Num. Cliente: {info_cliente.get('numCliente')} - Nombre: {info_cliente.get('nombre')}")
            lista_cuentas: list = [sub(".json","",cuenta) for cuenta in listdir(f"{self.base_path}{cliente}/") if cuenta != "cuentas_elimindadas" and cuenta != "info.json" ]
            for cuenta in lista_cuentas:
                info_cuenta: dict = self.leer_cuenta(int(cliente),int(cuenta))
                print(f"    Num. Cuenta: {info_cuenta.get('numCuenta')} - Saldo: {info_cuenta.get('saldo')}")  


class Escritor:
    def __init__(self):
        self.base_path = "Clientes/"
        self.lector = Lector()
        if not exists(self.base_path):
            mkdir(self.base_path)
        self.logger = Logger()

    def registrar_cliente(self, info_cliente:dict):
        cliente_path = f"{self.base_path}{info_cliente.get('numCliente')}/"
        mkdir(cliente_path)
        with open(f"{cliente_path}info.json","w") as fp:
            dump(info_cliente, fp = fp)
        self.logger.log_cliente_nuevo(info_cliente.get("numCliente"))

    def registrar_cuenta(self,info_cuenta: dict, num_cliente: int):
        cuenta_path = f"{self.base_path}{num_cliente}/{info_cuenta.get('numCuenta')}.json"
        with open(cuenta_path,"w", encoding="utf-8") as fp:
            dump(info_cuenta, fp = fp)
        self.logger.log_cuenta_nueva(info_cuenta.get("numCuenta"))

    def actualizar_cliente(self, num_cliente: int, nombre_nuevo):
        cliente_path = f"{self.base_path}{num_cliente}/info.json"
        cliente: dict = self.lector.leer_cliente(num_cliente)
        cliente.update({"nombre":nombre_nuevo})
        with open(cliente_path,"w") as fp:
            dump(cliente, fp = fp)
        self.logger.log_cliente_actualizado(num_cliente,"Nombre",nombre_nuevo)

    def actualizar_cuenta(self, num_cliente: int,num_cuenta: int, parametro_a_cambiar, datos_nuevos):
        cuenta_path = f"{self.base_path}{num_cliente}/{num_cuenta}.json"
        with open(cuenta_path,"w") as fp:
            cuenta: dict = self.lector.leer_cuenta(num_cliente,num_cuenta)
            cuenta.update({parametro_a_cambiar:datos_nuevos})
            dump(cuenta, fp = fp)
        self.logger.log_cuenta_actualizado(num_cuenta,parametro_a_cambiar,datos_nuevos)

    def eliminar_cuenta(self, num_cliente: int, num_cuenta: int):
        cuenta_path = f"{self.base_path}{num_cliente}/{num_cuenta}.json"
        eliminados_path = f"{self.base_path}{num_cliente}/cuentas_eliminadas"
        
        if not exists(eliminados_path):
            mkdir(eliminados_path)
        move(cuenta_path,eliminados_path)
        self.logger.log_cuenta_borrada(num_cuenta)


class Logger:
    def __init__(self):
        self.archivo = "Clientes/log.txt"
        if not exists(self.archivo):
            with open(self.archivo,"w") as fp:
                fp.write(f"Creacion Archivo log.txt - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cliente_nuevo(self,numCliente: int):
        with open(self.archivo,"a") as fp:
            fp.write(f"\nCliente #{numCliente} creado - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_nueva(self,numCuenta: int):
        with open(self.archivo,"a") as fp:
            fp.write(f"\nCuenta #{numCuenta} creada - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_borrada(self,numCuenta: int):
        with open(self.archivo,"a") as fp:
            fp.write(f"\nCuenta #{numCuenta} Borrada - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_actualizado(self,num_cuenta: int, parametro_actualizado: str, datos_nuevos):
        with open(self.archivo,"a") as fp:
            fp.write(f"\n{parametro_actualizado} de la cuenta #{num_cuenta} actualizado a {datos_nuevos} - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cliente_actualizado(self,num_cliente: int, parametro_actualizado: str, datos_nuevos):
        with open(self.archivo,"a") as fp:
            fp.write(f"\n{parametro_actualizado} del cliente #{num_cliente} actualizado a {datos_nuevos} - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")
