import os, pygame
from pygame.locals import *

default_width = 640
default_height = 480

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

def round(float_value):
	v1 = int(float_value)
	if (float_value > float(v1)):
		return v1+1
	else:
		return v1

def get_pixel_ratio_w():
	screen = pygame.display.get_surface()
	return float(screen.get_width()) / float(default_width)
	
def get_pixel_ratio_h():
	screen = pygame.display.get_surface()
	return float(screen.get_height()) / float(default_height)
    
def calc_w(pixel):
    return round(pixel * get_pixel_ratio_w())

def calc_h(pixel):
    return round(pixel * get_pixel_ratio_h())