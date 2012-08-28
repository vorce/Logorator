import datetime
import time
import pyglet
from pyglet.gl import *
from PIL import Image

class Eventhandler:
  def __init__(self, surface):
    self.surface = surface

    self.MOUSE_BUTTON_LEFT = 1
    self.MOUSE_BUTTON_RIGHT = 3
    self.MOUSE_BUTTON_MIDDLE = 2

    self.clickDownPos = None
    self.clickButton = None
    self.nclicks = 0
    self.paused = False
    self.next_seeds = False
    self.multi_view = True
    self.selected_view = None
    self.click_coord = (None, None)

    # Pyglet
    @self.surface.event
    def on_key_release(symbol, mod):
        if symbol == pyglet.window.key.SPACE:
	        self.handleSpacePress()
        elif symbol == pyglet.window.key.S:
	        self.handleSPress()
        elif symbol == pyglet.window.key.RIGHT:
            self.handleRightArrow()


    # Pyglet
    @self.surface.event
    def on_mouse_release(x, y, button, mod):
        self.click_coord = (x, y)

        if button == pyglet.window.mouse.LEFT:
	        self.handleLeftClickUp(None)
        elif button == pyglet.window.mouse.RIGHT:
	        self.handleRightClickUp(None)

  # A bit special, since we have to use PIL for this.
  # Pyglet refuses to not use alpha value on background.
  def saveScreenshot(self, filename):
    print("Saving screenshot: {0}".format(filename))
    mgr = pyglet.image.get_buffer_manager()
    color_buffer = mgr.get_color_buffer()
    image = color_buffer.image_data.get_image_data()
    pil_image = Image.fromstring(image.format, (image.width, image.height), image.get_data(image.format, image.pitch))
    pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
    pil_image = pil_image.convert('RGB')
    pil_image.save(filename, "PNG")

  def handleMouseMotion(self, pos):
    pass

  def handleLeftClickDown(self, event):
    pass

  def handleLeftClickUp(self, event):
      self.multi_view = not self.multi_view
      print("Multi view: " + str(self.multi_view))

  def handleRightClickDown(self, event):
    pass

  def handleRightClickUp(self, event):
    pass

  def handleMiddleClickDown(self, event):
    pass

  def handleMiddleClickUp(self, event):
    pass

  def handleSPress(self):
    now = datetime.datetime.now()
    filename = "{0}_{1}-{2}-{3}_{4}.{5}.{6}".format("logorator", now.year, now.month, now.day, now.hour, now.minute, now.second)
    self.saveScreenshot("screenshots/{0}.png".format(filename))

  def handleRightArrow(self):
      self.next_seeds = True

  def handleSpacePress(self):
      self.paused = not self.paused
      print("Paused: " + str(self.paused))

