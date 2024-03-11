from scipy.spatial import distance
from collections import deque

class Road:
    def __init__(self, origin, end):
        self.origin = origin
        self.end = end
        self.vehicles = deque()

        self.__init_properties()

    def __init_properties(self):
        self.has_traffic_signal = False
        self.length = distance.euclidean(self.origin, self.end)
        self.sin = (self.end[1]-self.origin[1]) / self.length
        self.cos = (self.end[0]-self.origin[0]) / self.length

    def set_traffic_signal(self, signal, group):
        self.has_traffic_signal = True
        self.traffic_signal = signal
        self.traffic_signal_group = group

    @property
    def traffic_signal_state(self):
        if(self.has_traffic_signal):
            i = self.traffic_signal_group
            return self.traffic_signal.current_cycle[i]
        return True

    def update(self, dt):
        n = len(self.vehicles)

        if(n > 0):
            self.vehicles[0].update(None, dt)
            for i in range(1, n):
                leader = self.vehicles[i-1]
                self.vehicles[i].update(leader, dt)

            if(self.traffic_signal_state):
                self.vehicles[0].go()
                for vehicle in self.vehicles:
                    vehicle.accelerate()
            else:
                if(self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance):
                    self.vehicles[0].slow(self.traffic_signal.slow_factor*self.vehicles[0]._max_velocity)

                if(self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2):
                    self.vehicles[0].stop()
