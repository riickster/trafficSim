class TrafficLight:
    def __init__(self, roads, config={}):
        self.roads = roads
        self.__set_default_config()
        self.__init_properties()
        
        for attr, val in config.items():
            setattr(self, attr, val)

    def __set_default_config(self):
        self.cycle = [(False, True), (True, False)]
        self.slow_distance = 50
        self.slow_factor = 0.4
        self.stop_distance = 15

        self.current_cycle_index = 0

        self.last_t = 0

    def __init_properties(self):
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self):
        return self.cycle[self.current_cycle_index]
    
    def update(self, sim):
        cycle_length = 15
        k = (sim.time // cycle_length) % 2
        self.current_cycle_index = int(k)
