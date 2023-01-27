from controlador import Controlador
from modelo import LectorCSV
from numpy.random import randint

if __name__=="__main__":
    controlador = Controlador("ejemplo.csv")
    lector = LectorCSV("ejemplo.csv")
    controlador.crearRegistro(numCliente= 7177451234464407, nombre = "Elizabeth Delgado", saldo = 100.20)