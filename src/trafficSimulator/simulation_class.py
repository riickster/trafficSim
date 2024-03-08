from .road_class import Road
from copy import deepcopy
from .vehicle_gen import VehicleGenerator
from .traffic_lights import TrafficLight
from .global_messages import Messaging

class Simulation:
    def __init__(self, config={}):
        self.__set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def __set_default_config(self):
        self.time = 0.0
        self.frame_count = 0
        self.delta_time = 1/60

        self.generated_roads = []
        self.vehicle_generators = []
        self.traffic_lights = []
        self.message_channel = Messaging()

    def generate_road(self, start, end):
        road = Road(start, end)
        self.generated_roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.generate_road(*road)

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config, self.message_channel)
        self.vehicle_generators.append(gen)
        return gen

    def create_traffic_light(self, roads, config={}):
        roads = [[self.generated_roads[i] for i in road_group] for road_group in roads]
        sig = TrafficLight(roads, config)
        self.traffic_lights.append(sig)
        return sig

    def update(self):
        for road in self.generated_roads:
            road.update(self.delta_time)

        for generator in self.vehicle_generators:
            generator.update()

        for signal in self.traffic_lights:
            signal.update(self)

        for generated_road in self.generated_roads:
            if(len(generated_road.vehicles) == 0): 
                continue
            
            vehicle = generated_road.vehicles[0]
            if(vehicle.x >= generated_road.length):
                if(vehicle.current_road_index + 1 < len(vehicle.path)):
                    vehicle.current_road_index += 1
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.generated_roads[next_road_index].vehicles.append(new_vehicle)
                generated_road.vehicles.popleft()
        self.time += self.delta_time
        self.frame_count += 1


    def run(self, steps):
        for _ in range(steps):
            self.update()