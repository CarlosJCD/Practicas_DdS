from controlador import Controlador
from modelo import Lector
from numpy.random import randint

if __name__ == "__main__":
    controlador: Controlador = Controlador()
    controlador.crear_cliente(int(randint(1e15,1e16,1)[0]),"Elias Madera",int(randint(1e15,1e16,1)[0]),250.95)