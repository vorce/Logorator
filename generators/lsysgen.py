import math
import logorator
import random
import pyglet.graphics, pyglet.image
from pyglet.gl import *
import lsys

# Unused for now, since we want to draw
# after constructing vertices instead.
def _lsys_forward_func(state):
    d = state.get("d", math.radians(90))
    s = state.get("s", 10)
    a = state.get("a")
    x = (state.get("x") + (s * math.cos(a)))
    y = (state.get("y") + (s * math.sin(a)))

    pyglet.graphics.draw(2, GL_LINES,
        ('v2f\static', (state.get("x"), state.get("y"), x, y)))

    return {"x":x,
            "y":y,
            "a":a,
            "s":s,
            "d":d}

class LSysGen(logorator.Generator):
    """
    """

    def __init__(self):
        self.seed = {}

        # List of different l-system configurations together with start state
        self.sys = [(lsys.LSys("F-B-B",
                              {"F":"F-B+F+B-F", "B":"BB"},
                              4),
                     {"x":0,#(self.seed["startx"]),
                      "y":0,#(self.seed["starty"]),
                      "a":0.0,
                      "s":5,
                      "d":math.radians(120)}),
                   (lsys.LSys("FX", {"X":"X+YF", "Y":"FX-Y"}, 10),
                    {"x":-15.0,
                     "y":20.0,
                     "a":0.0,
                     "s":1.8,
                     "d":math.radians(90)}),
                   (lsys.LSys("F", {"F":"B[+F]-F", "B":"BB"}, 7),
                   {"x":0,
                    "y":0,
                    "a":0.0,
                    "s":0.35,
                    "d":math.radians(45)}),
                   (lsys.LSys("X", {"X":"F-[[X]+X]+F[+FX]-X", "F":"FF"}, 6),
                   {"x":0,
                    "y":0,
                    "a":0.0,
                    "s":0.4,
                    "d":math.radians(25)}),
                   (lsys.LSys("F", {"F":"F[-F]F[+F][F]"}, 5),
                    {"x":0,
                     "y":0,
                     "a":0.0,
                     "s":1,
                     "d":math.radians(40)}),
                   (lsys.LSys("F", {"F":"FF-[-F+F+F]+[+F-F-F]"}, 4),
                    {"x":-15,
                     "y":0,
                     "a":0.0,
                     "s":1.75,
                     "d":math.radians(22.5)}),
                   (lsys.LSys("X", {"X":"F[+X][-X]FX", "F":"FF"}, 7),
                   {"x":-10,
                    "y":0,
                    "a":0.0,
                    "s":0.35,
                    "d":math.radians(25.7)}),
                    (lsys.LSys("X", {"X":"A+++ZFZF-FA-FAFA-ZF+",
                                     "Z":"-FA+++ZF+ZFZFFA-FA-A"}, 4),
                     {"x":0,
                     "y":0,
                     "a":0.0,
                     "s":5,
                     "d":math.radians(60)})
                   ]

        # Exposed parameters
        self.params = {'red': self.g_color_range(),
                       'green': self.g_color_range(),
                       'blue': self.g_color_range(),
                       'alpha': self.g_int_span(75, 150),
                       'startx': self.g_int_const(-40),
                       'starty': self.g_int_const(-30),
                       'thickness': self.g_int_span(8, 20),
                       'angle': self.g_int_range(359),
                       'model':self.g_int_range(len(self.sys)-1),
                       'koko':self.g_int_span(20, 50),
                       }

        # list of vertices for each entry in self.sys
        self.vs = [None] * len(self.sys)

    def mix(self, other):
        n = LSysGen()
        for i in self.seed:
            if i == '__generator__':
                continue
            n.seed[i] = random.gauss((self.seed[i] + other.seed[i]) / 2,
                                     abs((self.seed[i] - other.seed[i]) / 2))

        (ss, se) = self.sys[self.seed['model']]
        (os, oe) = other.sys[other.seed['model']]
        nc = {}
        for sc in ss.rules:
            nc[sc] = ss.rules[sc]
            for oc in os.rules:
                nc[oc] = os.rules[oc]
                if sc == oc:
                    nc[sc] = ss.rules[sc][: len(ss.rules) / 2] + os.rules[oc][len(os.rules) / 2 :]
                    
        niters = int(random.gauss((ss.iters + os.iters) / 2,
                                  abs((ss.iters - os.iters) / 2)))

        ne = {}
        for senv in se:
            for oenv in oe:
                if senv == oenv:
                    if senv == "s":
                        ne[senv] = {1:10, 2:5, 3:6, 4:3.74, 5:1, 6:0.4, 7:0.35,
                                    8:0.3, 9:0.2, 10:1.8}.get(niters)
                    else:
                        ne[senv] = (se[senv] + oe[oenv]) / 2

        nlsys = lsys.LSys(ss.axiom + os.axiom, nc, niters)
        n.sys.append((nlsys, ne))
        n.vs.append(None)
        n.seed['model'] = len(n.sys) - 1
        n.params['model'] = n.g_int_range(len(n.sys)-1)
        print("New LSys.\naxiom: {0}, rules: {1}, iterations: {2}\n environment: {3}".format(nlsys.axiom, nlsys.rules, nlsys.iters, ne))
        return n

    def render(self):
        if self.seed:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            glColor4ub(int(self.seed['red']), int(self.seed['green']),
                       int(self.seed['blue']), int(self.seed['alpha']))
           
            model = self.seed.get('model', 0)
            (ls, state) = self.sys[model]

            glRotatef(self.seed['angle'], 0.0, 0.0, 1.0)
            ls.parse(state, ls.commands)

            if self.vs[model] == None:
                self.vs[model] = pyglet.graphics.vertex_list(
                                    len(ls.verts)/2,
                                    ('v2f/static',
                                    ls.verts))
            self.vs[model].draw(GL_LINES)

