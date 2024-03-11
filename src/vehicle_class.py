import uuid
import random
import numpy as np

class Vehicle:
    def __init__(self, config={}, messaging_channel=None):
        self.messaging_channel = messaging_channel
        self.__set_default_config()
        self.__init_properties()

        for attr, val in config.items():
            setattr(self, attr, val)

    def __set_default_config(self):    
        self.length = 4
        self.s0 = 4
        self.time = 1
        self.max_velocity = 16.6
        self.max_acceleration = 1.44
        self.b_max = 4.61
        self.uuid = uuid.uuid4()

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.velocity = self.max_velocity
        self.acceleration = 0
        self.isStopped = False

        self.messaging_channel.register_agent(self.uuid)

    def __init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.max_acceleration*self.b_max)
        self._max_velocity = self.max_velocity

    def update(self, leader, dt):
        if(len(self.messaging_channel.read_messages()) != 0):
            last_message = self.messaging_channel.read_messages()[-1]
            if(last_message.get("uuid") != self.uuid):
                if(random.random() < 0.1):
                    self.messaging_channel.send_message({"uuid": self.uuid, "message": "OK"})

        if(self.velocity + self.acceleration*dt < 0):
            self.x -= 1 / 2*self.velocity*self.velocity / self.acceleration
            self.velocity = 0
        else:
            self.velocity += self.acceleration*dt
            self.x += self.velocity*dt + self.acceleration*dt*dt / 2

        alpha = 0
        if(leader):
            delta_x = leader.x - self.x - leader.length
            delta_v = self.velocity - leader.velocity

            alpha = (self.s0 + max(0, self.time*self.velocity + delta_v*self.velocity/self.sqrt_ab)) / delta_x

        self.acceleration = self.max_acceleration * (1-(self.velocity/self.max_velocity)**4 - alpha**2)

        if(self.isStopped):
            self.acceleration = -self.b_max*self.velocity / self.max_velocity
            self.messaging_channel.send_message({"uuid": self.uuid, "message": "STOPPED"})
        
    def stop(self):
        self.isStopped = True

    def go(self):
        self.isStopped = False

    def slow(self, v):
        self.max_velocity = v

    def accelerate(self):
        self.max_velocity = self._max_velocity
        

