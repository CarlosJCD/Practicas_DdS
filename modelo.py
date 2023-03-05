
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
from picklecryptor import PickleCryptor
from matplotlib.pyplot import subplots
from os import listdir, mkdir
from os.path import exists
from time import localtime
from shutil import move
from re import sub
from excepciones import ClienteNoExistente, CuentaNoExistente

class Lector:
    def __init__(self, 
                 base_path: str, 
                 password: str):
        self.__base_path = base_path
        self.__decrypter = PickleCryptor(password)

    def leer_cliente(self,numCliente: int) -> dict:
        cliente_path = f"{self.__base_path}{numCliente}"
        if not exists(cliente_path):
            raise ClienteNoExistente(f"Cliente #{numCliente} no existente.")

        with open(f"{cliente_path}/info.txt","rb") as fp: 
            return self.__decrypter.deserialize(fp.read())

    def leer_cuenta(self,num_cliente: int,num_cuenta: int) -> dict:
        cuenta_path = f"{self.__base_path}/{num_cliente}/{num_cuenta}.txt"
        if not exists(cuenta_path):
            raise CuentaNoExistente(f"Cuenta #{num_cuenta} no existente.")
        with open(cuenta_path,"rb") as fp:
            return self.__decrypter.deserialize(fp.read())

    def imprimir_registros(self):
        lista_clientes: list = [cliente for cliente in listdir(self.__base_path) if cliente!="log.txt"]
        for cliente in lista_clientes:
            info_cliente: dict = self.leer_cliente(int(cliente))
            print(f"\nNum. Cliente: {info_cliente.get('numCliente')} - Nombre: {info_cliente.get('nombre')}")
            lista_cuentas: list = [sub(".txt","",cuenta) for cuenta in listdir(f"{self.__base_path}{cliente}/") if cuenta != "cuentas_elimindadas" and cuenta != "info.txt" ]
            for cuenta in lista_cuentas:
                info_cuenta: dict = self.leer_cuenta(int(cliente),int(cuenta))
                print(f"    Num. Cuenta: {info_cuenta.get('numCuenta')} - Saldo: {info_cuenta.get('saldo')}")  
    
    def __generar_tablas(self) -> DataFrame:
        reporte_clientes = []
        reporte_cuentas = []
        lista_clientes: list = [cliente for cliente in listdir(self.__base_path) if cliente!="log.txt"]
        for num_cliente in lista_clientes:
            info_cliente = self.leer_cliente(int(num_cliente))
            reporte_clientes.append([info_cliente.get("numCliente"),info_cliente.get('nombre')])
            lista_cuentas: list = [sub(".txt","",cuenta) for cuenta in listdir(f"{self.__base_path}{num_cliente}/") if cuenta != "cuentas_elimindadas" and cuenta != "info.txt" ]
            for cuenta in lista_cuentas:
                info_cuenta = self.leer_cuenta(num_cliente,cuenta)
                reporte_cuentas.append([info_cliente.get('numCliente'),info_cuenta.get("numCuenta"),info_cuenta.get("saldo")])

        return DataFrame(reporte_clientes,columns=["num_cliente","nombre"]),DataFrame(reporte_cuentas,columns=["num_cliente","num_cuenta","saldo"])

    def generar_reporte(self):
        reporte_clientes,reporte_cuentas = self.__generar_tablas()

        fig, ax = subplots(sharex=True,sharey=True)

        ax1, ax2 = fig.subplots(2,1,sharex=True,sharey=True)

        ax.axis('tight')
        ax1.axis('tight')
        ax2.axis('tight')
        ax.axis("off")
        ax1.axis('off')
        ax2.axis('off')

        tabla_clientes = ax1.table(cellText =reporte_clientes.values, colLabels=reporte_clientes.columns,cellLoc = 'center')
        tabla_cuentas = ax2.table(cellText =reporte_cuentas.values, colLabels=reporte_cuentas.columns,cellLoc = 'center')

        reporte = PdfPages("reporte.pdf")
        reporte.savefig(fig,bbox_inches='tight')
        reporte.close()


class Escritor:
    def __init__(self, 
                 base_path: str, 
                 password: str):
        self.__base_path = base_path
        self.__encrypter = PickleCryptor(password)

    def registrar_cliente(self, info_cliente:dict):
        cliente_path = f"{self.__base_path}{info_cliente.get('numCliente')}/"
        mkdir(cliente_path)
        with open(f"{cliente_path}info.txt","wb") as fp:
            fp.write(self.__encrypter.serialize(info_cliente))

    def registrar_cuenta(self,info_cuenta: dict, num_cliente: int):
        cuenta_path = f"{self.__base_path}{num_cliente}/{info_cuenta.get('numCuenta')}.txt"
        with open(cuenta_path,"wb") as fp:
            fp.write(self.__encrypter.serialize(info_cuenta))

    def actualizar_cliente(self, num_cliente: int, nombre_nuevo: str, info_cliente: dict):
        cliente_path = f"{self.__base_path}{num_cliente}/info.txt"
        info_cliente.update({"nombre":nombre_nuevo})
        with open(cliente_path,"wb") as fp:
            fp.write(self.__encrypter.serialize(info_cliente))

    def actualizar_cuenta(self, num_cliente: int,num_cuenta: int, parametro_a_cambiar, datos_nuevos, info_cuenta: dict):
        cuenta_path = f"{self.__base_path}{num_cliente}/{num_cuenta}.txt"
        info_cuenta.update({parametro_a_cambiar:datos_nuevos})
        with open(cuenta_path,"wb") as fp:
            fp.write(self.__encrypter.serialize(info_cuenta))

    def eliminar_cuenta(self, num_cliente: int, num_cuenta: int):
        cuenta_path = f"{self.__base_path}{num_cliente}/{num_cuenta}.txt"
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
