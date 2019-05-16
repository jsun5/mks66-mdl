import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    #Thank you Larry for helping me with the code!

    for command in commands:
        cmd=command['op']
        args=command['args']
        if cmd == 'line':
            add_edge( coords,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult(stack[-1], coords)
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif cmd == 'sphere':
            reflect = args[0]
            add_sphere(coords1,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], coords1)
            if command['constants'] is not None:
                reflect = command['constants']
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []  
        elif cmd == 'torus':
            add_torus(coords1,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            if command['constants'] is not None:
                reflect = command['constants']
            matrix_mult(stack[-1], coords1)
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []
        elif cmd == 'box':
            add_box(coords1,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            if command['constants'] is not None:
                reflect = command['constants']
            matrix_mult(stack[-1], coords1)
            draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, reflect)
            coords1 = []
        elif cmd == 'circle':
            add_circle(coords,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult(stack[-1], coords)
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif cmd == 'hermite' or cmd == 'bezier':
            add_curve(coords,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step_3d, cmd)
            matrix_mult(stack[-1], coords)
            draw_lines(coords, screen, zbuffer, color)
            coords = []
        elif cmd == 'move':
            m = make_translate(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], m )
            stack[-1] = [ i[:] for i in m]
        elif cmd == 'scale':
            s = make_scale(float(args[0]), float(args[1]), float(args[2]))
            matrix_mult( stack[-1], s )
            stack[-1] = [ i[:] for i in s]
        elif cmd == 'rotate':
            theta = float(args[1]) * (math.pi / 180)
			
            if args[0] == 'x':
                r = make_rotX(theta)
            elif args[0] == 'y':
                r = make_rotY(theta)
            else:
                r = make_rotZ(theta)
            matrix_mult( stack[-1], r )
            stack[-1] = [ i[:] for i in r]
        elif cmd == 'clear':
            tmp = []
        elif cmd == 'push':
            stack.append( [ i[:] for i in stack[-1]])
        elif cmd == 'pop':
            stack.pop()
        elif cmd == 'display' or cmd == 'save':
            if cmd == 'display':
                display(screen)
            else:
                save_extension(screen, args[0]+'.png')

    else:
        print "Parsing failed."
        return
            