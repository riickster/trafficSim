import pygame
import numpy as np
from pygame import gfxdraw

class Window:
    def __init__(self, simulation, config={}):
        self.simulation = simulation
        self.__set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)
        
    def __set_default_config(self):

        #* Window Properties
        self.fps = 60
        self.zoom = 5
        self.window_width = 1280
        self.window_height = 720
        self.offset = (0, 0)

        #* Style
        
        #TODO Set styled variables
        # self.background_colour = (79, 58, 43) #Dirt
        self.background_colour = (250, 250, 250) # White
        # self.road_colour

        #* Mouse Variables
        self.mouse_onClick = False
        self.mouse_coordinates = (0, 0)

    def loop(self, loop=None):
        running = True

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        clock = pygame.time.Clock() # Initialize Clock to Fix FPS

        pygame.font.init() # Initialize Font
        self.text_font = pygame.font.SysFont('Arial', 16)

        #* Draw loop
        while running:
            if(loop):
                loop(self.simulation)

            self.draw() # Draw simulation on GE

            #* Send Frames to Display
            pygame.display.update()
            clock.tick(self.fps)

            #* Handle all events
            for event in pygame.event.get():
                if(event.type == pygame.QUIT): # Quit
                    running = False
                elif(event.type == pygame.MOUSEBUTTONDOWN): # Handle mouse events
                    if(event.button == 1): # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = self.offset
                        self.mouse_coordinates = (x-x0*self.zoom, y-y0*self.zoom)
                        self.mouse_onClick = True
                    if(event.button == 4): # Mouse wheel up
                        self.zoom *= (self.zoom**2+self.zoom/4+1) / (self.zoom**2+1)
                    if event.button == 5: # Mouse wheel down
                        self.zoom *= (self.zoom**2+1) / (self.zoom**2+self.zoom/4+1)
                elif event.type == pygame.MOUSEMOTION: # Drag content
                    if self.mouse_onClick:
                        x1, y1 = self.mouse_coordinates
                        x2, y2 = pygame.mouse.get_pos()
                        self.offset = ((x2-x1)/self.zoom, (y2-y1)/self.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_onClick = False           

    #* Runs the simulation by updating in every loop
    def run(self, steps_per_update=1):
        def loop(simulation):
            simulation.run(steps_per_update)
        self.loop(loop)

    #* Converts simulation coordinates to screen coordinates
    def convert(self, x, y=None):
        if(isinstance(x, list)):
            return [self.convert(e[0], e[1]) for e in x]
        if(isinstance(x, tuple)):
            return self.convert(*x)
        return (int(self.window_width/2 + (x + self.offset[0])*self.zoom), int(self.window_height/2 + (y + self.offset[1])*self.zoom))

    def inverse_convert(self, x, y=None):
        """Converts screen coordinates to simulation coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (
            int(-self.offset[0] + (x - self.window_width/2)/self.zoom),
            int(-self.offset[1] + (y - self.window_height/2)/self.zoom)
        )


    def background(self, r, g, b):
        """Fills screen with one color."""
        self.screen.fill((r, g, b))

    def line(self, start_pos, end_pos, color):
        """Draws a line."""
        gfxdraw.line(
            self.screen,
            *start_pos,
            *end_pos,
            color
        )

    def rect(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.rectangle(self.screen, (*pos, *size), color)

    def box(self, pos, size, color):
        """Draws a rectangle."""
        gfxdraw.box(self.screen, (*pos, *size), color)

    def circle(self, pos, radius, color, filled=True):
        gfxdraw.aacircle(self.screen, *pos, radius, color)
        if filled:
            gfxdraw.filled_circle(self.screen, *pos, radius, color)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def rotated_box(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255), filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        vertex = lambda e1, e2: (
            x + (e1*l*cos + e2*h*sin)/2,
            y + (e1*l*sin - e2*h*cos)/2
        )

        if centered:
            vertices = self.convert(
                [vertex(*e) for e in [(-1,-1), (-1, 1), (1,1), (1,-1)]]
            )
        else:
            vertices = self.convert(
                [vertex(*e) for e in [(0,-1), (0, 1), (2,1), (2,-1)]]
            )

        self.polygon(vertices, color, filled=filled)

    def rotated_rect(self, pos, size, angle=None, cos=None, sin=None, centered=True, color=(0, 0, 255)):
        self.rotated_box(pos, size, angle=angle, cos=cos, sin=sin, centered=centered, color=color, filled=False)

    def arrow(self, pos, size, angle=None, cos=None, sin=None, color=(255, 255, 255)):
        if angle:
            cos, sin = np.cos(angle), np.sin(angle)
        
        self.rotated_box(
            pos,
            size,
            cos=(cos - sin) / np.sqrt(2),
            sin=(cos + sin) / np.sqrt(2),
            color=color,
            centered=False
        )

        self.rotated_box(
            pos,
            size,
            cos=(cos + sin) / np.sqrt(2),
            sin=(sin - cos) / np.sqrt(2),
            color=color,
            centered=False
        )


    def draw_axes(self, color=(100, 100, 100)):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.window_width, self.window_height)
        self.line(
            self.convert((0, y_start)),
            self.convert((0, y_end)),
            color
        )
        self.line(
            self.convert((x_start, 0)),
            self.convert((x_end, 0)),
            color
        )

    def draw_grid(self, unit=50, color=(150,150,150), renderCoordinates=False):
        x_start, y_start = self.inverse_convert(0, 0)
        x_end, y_end = self.inverse_convert(self.window_width, self.window_height)

        n_x = int(x_start / unit)
        n_y = int(y_start / unit)
        m_x = int(x_end / unit)+1
        m_y = int(y_end / unit)+1

        if(renderCoordinates):
            # Pre-render text for all coordinates
            coordinate_texts = {}
            font = pygame.font.Font(None, 15)
            for i in range(n_x, m_x):
                for j in range(n_y, m_y):
                    text = f"({i*10}, {j*10})"
                    text_surface = font.render(text, True, (0,0,0))
                    coordinate_texts[(i, j)] = text_surface

        # Draw grid lines
        for i in range(n_x, m_x):
            self.line(
                self.convert((unit*i, y_start)),
                self.convert((unit*i, y_end)),
                color
            )
        for j in range(n_y, m_y):
            self.line(
                self.convert((x_start, unit*j)),
                self.convert((x_end, unit*j)),
                color
            )

        if(renderCoordinates):
            # Blit pre-rendered text onto the screen
            for (i, j), text_surface in coordinate_texts.items():
                text_rect = text_surface.get_rect(center=self.convert((unit*i, unit*j)))
                self.screen.blit(text_surface, text_rect)

        # for i in range(n_x, m_x):
        #     self.line(
        #         self.convert((unit*i, y_start)),
        #         self.convert((unit*i, y_end)),
        #         color
        #     )
        # for i in range(n_y, m_y):
        #     self.line(
        #         self.convert((x_start, unit*i)),
        #         self.convert((x_end, unit*i)),
        #         color
        #     )

    def draw_roads(self):
        for road in self.simulation.roads:
            # Draw road background
            self.rotated_box(
                road.start,
                (road.length, 3.7),
                cos=road.angle_cos,
                sin=road.angle_sin,
                color=(74, 74, 79),
                centered=False
            )
            # Draw road lines
            # self.rotated_box(
            #     road.start,
            #     (road.length, 0.25),
            #     cos=road.angle_cos,
            #     sin=road.angle_sin,
            #     color=(0, 0, 0),
            #     centered=False
            # )

            # Draw road arrow
            if road.length > 5: 
                for i in np.arange(-0.5*road.length, 0.5*road.length, 10):
                    pos = (road.start[0] + (road.length/2 + i + 3) * road.angle_cos, road.start[1] + (road.length/2 + i + 3) * road.angle_sin)
                    self.arrow(pos, (-1.25, 0.2), cos=road.angle_cos, sin=road.angle_sin) 

    def draw_vehicle(self, vehicle, road):
        l, h = vehicle.l,  2
        sin, cos = road.angle_sin, road.angle_cos

        x = road.start[0] + cos * vehicle.x 
        y = road.start[1] + sin * vehicle.x 

        self.rotated_box((x, y), (l, h), cos=cos, sin=sin, centered=True)

    def draw_vehicles(self):
        for road in self.simulation.roads:
            # Draw vehicles
            for vehicle in road.vehicles:
                self.draw_vehicle(vehicle, road)

    def draw_signals(self):
        for signal in self.simulation.traffic_signals:
            for i in range(len(signal.roads)):
                color = (0, 255, 0) if signal.current_cycle[i] else (255, 0, 0)
                for road in signal.roads[i]:
                    a = 0
                    position = (
                        (1-a)*road.end[0] + a*road.start[0],        
                        (1-a)*road.end[1] + a*road.start[1]
                    )
                    self.rotated_box(
                        position,
                        (1, 3),
                        cos=road.angle_cos, sin=road.angle_sin,
                        color=color)

    def draw_status(self):
        text_fps = self.text_font.render(f't={self.simulation.t:.5}', False, (0, 0, 0))
        text_frc = self.text_font.render(f'n={self.simulation.frame_count}', False, (0, 0, 0))
        
        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_frc, (100, 0))


    def draw(self):
        # Fill background
        self.background(*self.background_colour)

        # Major and minor grid and axes
        self.draw_grid(10, (220,220,220))
        self.draw_grid(100, (200,200,200))
        self.draw_axes()

        self.draw_roads()
        self.draw_vehicles()
        self.draw_signals()

        # Draw status info
        self.draw_status()
        