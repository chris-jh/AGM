import os, pygame
from pygame.locals import *

default_width = 640
default_height = 480

def check_file_exists(file):
    return os.path.exists(file)

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

def adjust_c(colour, value):
    c = (255,255,255,255)
    if ((colour[0]+value) > 255):
        c = (255, c[1], c[2], c[3])
    elif ((colour[0]+value) < 0):
        c = (0, c[1], c[2], c[3])    
    else:
        c = (colour[0]+value, c[1], c[2], c[3])
    
    if ((colour[1]+value) > 255):
        c = (c[0], 255, c[2], c[3])
    elif ((colour[1]+value) < 0):
        c = (c[0], 0, c[2], c[3])    
    else:
        c = (c[0], colour[1]+value, c[2], c[3])
    
    if ((colour[2]+value) > 255):
        c = (c[0], c[1], 255, c[3])
    elif ((colour[2]+value) < 0):
        c = (c[0], c[1], 0, c[3])   
    else:
        c = (c[0], c[1], colour[2]+value, c[3])
    
    c = (c[0], c[1], c[2], colour[3])
    return c
