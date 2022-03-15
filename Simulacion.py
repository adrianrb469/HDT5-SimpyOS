import simpy
import random



def program(env, name, CPU, RAM, instructions, ramAsigned, clock_speed, arrival, interval):

    yield env.timeout(random.expovariate(1.0 / interval))  # Simula el tiempo en que se llega un proceso nuevo a la cola
    current_time = env.now  

    print('t=%i %s en New. RAM requerida: %i RAM disponible: %i' % (env.now, name, ramAsigned, RAM.level))
    yield RAM.get(ramAsigned) # Pide la memoria necesaria
    
    while (instructions > 0):
        # Entra en ready
        print('t=%i %s en Ready. Instrucciones restantes: %i ' % (env.now, name, instructions))
        with CPU.request() as req:  #pide el procesador
            yield req
            instructions -= clock_speed 
            yield env.timeout(1) # Un ciclo de reloj
            # Estado despues de 1 ciclo
            print('t=%i %s en Running. Instrucciones restantes: %i ' % (env.now, name, instructions))
    
    yield  RAM.put(ramAsigned)
    print('t=%i %s Terminated. RAM devuelta: %i RAM disponible: %i' % (env.now, name, ramAsigned, RAM.level))
    # Calcula el tiempo total de la simulacion
    global total_time
    total_time += env.now - current_time
    print('Tiempo total %d' % (env.now - current_time))

random.seed(10)
env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100) # Memoria RAM inicial
CPU = simpy.Resource(env, 1) # Cantidad de CPUs disponibles
total_time = 0


num_processes = 200 # Numero total de procesos a ser corridos en el OS
 # Intervalo para generar tiempos al azar de llegada de procesos
clock_speed = 3 # Velocidad de un ciclo de reloj

for i in range(num_processes):
        arrival = 0
        instructions = random.randint(1,10) # Instrucciones a completar por el CPU 
        ramAsigned = random.randint(1,10) # Memoria RAM que necesita el proceso
        env.process(program(env, '[Proceso%i]' % i, CPU, RAM, instructions, ramAsigned, clock_speed, arrival, 5)) 
    
        
       
env.run()
print('Tiempo promedio %d ' % (total_time / num_processes))

