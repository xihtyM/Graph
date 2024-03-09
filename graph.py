from turtle import *

# trig functions
from math import e, pi, sin, cos, tan, sinh, cosh, tanh, erf, erfc
from math import asin as arcsin, acos as arccos, atan as arctan, atan2 as arctan2

# other functions
from math import cbrt, sqrt as _sqrt, ceil, floor, gcd, lcm, log10, log2, ulp
from scipy.special import gamma, factorial

# numbers
from math import e, pi


# user defined functions

def sqrt(x):
    if not x:
        return 0
    
    if type(x) is complex:
        if not x.imag:
            x = x.real
        elif not x.real:
            rt = (_sqrt(2)/2 + (i * _sqrt(2))/2) * _sqrt(x.imag)
            return (rt, -rt)
        else:
            rt = _sqrt( (abs(x) + x.real)/2 ) + \
                 (i * (x.imag/abs(x.imag)) * _sqrt( (abs(x) - x.real)/2 ))
            return (rt, -rt)
    
    if x < 0:
        rt = _sqrt(abs(x))
        return (i * rt, i * -rt)

    rt = _sqrt(x)
    return (rt, -rt)


from time import sleep
from random import choice
from typing import Callable
from dataclasses import dataclass, field

HEIGHT = 840
WIDTH = 1140

MULTIPLIER = 2500
AXIS_DISTANCE = 30

i = 1j
undefined = None
inf = float("inf")

REAL = "1"
IMAGINARY = "2"

colors = [
    (44, 44, 44),
    (120, 220, 46),
    (184, 207, 20),
    (252, 108, 120),
    (108, 252, 120),
    (120, 230, 208),
    (48, 96, 201),
    (202, 6, 242),
]


@dataclass(frozen=True)
class Position():
    x: float = 0.0
    y: float = 0.0

@dataclass
class Func():
    f: Callable
    _range: tuple[int, int]
    zeros: list
    
    peak: Position = Position(0, -inf)
    min: Position = Position(0, inf)

functions: dict[Func] = {}

uid = 0

def unique_id():
    global uid
    uid += 1
    return uid - 1

t = Turtle()

# use for drawing anything other than the graph (mainly the axis)
axis = Turtle()

s = Screen()
s.setup(WIDTH, HEIGHT)

zoom = 1.

world_coords = (-WIDTH/2, -HEIGHT/2, WIDTH/2, HEIGHT/2)

s.setworldcoordinates(*world_coords)
s.colormode(255)

c = s.getcanvas()

t.ht()
t._tracer(0)

axis.ht()
axis._tracer(0)

N = max(HEIGHT, WIDTH) # draws enough to fit on screen

