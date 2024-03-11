from numpy.random import randint
from vehicle_class import Vehicle

class VehicleGenerator:
    def __init__(self, sim, config={}, messaging_channel=None):
        self.sim = sim
        self.messaging_channel = messaging_channel
        
        self.__set_default_config()
        
        for attr, val in config.items():
            setattr(self, attr, val)

        self.__init_properties()


    def __set_default_config(self):
        self.last_added_time = 0
        self.vehicle_rate = 20
        self.vehicles = [(1, {})]

    def __init_properties(self):
        self.upcoming_vehicle = self.generate_vehicle()

    def generate_vehicle(self):
        r = randint(1, sum(pair[0] for pair in self.vehicles) + 1)
        for (weight, config) in self.vehicles:
            r -= weight
            if(r <= 0):
                return Vehicle(config, self.messaging_channel)

    def update(self):
        if(self.sim.time - self.last_added_time >= 60 / self.vehicle_rate):
            road = self.sim.generated_roads[self.upcoming_vehicle.path[0]]      
            if(len(road.vehicles) == 0 or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.length):
                self.upcoming_vehicle.time_added = self.sim.time
                road.vehicles.append(self.upcoming_vehicle)
                self.last_added_time = self.sim.time
            self.upcoming_vehicle = self.generate_vehicle()

