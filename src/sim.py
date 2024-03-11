from pygame_class import Window
from curve_class import curve_road
from simulation_class import Simulation

n = 15
sim = Simulation()

def road_class(a): 
    return range(a, a+n)

#North Fragments
I_NORTH_1_RIGHT_ORIGIN = (-10, 40)
NORTH_1_RIGHT_CHK_1 = (-10, 20)
I_NORTH_1_RIGHT_CHK_2 = (-10, 10)
NORTH_1_RIGHT_CHK_3 = (-10,0)
NORTH_1_RIGHT_CHK_4 = (0,-10)
NORTH_1_RIGHT_CHK_5 = (20, -20)
NORTH_1_RIGHT_CHK_6 = (20, -30)
NORTH_1_RIGHT_CHK_7 = (20, -60)
NORTH_2_RIGHT_ORIGIN = (-60, 0)
NORTH_2_RIGHT_CHK_1 = (-60, -40)
NORTH_2_RIGHT_CHK_2 = (-60, -60)
NORTH_3_RIGHT_CHK_1 = (80, 90)
NORTH_3_RIGHT_CHK_2 = (80, 40)
NORTH_3_RIGHT_CHK_3 = (80, 20)

#South Fragments
SOUTH_RIGHT_ORIGIN = (-50,50)
I_SOUTH_RIGHT_CHK_1 = (-20, 50)
SOUTH_RIGHT_CHK_2 = (-10, 50)
SOUTH_RIGHT_CHK_3 = (20, 50)
SOUTH_RIGHT_CHK_4 = (30, 60)
SOUTH_RIGHT_CHK_5 = (30, 90)
SOUTH_RIGHT_CHK_6 = (40, 100)
SOUTH_RIGHT_CHK_7 = (70, 100)
SOUTH_2_RIGHT_ORIGIN = (-60, 20)
SOUTH_2_RIGHT_CHK_1 = (-60, 40)
SOUTH_2_RIGHT_CHK_2 = (-60, -50)
SOUTH_2_RIGHT_CHK_3 = (-60, 10)
SOUTH_3_RIGHT_ORIGIN = (110, -60)
SOUTH_3_RIGHT_CHK_1 = (110, -20)
SOUTH_3_RIGHT_CHK_3 = (110, 0)

#West Fragments
I_WEST_1_RIGHT_ORIGIN = (-20, 10)
WEST_1_RIGHT_CHK_1 = (-50, 10)
WEST_1_RIGHT_CHK_2 = (100, 10)
WEST_1_RIGHT_CHK_3 = (70,10)
WEST_1_RIGHT_CHK_4 = (40, 10)
WEST_1_RIGHT_CHK_5 = (0, 10)

#East Fragments
EAST_1_RIGHT_ORIGIN = (10,-10)
I_EAST_1_RIGHT_CHK_1 = (100, -10)
EAST_2_RIGHT_ORIGIN = (-50, -70)
EAST_2_RIGHT_CHK_1 = (30, -70)
EAST_2_RIGHT_CHK_2 = (10, -70)
EAST_2_RIGHT_CHK_3 = (70, -70)
EAST_2_RIGHT_CHK_4 = (100, -70)

#North Curve Controls
NORTH_RIGHT_CTRL_1 = (-10, 50)
NORTH_RIGHT_CTRL_2 = (-10, -10)
NORTH_RIGHT_CTRL_3 = (-60, 10)
NORTH_RIGHT_CTRL_4 = (20, -10)
NORTH_RIGHT_CTRL_5 = (80, 100)
NORTH_RIGHT_CTRL_6 = (-10, 10)

#South Curve Controls
SOUTH_RIGHT_CTRL_1 = (30, 50)
SOUTH_RIGHT_CTRL_2 = (30, 100)
SOUTH_RIGHT_CTRL_3 = (-60, 10)
SOUTH_RIGHT_CTRL_4 = (-60, 50)
SOUTH_RIGHT_CTRL_5 = (110, -70)
SOUTH_RIGHT_CTRL_6 = (110, -10)