def label_x_axis():
    dist = AXIS_DISTANCE

    if zoom >= 8.:
        dist *= round(int(zoom * 1.25), -1)
    elif zoom >= 6.:
        dist *= 8
    elif zoom >= 3.5:
        dist *= 5
    elif zoom >= 1.5:
        dist *= 2
    elif zoom <= 0.03:
        dist = 1
    elif zoom <= 0.05:
        dist //= 15
    elif zoom <= 0.1:
        dist //= 10
    elif zoom <= 0.25:
        dist //= 6
    elif zoom <= 0.5:
        dist //= 2
    
    start_point = -(N // dist) * dist

    for x in range(start_point, -start_point, dist):
        if not x:
            continue
        
        axis.penup()
        axis.goto(x - len(str(x)) * zoom, -20 * zoom)

        x_val = x/AXIS_DISTANCE

        if x_val == int(x_val):
            axis.write("%d" % int(x_val))
        else:
            axis.write("%.2f" % x_val)

        axis.goto(x, -5 * zoom)
        axis.pendown()
        axis.goto(x, 0)

def label_y_axis():
    dist = AXIS_DISTANCE

    if zoom >= 8.:
        dist *= round(int(zoom * 1.25), -1)
    elif zoom >= 6.:
        dist *= 8
    elif zoom >= 3.5:
        dist *= 5
    elif zoom >= 1.5:
        dist *= 2
    elif zoom <= 0.03:
        dist = 1
    elif zoom <= 0.05:
        dist //= 15
    elif zoom <= 0.1:
        dist //= 10
    elif zoom <= 0.25:
        dist //= 6
    elif zoom <= 0.5:
        dist //= 2
    
    start_point = -(N // dist) * dist

    for y in range(start_point, -start_point, dist):
        if not y:
            continue
        
        axis.penup()

        axis.goto(-15 * zoom, y - len(str(y)) * zoom)
        y_val = y/AXIS_DISTANCE

        if y_val == int(y_val):
            axis.write("%d" % int(y_val))
        else:
            axis.write("%.2f" % y_val)
        
        axis.goto(-5 * zoom, y)
        axis.pendown()
        axis.goto(0, y)

def start():
    # reset board
    axis.clear()
    
    # draw axis
    axis.penup()
    axis.goto(-N, 0)
    axis.pendown()
    axis.goto(N, 0)

    axis.penup()
    axis.goto(0, N)
    axis.pendown()
    axis.goto(0, -N)

    label_x_axis()
    label_y_axis()

    axis._update()
    

def plot(f: Callable, _range: tuple = (-20, 20)):
    t.pencolor(colors[int(input("Color: "))])
    t.penup()
    
    range_multiplier = MULTIPLIER//(1 + (_range[1] - _range[0])//100)

    func_id = unique_id()
    functions[func_id] = Func(f, _range, [])

    all_results = []
    start = []
    is_penup = False
    
    for x in range(_range[0] * range_multiplier, _range[1] * range_multiplier):
        try:
            res = f(x/range_multiplier)
        except Exception:
            res = undefined

        if type(res) is not tuple:
            res = (res, )

        for i, v in enumerate(res):
            try:
                if type(v) is complex:
                    v = undefined
                all_results[i].append(v)
            except IndexError:
                start.append(x)
                all_results.append([v])

    for i, results in enumerate(all_results):
        x = start[i]

        try:
            res = results.pop(0)
            while res is undefined:
                x += 1
                res = results.pop(0)
        except IndexError:
            continue

        t.goto(x * AXIS_DISTANCE/range_multiplier, res * AXIS_DISTANCE)

        if not res:
            functions[func_id].zeros.append(Position(x/range_multiplier, res))

        if res > functions[func_id].peak.y:
            functions[func_id].peak = Position(x/range_multiplier, res)
        elif res < functions[func_id].min.y:
            functions[func_id].min = Position(x/range_multiplier, res)
        
        t.pendown()

        for res in results:
            x += 1
            if res is undefined:
                t.penup()
                is_penup = True
                continue

            t.goto(x * AXIS_DISTANCE/range_multiplier, res * AXIS_DISTANCE)

            if not res:
                functions[func_id].zeros.append(Position(x/range_multiplier, res))

            if res > functions[func_id].peak.y:
                functions[func_id].peak = Position(x/range_multiplier, res)
            elif res < functions[func_id].min.y:
                functions[func_id].min = Position(x/range_multiplier, res)

            if is_penup:
                is_penup = False
                t.pendown()

        t.penup()
        t._update()
        
    t._update()

def iplot(f: Callable, _range: tuple = (-20, 20)):
    t.pencolor(colors[int(input("Color: "))])
    t.penup()
    
    range_multiplier = MULTIPLIER//(1 + (_range[0] + _range[1])//100)

    func_id = unique_id()
    functions[func_id] = Func(f, _range, [])

    all_results = []
    start = []
    is_penup = False
    
    for x in range(_range[0] * range_multiplier, _range[1] * range_multiplier):
        try:
            res = f(x/range_multiplier)
        except Exception:
            res = undefined

        if type(res) is not tuple:
            res = (res, )

        for i, v in enumerate(res):
            try:
                if type(v) is not complex and v is not undefined:
                    v = complex(v, 0)
                all_results[i].append(v)
            except IndexError:
                start.append(x)
                all_results.append([v])

    for i, results in enumerate(all_results):
        x = start[i]

        try:
            res = results.pop(0)
            while res is undefined:
                x += 1
                res = results.pop(0)
        except IndexError:
            continue

        t.goto(res.real * AXIS_DISTANCE, res.imag * AXIS_DISTANCE)

        if not res.imag:
            functions[func_id].zeros.append(Position(res.real, res.imag))

        if res.imag > functions[func_id].peak.y:
            functions[func_id].peak = Position(res.real, res.imag)
        elif res.imag < functions[func_id].min.y:
            functions[func_id].min = Position(res.real, res.imag)
        
        t.pendown()

        for res in results:
            x += 1
            if res is undefined:
                t.penup()
                is_penup = True
                continue

            t.goto(res.real * AXIS_DISTANCE, res.imag * AXIS_DISTANCE)

            if not res:
                functions[func_id].zeros.append(Position(res.real, res.imag))

            if res.imag > functions[func_id].peak.y:
                functions[func_id].peak = Position(res.real, res.imag)
            elif res.imag < functions[func_id].min.y:
                functions[func_id].min = Position(res.real, res.imag)

            if is_penup:
                is_penup = False
                t.pendown()
        
        t.penup()
        t._update()
    
    t._update()

def get_function(_range: tuple):
    print("Pick a plane:")
    print("Real number (1)")
    print("Imaginary (2)")
    plane = input()

    if plane not in (REAL, IMAGINARY):
        print("Type either a 1 or a 2 it isn't hard when you try...")
        return

    inp_f = input("y = ")

    if plane == REAL:
        plot_function = plot
    elif plane == IMAGINARY:
        plot_function = iplot
    
    plot_function(lambda x: eval(inp_f, {'x': x, 'i': i, 'e': e, 'pi': pi, 'sin': sin, 'cos': cos, 'tan': tan,
                    'sinh': sinh, 'cosh': cosh, 'tanh': tanh, 'erf': erf,
                    'erfc': erfc, 'asin': arcsin, 'acos': arccos, 'atan': arctan,
                    'atan2': arctan2, 'cbrt': cbrt, 'sqrt': sqrt, 'ceil': ceil,
                    'floor': floor, 'gcd': gcd, 'lcm': lcm, 'log10': log10,
                    'log2': log2, 'ulp': ulp, 'gamma': gamma, 'factorial': factorial}), _range)
    
    func = functions[uid - 1]

    print("f(x) = %s Stats:\n" % inp_f)
    print("     Min: (%f, %f)" % (func.min.x, func.min.y))
    print("     Max: (%f, %f)" % (func.peak.x, func.peak.y))
    print("     Zeros: " + ", ".join(["(%f, %f)" % (zero.x, zero.y) for zero in func.zeros]) + "\n")

# TODO: fix pls
def handle_click(x, y):
    global world_coords

    x_dist = (world_coords[2] - world_coords[0])/2
    y_dist = (world_coords[3] - world_coords[1])/2

    mid_x = world_coords[0] + x_dist
    mid_y = world_coords[1] + y_dist

    relative_x = mid_x - x
    relative_y = mid_y - y

    world_coords = (relative_x - x_dist, relative_y - y_dist, relative_x + x_dist, relative_y + y_dist)
    s.setworldcoordinates(zoom * world_coords[0], zoom * world_coords[1], zoom * world_coords[2], zoom * world_coords[3])

def category(zoom_value):
    if zoom_value >= 8.:
        return zoom_value//10
    elif zoom_value >= 6.:
        return 2
    elif zoom_value >= 3.5:
        return 3
    elif zoom_value >= 1.5:
        return 4
    elif zoom_value <= 0.03:
        return 9
    elif zoom_value <= 0.05:
        return 8
    elif zoom_value <= 0.1:
        return 7
    elif zoom_value <= 0.25:
        return 6
    elif zoom_value <= 0.5:
        return 5

def handle_scroll(y):
    global world_coords, flat_world_coords, zoom, N

    old_zoom = zoom
    zoom -= (y.delta * (zoom/4)/(AXIS_DISTANCE * 25))

    if zoom < 0.03:
        zoom = 0.03
    elif zoom > 5000:
        zoom = 5000.

    s.setworldcoordinates(zoom * world_coords[0], zoom * world_coords[1], zoom * world_coords[2], zoom * world_coords[3])
    if category(old_zoom) != category(zoom):
        start()
    
    N = int(max(HEIGHT, WIDTH) * zoom) # draws enough to fit on screen

def main():
    #s.onscreenclick(handle_click, btn=1, add=True)
    s.getcanvas().bind("<MouseWheel>", handle_scroll)
    s.getcanvas().bind("r", start)
    start()

    while True:
        get_function((-500, 500))

if __name__ == "__main__":
    main()
    input()
