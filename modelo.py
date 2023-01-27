from re import sub

class LectorCSV:
    def __init__(self, archivo: str) -> None:
        self.nombre_archivo = archivo
    
    def leer_archivo(self) -> list:
        with open(self.nombre_archivo) as fp:
            return fp.readlines()
    
    def imprimir_registros(self):
        print("Num Cliente | Nombre | Num Cuenta | Saldo \n")
        registros = self.leer_archivo()
        for registro in registros:
            print(sub(","," | ",registro))


class EscritorCSV:
    def __init__(self,archivo: str) -> None:
        self.nombre_archivo = archivo

    def add(self, registro: dict):

        with open(self.nombre_archivo,"a") as fp:
            fp.write(f"\n{registro.get('numCliente')},{registro.get('nombre')},{registro.get('numCuenta')},{registro.get('saldo')}")