from controlador import Controlador
from modelo import Lector
from numpy.random import randint

if __name__ == "__main__":
    lector: Lector = Lector(base_path="Clientes/",password="contraseña")
    controlador: Controlador = Controlador()
    #controlador.crear_cliente(int(randint(1e15,1e16,1)[0]),"Carlos Calderon",int(randint(1e15,1e16,1)[0]),120.74)
    #controlador.crear_cliente(int(randint(1e15,1e16,1)[0]),"Elias Madera",int(randint(1e15,1e16,1)[0]),00.00)
    #controlador.crear_cliente(int(randint(1e15,1e16,1)[0]),"Alejandro Victoria",int(randint(1e15,1e16,1)[0]),70.21)
    #controlador.crear_cliente(int(randint(1e15,1e16,1)[0]),"Diego Ortiz",int(randint(1e15,1e16,1)[0]),73.47)
    controlador.actualizar_cuenta(num_cliente=3216192211046181, num_cuenta= 1259448918565994, saldo=60000.00)
    lector.imprimir_registros()
    lector.generar_reporte()

