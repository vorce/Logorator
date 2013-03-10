import datetime
import time
from pyglet.gl import *
#from PIL import Image


class Eventhandler:
    def __init__(self, surface):
        self.surface = surface

        self.MOUSE_BUTTON_LEFT = 1
        self.MOUSE_BUTTON_RIGHT = 3
        self.MOUSE_BUTTON_MIDDLE = 2

        self.click_down_position = None
        self.click_button = None
        self.nclicks = 0
        self.paused = False
        self.next_seeds = False
        self.multi_logoview = True
        self.selected_view = None
        self.click_coord = None


        # Pyglet
        @self.surface.event
        def on_key_release(symbol, mod):
            if symbol == pyglet.window.key.SPACE:
                self.handle_space_press()
            elif symbol == pyglet.window.key.S:
                self.handle_s_press()
            elif symbol == pyglet.window.key.RIGHT:
                self.handle_right_arrow_press()


        # Pyglet
        @self.surface.event
        def on_mouse_release(x, y, button, mod):
            self.click_coord = (x, y)

            if button == pyglet.window.mouse.LEFT:
                self.handle_left_click_up(None)
            elif button == pyglet.window.mouse.RIGHT:
                self.handle_right_click_up(None)


    # A bit special, since we have to use PIL for this.
    # Pyglet refuses to not use alpha value on background.
    def save_screenshot(self, filename):
        print("Saving screenshot: {0}".format(filename))
        mgr = pyglet.image.get_buffer_manager()
        color_buffer = mgr.get_color_buffer()
        image = color_buffer.image_data.get_image_data()
        #pil_image = Image.fromstring(image.format, (image.width, image.height), image.get_data(image.format, image.pitch))
        #pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
        #pil_image = pil_image.convert('RGB')
        #pil_image.save(filename, "PNG")


    def handle_left_click_up(self, event):
        self.multi_logoview = not self.multi_logoview
        # print("Multi view: " + str(self.multi_logoview))


    def handle_s_press(self):
        now = datetime.datetime.now()
        filename = "{0}_{1}-{2}-{3}_{4}.{5}.{6}".format("logorator",
                    now.year, now.month, now.day, now.hour,
                    now.minute, now.second)
        self.save_screenshot("screenshots/{0}.png".format(filename))


    def handle_right_arrow_press(self):
        self.next_seeds = True


    def handle_space_press(self):
        self.paused = not self.paused
        print("Paused: " + str(self.paused))