#WEST Curve Controls
WEST_RIGHT_CTRL_1 = (-10, 10)
WEST_RIGHT_CTRL_2 = (110, 10)
WEST_RIGHT_CTRL_3 = (80, 10)

#East Curve Controls
EAST_RIGHT_CTRL_1 = (-60, -70)
EAST_RIGHT_CTRL_2 = (20, -70)

sim.create_roads([
    (SOUTH_RIGHT_ORIGIN, I_SOUTH_RIGHT_CHK_1), # 0
    (I_SOUTH_RIGHT_CHK_1, SOUTH_RIGHT_CHK_2), # 1
    (SOUTH_RIGHT_CHK_2, SOUTH_RIGHT_CHK_3), # 2
    *curve_road(SOUTH_RIGHT_CHK_3, SOUTH_RIGHT_CHK_4, SOUTH_RIGHT_CTRL_1), # 3->17
    (SOUTH_RIGHT_CHK_4, SOUTH_RIGHT_CHK_5), # 18
    *curve_road(SOUTH_RIGHT_CHK_5, SOUTH_RIGHT_CHK_6, SOUTH_RIGHT_CTRL_2), # 19->33
    (SOUTH_RIGHT_CHK_6, SOUTH_RIGHT_CHK_7), #34
    *curve_road(I_SOUTH_RIGHT_CHK_1, I_NORTH_1_RIGHT_ORIGIN, NORTH_RIGHT_CTRL_1), # 35->49
    (I_NORTH_1_RIGHT_ORIGIN, NORTH_1_RIGHT_CHK_1), # 50
    (NORTH_1_RIGHT_CHK_1, I_NORTH_1_RIGHT_CHK_2), # 51
    (I_NORTH_1_RIGHT_CHK_2, NORTH_1_RIGHT_CHK_3), # 52
    *curve_road(NORTH_1_RIGHT_CHK_3, NORTH_1_RIGHT_CHK_4, NORTH_RIGHT_CTRL_2), # 53->67
    (NORTH_1_RIGHT_CHK_4, EAST_1_RIGHT_ORIGIN), # 68
    *curve_road(EAST_1_RIGHT_ORIGIN, NORTH_1_RIGHT_CHK_5, NORTH_RIGHT_CTRL_4), #69->83
    (NORTH_1_RIGHT_CHK_5, NORTH_1_RIGHT_CHK_6), # 84
    (NORTH_1_RIGHT_CHK_6, NORTH_1_RIGHT_CHK_7), # 85
    *curve_road(NORTH_1_RIGHT_CHK_7, EAST_2_RIGHT_CHK_1, EAST_RIGHT_CTRL_2), # 86->100
    (EAST_1_RIGHT_ORIGIN, I_EAST_1_RIGHT_CHK_1), # 101
    *curve_road(I_EAST_1_RIGHT_CHK_1, SOUTH_3_RIGHT_CHK_3, SOUTH_RIGHT_CTRL_6), # 102->116
    *curve_road(NORTH_1_RIGHT_CHK_1, I_WEST_1_RIGHT_ORIGIN, WEST_RIGHT_CTRL_1), # 117->131
    (I_WEST_1_RIGHT_ORIGIN, WEST_1_RIGHT_CHK_1), # 132
    *curve_road(WEST_1_RIGHT_CHK_1, NORTH_2_RIGHT_ORIGIN, NORTH_RIGHT_CTRL_3), # 133->147
    (NORTH_2_RIGHT_ORIGIN, NORTH_2_RIGHT_CHK_1), # 148
    (NORTH_2_RIGHT_CHK_1, NORTH_2_RIGHT_CHK_2), # 149
    *curve_road(NORTH_2_RIGHT_CHK_2, EAST_2_RIGHT_ORIGIN, EAST_RIGHT_CTRL_1), # 150->164
    (EAST_2_RIGHT_ORIGIN, EAST_2_RIGHT_CHK_2), # 165
    (EAST_2_RIGHT_CHK_2, EAST_2_RIGHT_CHK_1), # 166
    (EAST_2_RIGHT_CHK_1, EAST_2_RIGHT_CHK_3), # 167
    (EAST_2_RIGHT_CHK_3, EAST_2_RIGHT_CHK_4), # 168
    *curve_road(EAST_2_RIGHT_CHK_4, SOUTH_3_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_5), # 169->183
    (SOUTH_3_RIGHT_ORIGIN, SOUTH_3_RIGHT_CHK_1), # 184
    (SOUTH_3_RIGHT_CHK_1, SOUTH_3_RIGHT_CHK_3), # 185
    *curve_road(SOUTH_3_RIGHT_CHK_3, WEST_1_RIGHT_CHK_2, WEST_RIGHT_CTRL_2), # 186->200
    *curve_road(WEST_1_RIGHT_CHK_1, SOUTH_2_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_3), # 201->215
    (SOUTH_2_RIGHT_ORIGIN, SOUTH_2_RIGHT_CHK_1), # 216
    *curve_road(SOUTH_2_RIGHT_CHK_1, SOUTH_RIGHT_ORIGIN, SOUTH_RIGHT_CTRL_4), # 217->231
    *curve_road(SOUTH_RIGHT_CHK_7, NORTH_3_RIGHT_CHK_1, NORTH_RIGHT_CTRL_5), # 232->246
    (NORTH_3_RIGHT_CHK_1, NORTH_3_RIGHT_CHK_2), # 247
    (NORTH_3_RIGHT_CHK_2, NORTH_3_RIGHT_CHK_3), # 248
    *curve_road(SOUTH_RIGHT_CHK_7, NORTH_3_RIGHT_CHK_1, NORTH_RIGHT_CTRL_5), # 249->263
    (WEST_1_RIGHT_CHK_2, WEST_1_RIGHT_CHK_3), # 264
    (WEST_1_RIGHT_CHK_3, WEST_1_RIGHT_CHK_4), # 265
    (WEST_1_RIGHT_CHK_4, WEST_1_RIGHT_CHK_5), # 266
    *curve_road(WEST_1_RIGHT_CHK_5, NORTH_1_RIGHT_CHK_3, NORTH_RIGHT_CTRL_6), # 267->281
    *curve_road(NORTH_3_RIGHT_CHK_3, WEST_1_RIGHT_CHK_3, WEST_RIGHT_CTRL_3), # 282->296
    (WEST_1_RIGHT_CHK_5, I_WEST_1_RIGHT_ORIGIN), # 297

    *curve_road((30, 60), (40,70), (30, 70)), #Target 1 298->312
    *curve_road((-60, 20), (-50,30), (-60, 30)), #Target 2 313->327
    *curve_road((20, -30), (10,-40), (20, -40)), #Target 3 328->342
    *curve_road((-60, -40), (-50,-50), (-60, -50)), #Target 4 343->357
    *curve_road((70, -70), (80,-60), (80, -70)), #Target 5 358->372
    *curve_road((80, 40), (70,30), (80, 30)), #Target 6 373->387
    *curve_road((40, 10), (30, 0), (30, 10)), #Target 7 388->402
])

sim.create_gen({
    'vehicle_rate': 20,
    'vehicles': [
        [1, {"path": [0, 1, *road_class(2), *road_class(298)]}], # BottomLeft Objective 1
        [1, {"path": [0, *road_class(35), 50, *road_class(117), 132, *road_class(201), *road_class(313)]}], # BottomLeft Objective 2
        [1, {"path": [0, *road_class(35), 50, 51, 52, *road_class(53), 68, *road_class(69), 84, *road_class(328)]}], # Objective 3
        [1, {"path": [0, *road_class(35), 50, *road_class(117), 132, *road_class(133), 148, *road_class(343)]}], # Objective 4
        [1, {"path": [165, 166, 167, *road_class(358)]}], # TopLeft Objective 5 
    ]
})

sim.create_traffic_light([[50, 165, 184], [266, 85, 101]])

win = Window(sim)
win.run(steps_per_update=3)

