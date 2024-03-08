import uuid
import random
import numpy as np

class Vehicle:
    def __init__(self, config={}, messaging_channel=None):
        # Set default configuration
        self.messaging_channel = messaging_channel
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):    
        self.l = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61
        self.uuid = uuid.uuid4()

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

        self.messaging_channel.register_agent(self.uuid)
        self.allow_message = True

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        # Update position and velocity
        if(len(self.messaging_channel.read_messages()) != 0):
            last_message = self.messaging_channel.read_messages()[-1]
            if(last_message.get("uuid") != self.uuid):
                if(random.random() < 0.1):
                    self.messaging_channel.send_message({"uuid": self.uuid, "message": "OK"})

        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)

        if self.stopped:
            self.a = -self.b_max*self.v/self.v_max
            self.messaging_channel.send_message({"uuid": self.uuid, "message": "STOPPED"})
        
    def stop(self):
        self.stopped = True

    def go(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def accelerate(self):
        self.v_max = self._v_max
        

