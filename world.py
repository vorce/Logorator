from pyglet.gl import *

import sys

sys.path.insert(0, 'generators')
import polygen
import textgen
import lsysgen

from logo import Logo

class LogoView():
    """
    A view for a logo, takes care of rendering
    """
    def __init__(self, position, dimensions, logo = None):
        self.position = position
        self.logo = logo
        self.width, self.height = dimensions

    def _setup_view(self, width, height, coords):
        (x, y) = coords
        glViewport(x, y, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        zoom = 50.0
        width_ratio = width / height
        gluOrtho2D(-zoom * width_ratio,
                   zoom * width_ratio,
                   -zoom,
                   zoom)

        glPushAttrib(GL_ENABLE_BIT | GL_SCISSOR_BIT)
        glEnable(GL_SCISSOR_TEST)
        glScissor(x, y, width, height)

    def render(self, multi_view = True):
        if multi_view:
            self._setup_view(self.width, self.height, self.position)

        for generator in self.logo: 
            generator.render()

        if multi_view:
            glPopAttrib()

class World(object):
    def __init__(self, win, seeds):
        self.paused = False
        self.multi_logoview = True
        self.win = win
        
        self.single_logoview = None

        width = win.width / 3
        height = win.height / 3

        self.logoviews = [LogoView((0, int(win.height/1.5)), (width, height),
                              Logo([textgen.TextGen()])),
                      LogoView((width, int(win.height/1.5)), (width, height),
                              Logo([lsysgen.LSysGen(), polygen.PolyGen(),
                               polygen.PolyGen(), polygen.PolyGen()])),
                      LogoView((int(win.width/1.5), int(win.height/1.5)), (width, height),
                              Logo([polygen.PolyGen(), polygen.PolyGen(),
                               lsysgen.LSysGen()])),

                      LogoView((0, height), (width, height),
                              Logo([polygen.PolyGen()])),
                      LogoView((width, height), (width, height),
                              Logo([lsysgen.LSysGen(), lsysgen.LSysGen()])),
                      LogoView((int(win.width/1.5), height), (width, height),
                              Logo([polygen.PolyGen()])),

                      LogoView((0, 0), (width, height),
                              Logo([lsysgen.LSysGen()])),
                      LogoView((width, 0), (width, height),
                              Logo([polygen.PolyGen()])),
                      LogoView((int(win.width/1.5), 0), (width, height),
                              Logo())
                    ]

        if seeds == None:
            self.create_seeds_for_all_generators(0)

            # Mix the second and third logo to form a new one, and place it
            # in the lower right position.
            logo = Logo.mix_of(self.logoviews[1].logo, self.logoviews[2].logo)
            mixed_view = LogoView((int(win.width/1.5), 0),
                                  (width, height), logo)

            self.logoviews[8] = mixed_view
        else:
            newgens = []
            for seed in seeds:
                (module, generator) = seed.get('__generator__',
                                               ('polygen', 'PolyGen'))
                genclass = reduce(getattr, [generator], sys.modules[module])
                gen = genclass()
                gen.seed = seed
                newgens.append(gen)

            for view in self.logoviews:
                view.logo = Logo(newgens)

            print(self.logoviews)

        pyglet.clock.schedule_interval(self.create_seeds_for_all_generators, 10)

    def create_seed(self, generator):
        new_seed = {'__generator__': (generator.__module__, generator.__class__.__name__)}
        for param in generator.params:
            new_seed[param] = generator.params[param].next()
        generator.seed = new_seed
        

    def create_seeds_for_all_generators(self, timer):
        for view in self.logoviews:
            for generator in view.logo:
                self.create_seed(generator)
                print("seed: {0}".format(generator.dump()))
        print("-------------------")

    def tick(self, events):
        if not self.paused and events.paused:
            pyglet.clock.unschedule(self.create_seeds_for_all_generators)
        elif self.paused and not events.paused:
            pyglet.clock.schedule_interval(self.create_seeds_for_all_generators, 10)

        self.paused = events.paused
        self.multi_logoview = events.multi_logoview

        if events.next_seeds:
            self.create_seeds_for_all_generators(None)
            events.next_seeds = False

        if events.click_coord and not self.multi_logoview:
            self.single_logoview = self.__get_logo_view(events.click_coord)

    def __get_logo_view(self, coords):
        (x, y) = coords
        
        if x < int(self.win.width/3):
            if y < int(self.win.height/3):
                return self.logoviews[6]
            elif y < int(self.win.height/1.5):
                return self.logoviews[3]
            else:
                return self.logoviews[0]
        elif x < int(self.win.width/1.5):
            if y < int(self.win.height/3):
                return self.logoviews[7]
            elif y < int(self.win.height/1.5):
                return self.logoviews[4]
            else:
                return self.logoviews[1]
        else:
            if y < int(self.win.height/3):
                return self.logoviews[8]
            elif y < int(self.win.height/1.5):
                return self.logoviews[5]
            else:
                return self.logoviews[2]


    def draw(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT)

        if self.multi_logoview:
            for v in self.logoviews:
                v.render(True)
            glDisable(GL_SCISSOR_TEST)

        elif self.single_logoview:
            self.single_logoview.render(False)
        
