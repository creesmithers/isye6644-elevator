#### For elevator controls & everything else
import simpy
import random

SIM_TIME = 50
PASSENGER_INTERVAL = 10

### Passenger
class Passenger:
    def __init__ (self, pid, pickup, destination):
        self.id = pid
        self.pickup = pickup
        self.destination = destination
        # arrival time?
        # 

    def __repr__(self):
        return f"P{self.id}({self.pickup} --> {self.destination})"
        

class Control_System:
    def __init__ (self, floor1: list, floor2: list, floor3: list):
        self.floor1 = floor1
        self.floor2 = floor2
        self.floor3 = floor3

class Elevator:
    pass

def passenger_generator(env, ):
    pid = 1
    while True:
        yield env.timeout(random.expovariate(1.0 / PASSENGER_INTERVAL))
        pickup = random.randint(0, 2)
        destination = random.randint(0, 2)
        while destination == pickup:
            destination = random.randint(0,2)

        passenger = Passenger(pid, pickup, destination)
        print(f"[{env.now:.1f}] Passenger {pid} arrived at floor {pickup} --> {destination}")
        pid += 1


env = simpy.Environment()
env.process(passenger_generator(env))
env.run(until = SIM_TIME)