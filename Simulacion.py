import simpy
import random

# Generador de Procesos/Programas
def OS(env, RAM, CPU, number, interval, clockSpeed):
    for i in range(number):
        instructions = random.randint(1,10) # Instrucciones a completar por el CPU 
        ramAsigned = random.randint(1,10) # Memoria RAM que ocupara
        env.process(program(env, 'Proceso %i' % i, CPU, RAM, instructions, ramAsigned, clockSpeed)) 
        yield env.timeout(random.expovariate(1.0 / interval)) # Simula el tiempo en que se llega un proceso nuevo a la cola


def program(env, name, CPU, RAM, instructions, ramAsigned, clockSpeed):

    print('%f %s Proceso en New. RAM requerida: %i RAM disponible: %i' % (env.now, name, ramAsigned, RAM.level))
    yield RAM.get(ramAsigned) # Pide la memoria necesaria

    while (instructions > 0):
        # Entra en ready
        print('%f %s Proceso en Ready. Instrucciones restantes: %i ' % (env.now, name, instructions))
        instructions -= clockSpeed 
            
        

env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100) # Memoria RAM inicial
CPU = simpy.Resource(env, 1) # Cantidad de CPUs disponibles
numProcesses = 25 # Numero total de procesos a ser corridos en el OS
interval = 10 # Intervalo para generar tiempos al azar de llegada de procesos
clockSpeed = 3 # Velocidad de un ciclo de reloj
env.process(OS(env, RAM, CPU, numProcesses, interval, clockSpeed))
env.run()



