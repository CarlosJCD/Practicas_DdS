from controlador import Controlador
from modelo import LectorCSV
from numpy.random import randint

if __name__=="__main__":
    controlador = Controlador("ejemplo.csv")
    lector = LectorCSV("ejemplo.csv")