from re import compile
from modelo import LectorCSV, EscritorCSV
from Excepciones.Registros import CuentaExistenteExcepcion, NumClienteExistenteExcepcion
from Excepciones.Credenciales import CredencialesInvalidasExcepcion

class Controlador:
    """ 
    Atributos
    ---------
    nombre_archivo: str
        Cadena que representa la ruta del archivo con el cual va a estar trabajando el controlador
    
    Metodos
    -------
    __validar_credenciales(registro: dict)
            Valida las credenciales de un registro
    crear_Registro(num_cliente: int, nombre: str, num_cuenta: int, saldo: float)


    """

    def __init__(self, nombre_archivo: str) -> None:
        self.nombre_archivo = nombre_archivo

    def __validar_credenciales(self,registro: dict) -> None:
        patron_num = compile("^\d{16}$")
        patron_saldo = compile("^\d*.\d*$")
        patron_nombre = compile("^[A-Za-z]{2,25}\s[A-Za-z]{2,25}$")

        condicion_num_cuenta = patron_num.search(str(registro.get("numCuenta"))) or not registro.get("numCuenta")
        condicion_num_cliente = patron_num.search(str(registro.get("numCliente")))
        condicion_saldo = patron_saldo.search(str(registro.get("saldo")))
        condicion_nombre = patron_nombre.search(str(registro.get("nombre")))
        try:
            if not condicion_num_cuenta:
                raise CredencialesInvalidasExcepcion(credencial = "Num. Cuenta", valor = registro.get("numCuenta"))
            elif not condicion_num_cliente:
                raise CredencialesInvalidasExcepcion(credencial = "Num. Cliente", valor= registro.get("numCliente"))
            elif not condicion_saldo:
                raise CredencialesInvalidasExcepcion(credencial = "Saldo", valor= registro.get("saldo"))
            elif not condicion_nombre:
                raise CredencialesInvalidasExcepcion(credencial = "Nombre", valor= registro.get("nombre"))
        except CredencialesInvalidasExcepcion as excepcion_credencial:
            print(excepcion_credencial)           
    def crear_registro(self,num_cliente: int, nombre: str, num_cuenta: int, saldo: float = 0.0):
        """
        Crea un registro valido con la siguiente estructura:

        num_cliente,nombre,num_cuenta,saldo

        Parametros
        --------------
        num_cliente: int
            Entero que representa el numero de cliente. Debe ser de 16 digitos
        nombre: String
            Cadena que representa el nombre del cliente
        num_cuenta: int
            Entero que representa el numero de cuenta. Debe ser de 16 digitos
        saldo: float
            Flotante que representa el saldo de la cuenta. Su valor por defecto es 0.0
        
        Excepciones
        -----------
        NumClienteExistenteExcepcion: 
            Excepcion levantada cuando num_cliente del nuevo registro y num_cliente del registro actual coinciden pero los nombres de cliente no coinciden
        NumCuentaExistenteExcepcion:
            Excepcion levantada cuando el valor de num_cuenta ya fue registrado.
        
        Return
        ------
        None
        """
        registro_nuevo = {
            "numCliente": num_cliente,
            "nombre": nombre,
            "numCuenta": num_cuenta,
            "saldo": saldo
        }
        self.__validar_credenciales(registro_nuevo)

        if not num_cuenta:
            registro_nuevo["saldo"] = None

        try:
            lector = LectorCSV(self.nombre_archivo)
            registros = lector.leer_archivo()
            for registro in registros:
                registroExistente={
                    "numCliente": registro.split(",")[0],
                    "nombre": registro.split(",")[1],
                    "numCuenta": registro.split(",")[2],
                    "saldo": registro.split(",")[3]
                }
                if (str(registro_nuevo.get("numCliente")) == registroExistente.get("numCliente")) and (registro_nuevo.get("nombre") != registroExistente.get("nombre")):
                    raise NumClienteExistenteExcepcion(f"ERROR: Numero de Cliente {registro_nuevo.get('numCliente')} ya registrado")
                elif str(registro_nuevo.get("numCuenta")) == registroExistente.get("numCuenta"):
                    raise NumClienteExistenteExcepcion(f"ERROR: Numero de Cuenta #{registro_nuevo.get('numCuenta')} ya registrado")
            
            escritor = EscritorCSV(self.nombre_archivo)
            escritor.add(registro_nuevo)
        except CuentaExistenteExcepcion as excepcion:
            print(excepcion.mensaje)
        except NumClienteExistenteExcepcion as excepcion:
            print(excepcion.mensaje)
