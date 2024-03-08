import pygame
import numpy as np
from pygame import gfxdraw

class Window:
    def __init__(self, simulation, config={}):
        self.sim = simulation
        self.__set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)
        
    def __set_default_config(self):
        self.frames_per_second = 60
        self.zoom_level = 10
        self.window_width = 1280
        self.window_height = 720
        self.window_offset = (0, 0)
        
        self.background_colour = (250, 250, 250)

        self.mouse_onClick = False
        self.mouse_coordinates = (0, 0)

    def loop(self, loop=None):
        running = True

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        clock = pygame.time.Clock()

        pygame.font.init()
        self.text_font = pygame.font.SysFont('Arial', 16)

        while running:
            if(loop): loop(self.sim)

            self.draw()

            pygame.display.update()
            clock.tick(self.frames_per_second)

            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    running = False
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    if(event.button == 1):
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.window_offset
                        self.mouse_coordinates = (x-x0*self.zoom_level, y-y0*self.zoom_level)
                        self.mouse_onClick = True
                    if(event.button == 4):
                        self.zoom_level *= (self.zoom_level**2+self.zoom_level/4+1) / (self.zoom_level**2+1)
                    if(event.button == 5):
                        self.zoom_level *= (self.zoom_level**2+1) / (self.zoom_level**2+self.zoom_level / 4+1)
                elif(event.type == pygame.MOUSEMOTION):
                    if(self.mouse_onClick):
                        x1, y1 = self.mouse_coordinates
                        x2, y2 = pygame.mouse.get_pos()
                        self.window_offset = ((x2-x1) / self.zoom_level, (y2-y1) / self.zoom_level)
                elif(event.type == pygame.MOUSEBUTTONUP):
                    self.mouse_onClick = False           

    def run(self, steps_per_update=1):
        def loop(simulation):
            simulation.run(steps_per_update)
        self.loop(loop)

    def convert(self, x, y=None):
        if(isinstance(x, list)):
            return [self.convert(e[0], e[1]) for e in x]
        if(isinstance(x, tuple)):
            return self.convert(*x)
        return (int(self.window_width / 2 + (x + self.window_offset[0])*self.zoom_level), int(self.window_height / 2 + (y + self.window_offset[1])*self.zoom_level))

    def inverse_convert(self, x, y=None):
        if(isinstance(x, list)):
            return [self.convert(e[0], e[1]) for e in x]
        if(isinstance(x, tuple)):
            return self.convert(*x)
        return (int(-self.window_offset[0] + (x - self.window_width / 2) / self.zoom_level), int(-self.window_offset[1] + (y - self.window_height / 2) / self.zoom_level))

    def background(self, r, g, b):
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        gfxdraw.line(self.screen,*start_pos,*end_pos,color)

    def rect(self, pos, size, color):
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if(filled): 
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if(filled): gfxdraw.filled_polygon(self.screen, vertices, color)

    def rot_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        x, y = pos
        l, h = size

        if(angle):
            cos, sin = np.cos(angle), np.sin(angle)
        
        vertex = lambda e1, e2: (x + (e1*l*cos + e2*h*sin)/2,y + (e1*l*sin - e2*h*cos)/2)

        if(centered):
            vertices = self.convert([vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]])
        else:
            vertices = self.convert([vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]])

        self.polygon(vertices, color, filled=filled)

    def rot_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rot_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(255, 255, 255)):
        if(angle):
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rot_box(pos, size, cos=(cos - sin) / np.sqrt(2), sin=(cos + sin) / np.sqrt(2), color=color, centered=False)
        self.rot_box(pos, size, cos=(cos + sin) / np.sqrt(2), sin=(sin - cos) / np.sqrt(2), color=color, centered=False)


    def generate_axes(self, color=(100, 100, 100)):
        x_s, y_s = self.inverse_convert(0, 0)
        x_e, y_e = self.inverse_convert(self.window_width, self.window_height)
        self.line(self.convert((0, y_s)), self.convert((0, y_e)), color)
        self.line(self.convert((x_s, 0)),self.convert((x_e, 0)),color)

    def generate_grid(self, unit=50, color=(150,150,150), renderCoordinates=False):
        x_s, y_s = self.inverse_convert(0, 0)
        x_e, y_e = self.inverse_convert(self.window_width, self.window_height)

        n_x = int(x_s / unit)
        n_y = int(y_s / unit)
        m_x = int(x_e / unit)+1
        m_y = int(y_e / unit)+1

        if(renderCoordinates):
            coordinate_texts = {}
            font = pygame.font.Font(None, 15)
            for i in range(n_x, m_x):
                for j in range(n_y, m_y):
                    text = f"({i*10}, {j*10})"
                    text_surface = font.render(text, True, (0,0,0))
                    coordinate_texts[(i, j)] = text_surface
            for (i, j), text_surface in coordinate_texts.items():
                text_rect = text_surface.get_rect(center=self.convert((unit*i, unit*j)))
                self.screen.blit(text_surface, text_rect)

        for i in range(n_x, m_x):
            for j in range(n_y, m_y):
                self.line(self.convert((unit*i, y_s)), self.convert((unit*i, y_e)), color)
                self.line(self.convert((x_s, unit*j)), self.convert((x_e, unit*j)),color)

    def generate_roads(self):
        for road in self.sim.generated_roads:
            self.rot_box(road.origin, (road.length, 3.7), cos=road.cos, sin=road.sin, color=(74, 74, 79), centered=False)
            self.rot_box(road.origin, (road.length, 0.25), cos=road.cos, sin=road.sin, color=(0, 0, 0), centered=False)
            if(road.length > 5): 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (road.origin[0] + (road.length / 2 + i + 3) * road.cos, road.origin[1] + (road.length / 2 + i + 3) * road.sin)
                    self.arrow(pos, (-1.25, 0.2), cos=road.cos, sin=road.sin) 

    def generate_vehicle(self, vehicle, road):
        l, h = vehicle.length,  2
        sin, cos = road.sin, road.cos

        x = road.origin[0] + cos * vehicle.x 
        y = road.origin[1] + sin * vehicle.x 

        self.rot_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def generate_vehicles(self):
        for road in self.sim.generated_roads:
            for vehicle in road.vehicles:
                self.generate_vehicle(vehicle, road)

    def generate_traffic_ligths(self):
        for signal in self.sim.traffic_lights:
            for i in range(len(signal.roads)):
                color = (0, 255, 0) if(signal.current_cycle[i]) else (255, 0, 0)
                for road in signal.roads[i]:
                    position = ( 1*road.end[0] + 0*road.origin[0], 1*road.end[1] + 0*road.origin[1])
                    self.rot_box(position, (1, 3), cos=road.cos, sin=road.sin, color=color)


    def draw(self):
        self.background(*self.background_colour)

        self.generate_grid(10, (220,220,220))
        self.generate_grid(100, (200,200,200))
        self.generate_axes()

        self.generate_roads()
        self.generate_vehicles()
        self.generate_traffic_ligths()
        