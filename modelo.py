from os import listdir, mkdir
from os.path import exists
from json import load,dump
from time import localtime
from shutil import move
from re import sub
from excepciones import ClienteNoExistente, CuentaNoExistente

class Lector:
    def __init__(self):
        self.__base_path = "Clientes/"
        if not exists(self.__base_path):
            mkdir(self.__base_path)

    def leer_cliente(self,numCliente: int) -> dict:
        cliente_path = f"{self.__base_path}{numCliente}"
        if not exists(cliente_path):
            raise ClienteNoExistente(f"Cliente #{numCliente} no existente.")

        with open(f"{cliente_path}/info.json","r") as fp: 
            return load(fp)

    def leer_cuenta(self,num_cliente: int,num_cuenta: int) -> dict:
        cuenta_path = f"{self.__base_path}/{num_cliente}/{num_cuenta}.json"
        if not exists(cuenta_path):
            raise CuentaNoExistente(f"Cuenta #{num_cuenta} no existente.")
        with open(cuenta_path) as fp:
            return load(fp)

    def imprimir_registros(self):
        lista_clientes: list = listdir(self.__base_path).remove("log.txt")
        for cliente in lista_clientes:
            info_cliente: dict = self.leer_cliente(int(cliente))
            print(f"Num. Cliente: {info_cliente.get('numCliente')} - Nombre: {info_cliente.get('nombre')}")
            lista_cuentas: list = [sub(".json","",cuenta) for cuenta in listdir(f"{self.__base_path}{cliente}/") if cuenta != "cuentas_elimindadas" and cuenta != "info.json" ]
            for cuenta in lista_cuentas:
                info_cuenta: dict = self.leer_cuenta(int(cliente),int(cuenta))
                print(f"    Num. Cuenta: {info_cuenta.get('numCuenta')} - Saldo: {info_cuenta.get('saldo')}")  


class Escritor:
    def __init__(self):
        self.__base_path = "Clientes/"
        if not exists(self.__base_path):
            mkdir(self.__base_path)

    def registrar_cliente(self, info_cliente:dict):
        cliente_path = f"{self.__base_path}{info_cliente.get('numCliente')}/"
        mkdir(cliente_path)
        with open(f"{cliente_path}info.json","w") as fp:
            dump(info_cliente, fp = fp)

    def registrar_cuenta(self,info_cuenta: dict, num_cliente: int):
        cuenta_path = f"{self.__base_path}{num_cliente}/{info_cuenta.get('numCuenta')}.json"
        with open(cuenta_path,"w", encoding="utf-8") as fp:
            dump(info_cuenta, fp = fp)

    def actualizar_cliente(self, num_cliente: int, nombre_nuevo: str, info_cliente: dict):
        cliente_path = f"{self.__base_path}{num_cliente}/info.json"
        info_cliente.update({"nombre":nombre_nuevo})
        with open(cliente_path,"w") as fp:
            dump(info_cliente, fp = fp)

    def actualizar_cuenta(self, num_cliente: int,num_cuenta: int, parametro_a_cambiar, datos_nuevos, info_cuenta: dict):
        cuenta_path = f"{self.__base_path}{num_cliente}/{num_cuenta}.json"
        info_cuenta.update({parametro_a_cambiar:datos_nuevos})
        with open(cuenta_path,"w") as fp:
            dump(info_cuenta, fp = fp)

    def eliminar_cuenta(self, num_cliente: int, num_cuenta: int):
        cuenta_path = f"{self.__base_path}{num_cliente}/{num_cuenta}.json"
        eliminados_path = f"{self.__base_path}{num_cliente}/cuentas_eliminadas"
        if not exists(eliminados_path):
            mkdir(eliminados_path)
        move(cuenta_path,eliminados_path)


class Logger:
    def __init__(self):
        self.__base_path = "Clientes/log.txt"
        if not exists(self.__base_path):
            with open(self.__base_path,"w") as fp:
                fp.write(f"Creacion Archivo log.txt - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cliente_nuevo(self,numCliente: int):
        with open(self.__base_path,"a") as fp:
            fp.write(f"\nCliente #{numCliente} creado - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_nueva(self,numCuenta: int):
        with open(self.__base_path,"a") as fp:
            fp.write(f"\nCuenta #{numCuenta} creada - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_borrada(self,numCuenta: int):
        with open(self.__base_path,"a") as fp:
            fp.write(f"\nCuenta #{numCuenta} Borrada - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cuenta_actualizado(self,num_cuenta: int, parametro_actualizado: str, datos_nuevos):
        with open(self.__base_path,"a") as fp:
            fp.write(f"\n{parametro_actualizado} de la cuenta #{num_cuenta} actualizado a {datos_nuevos} - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")

    def log_cliente_actualizado(self,num_cliente: int, parametro_actualizado: str, datos_nuevos):
        with open(self.__base_path,"a") as fp:
            fp.write(f"\n{parametro_actualizado} del cliente #{num_cliente} actualizado a {datos_nuevos} - Fecha: {localtime()[2]}/{localtime()[1]}/{localtime()[0]} - Hora: {localtime()[3]}:{localtime()[4]}:{localtime()[5]}")
