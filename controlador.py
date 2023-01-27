from re import compile
from modelo import LectorCSV, EscritorCSV
from Excepciones.RegistroExistenteExcepcion import CuentaExistenteExcepcion, NumClienteExistenteExcepcion
from Excepciones.CredencialesInvalidasExcepcion import CredencialesInvalidasExcepcion

class Controlador:
    def __init__(self, nombreArchivo: str) -> None:
        self.nombreArchivo = nombreArchivo

    def __validarCredenciales(self,registro: dict):
        patronNum = compile("^\d{16}$")
        patronSaldo = compile("^\d*.\d*$")
        patronNombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")

        condicionNumCuenta = patronNum.search(str(registro.get("numCuenta"))) or not registro.get("numCuenta")
        condicionNumCliente = patronNum.search(str(registro.get("numCliente")))
        condicionSaldo = patronSaldo.search(str(registro.get("saldo")))
        condicionNombre = patronNombre.search(str(registro.get("nombre")))
        try:
            if not condicionNumCuenta:
                raise CredencialesInvalidasExcepcion(credencial= "Num. Cuenta", valor = registro.get("numCuenta"))
            elif not condicionNumCliente:
                raise CredencialesInvalidasExcepcion(credencial = "Num. Cliente", valor= registro.get("numCliente"))
            elif not condicionSaldo:
                raise CredencialesInvalidasExcepcion(credencial = "Saldo", valor= registro.get("saldo"))
            elif not condicionNombre:
                raise CredencialesInvalidasExcepcion(credencial = "Nombre", valor= registro.get("nombre"))
        except CredencialesInvalidasExcepcion as e:
            print(e)
            
    def crearRegistro(self,numCliente: int, nombre: str, numCuenta: int = None, saldo: float = 0.0):
        registroNuevo = {
            "numCliente": numCliente,
            "nombre": nombre,
            "numCuenta": numCuenta,
            "saldo": saldo
        }
        self.__validarCredenciales(registroNuevo)

        if not numCuenta:
            registroNuevo["saldo"] = None

        try:
            lector = LectorCSV(self.nombreArchivo)
            registros = lector.leer_archivo()
            for registro in registros:
                registroExistente={
                    "numCliente": registro.split(",")[0],
                    "nombre": registro.split(",")[1],
                    "numCuenta": registro.split(",")[2],
                    "saldo": registro.split(",")[3]
                }
                if (str(registroNuevo.get("numCliente")) == registroExistente.get("numCliente")) and (registroNuevo.get("nombre") != registroExistente.get("nombre")):
                    raise NumClienteExistenteExcepcion(f"ERROR: Numero de Cliente {registroNuevo.get('numCliente')} ya registrado")
                elif str(registroNuevo.get("numCuenta")) == registroExistente.get("numCuenta"):
                    raise NumClienteExistenteExcepcion(f"ERROR: Numero de Cuenta #{registroNuevo.get('numCuenta')} ya registrado")
            
            escritor = EscritorCSV(self.nombreArchivo)
            escritor.add(registroNuevo)
        except CuentaExistenteExcepcion as e:
            print(e.mensaje)
        except NumClienteExistenteExcepcion as e:
            print(e.mensaje)
