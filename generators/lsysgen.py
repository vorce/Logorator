import math
import random
import pyglet.graphics, pyglet.image
from pyglet.gl import *

import generator
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

class LSysGen(generator.Generator):
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
                       'startx': self.g_constant(-40),
                       'starty': self.g_constant(-30),
                       'thickness': self.g_int_span(8, 20),
                       'angle': self.g_int_range(359),
                       'model':self.g_int_range(len(self.sys)-1),
                       }

        # list of vertices for each entry in self.sys
        self.vertices = [None] * len(self.sys)

    # TODO clean me up V - V
    @classmethod
    def mix_of(cls, lsys1, lsys2):
        new_lsysgen = cls()
        for i in lsys1.seed:
            if i == '__generator__':
                continue
            new_lsysgen.seed[i] = random.gauss((lsys1.seed[i] + lsys2.seed[i]) / 2,
                                     abs((lsys1.seed[i] - lsys2.seed[i]) / 2))

        (ss, se) = lsys1.sys[lsys1.seed.get('model', 0)]
        (os, oe) = lsys2.sys[lsys2.seed.get('model', 0)]
        nc = {}
        for sc in ss.rules:
            nc[sc] = ss.rules[sc]
            for oc in os.rules:
                nc[oc] = os.rules[oc]
                if sc == oc:
                    nc[sc] = ss.rules[sc][:(len(ss.rules) / 2)] + os.rules[oc][(len(os.rules) / 2) :]
                    
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
        new_lsysgen.sys.append((nlsys, ne))
        new_lsysgen.vertices.append(None)
        new_lsysgen.seed['model'] = len(new_lsysgen.sys) - 1
        new_lsysgen.params['model'] = new_lsysgen.g_int_range(len(new_lsysgen.sys)-1)
        print("New LSys.\naxiom: {0}, rules: {1}, iterations: {2}\new_lsysgen environment: {3}".format(
              nlsys.axiom, nlsys.rules, nlsys.iters, ne))
        return new_lsysgen


    def get_current_lsystem_vertices(self, model):
        (lsystem, state) = self.sys[model]
        lsystem.parse(state, lsystem.commands)
        return lsystem.verts


    def render(self):
        if self.seed:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            glColor4ub(int(self.seed['red']), int(self.seed['green']),
                       int(self.seed['blue']), int(self.seed['alpha']))

            glRotatef(self.seed['angle'], 0.0, 0.0, 1.0)
            
            model = self.seed.get('model', 0)
            
            if self.vertices[model] == None:
                lsys_verts = self.get_current_lsystem_vertices(model)
                self.vertices[model] = pyglet.graphics.vertex_list(
                                    len(lsys_verts) / 2,
                                    ('v2f/static', lsys_verts))
            self.vertices[model].draw(GL_LINES)

