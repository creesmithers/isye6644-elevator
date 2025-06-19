import simpy
import random
from statistics import mean
import itertools


# Global Constants
RANDOM_SEED = 42           # Set the random seed so that results are reproduceable
ID_SERVICE_TIME = 0.75     # Mean service time for ID check (exponential, minutes)
ARRIVAL_INTER = 1/20        # Mean interarrival time = 1 / lambda (minutes)
SIM_TIME = 240             # Simulation time (minutes)
SCANNER_TIME_MIN = 0.5     # Minimum scanner time (uniform, minutes)
SCANNER_TIME_MAX = 1.0     # Maximum scanner time (uniform, minutes)

class IDCheck(object):
    """Simulate the ID/boarding-pass check process."""
    def __init__(self, env, num_id_checkers):
        self.env = env
        self.resource = simpy.Resource(env, num_id_checkers)  # Pass number of checkers here
        self.servicetime = ID_SERVICE_TIME

    def serve(self, passenger):
        delay = random.expovariate(1.0 / self.servicetime)
        yield self.env.timeout(delay)

class PersonalScanner(object):
    """Simulate the personal scanner process."""
    def __init__(self, env, scanner_id):
        self.env = env
        self.resource = simpy.Resource(env, 1)  # One resource per scanner
        self.scanner_id = scanner_id

    def scan(self, passenger):
        delay = random.uniform(SCANNER_TIME_MIN, SCANNER_TIME_MAX)
        yield self.env.timeout(delay)

def passenger(env, name, id_station, scanners, wait_times):

    """Simulate a passenger going through ID check and personal scanner."""
    arrival_time = env.now
    with id_station.resource.request() as request:
        yield request
        yield env.process(id_station.serve(name))
    scanner_queues = [len(scanner.resource.queue) for scanner in scanners]
    chosen_scanner = scanners[scanner_queues.index(min(scanner_queues))]
    with chosen_scanner.resource.request() as request:
        yield request
        yield env.process(chosen_scanner.scan(name))
    total_time = env.now - arrival_time
    wait_times.append(total_time)

def setup(env, num_id_checkers, num_scanners, arrival_inter, wait_times):
    """Create ID check and scanners, and generate passengers."""
    id_station = IDCheck(env, num_id_checkers)
    scanners = [PersonalScanner(env, i) for i in range(num_scanners)]
    passenger_count = itertools.count()
    while True:
        interarrival = random.expovariate(1.0 / arrival_inter)
        yield env.timeout(interarrival)
        env.process(passenger(env, f'Passenger {next(passenger_count)}', id_station, scanners, wait_times))

# Test different configurations
print("Airport Security Simulation Results")
print("------------------------------------")
sim_trial = 0
results = []  # Store results for summary

for id_checkers in range(1, 6):  # Test 1 to 4 ID checkers
    for personal_scanners in range(1, 6):  # Test 1 to 4 scanners
        sim_trial += 1
        wait_times = []  # Reset wait times for each trial
        random.seed(RANDOM_SEED)
        env = simpy.Environment()
        env.process(setup(env, id_checkers, personal_scanners, ARRIVAL_INTER, wait_times))
        env.run(until=SIM_TIME)

        avg_time = mean(wait_times) if wait_times else float('inf')
        results.append((id_checkers, personal_scanners, avg_time))
        print(f"Trial {sim_trial}: {id_checkers} ID Checkers, {personal_scanners} Scanners - Avg Time: {avg_time:.2f} minutes")

# Summary of configurations meeting the 15-minute goal
print("\nConfigurations with Average Time < 15 Minutes:")
for id_checkers, scanners, avg_time in results:
    if avg_time < 15:
        print(f"ID Checkers: {id_checkers}, Scanners: {scanners}, Avg Time: {avg_time:.2f} minutes")


# Test NEW configurations with higher upper bound
print("Airport Security Simulation Results")
print("------------------------------------")
sim_trial = 0
results = []  # Store results for summary

for id_checkers in range(1, 16):  # Test 1 to 4 ID checkers
    for personal_scanners in range(1, 16):  # Test 1 to 4 scanners
        sim_trial += 1
        wait_times = []  # Reset wait times for each trial
        random.seed(RANDOM_SEED)
        env = simpy.Environment()
        env.process(setup(env, id_checkers, personal_scanners, ARRIVAL_INTER, wait_times))
        env.run(until=SIM_TIME)

        avg_time = mean(wait_times) if wait_times else float('inf')
        results.append((id_checkers, personal_scanners, avg_time))
        print(f"Trial {sim_trial}: {id_checkers} ID Checkers, {personal_scanners} Scanners - Avg Time: {avg_time:.2f} minutes")

# Summary of configurations meeting the 15-minute goal
print("\nConfigurations with Average Time < 15 Minutes:")
for id_checkers, scanners, avg_time in results:
    if avg_time < 15:
        print(f"ID Checkers: {id_checkers}, Scanners: {scanners}, Avg Time: {avg_time:.2f} minutes")
