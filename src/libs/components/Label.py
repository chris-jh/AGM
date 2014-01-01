import pygame
from pygame.locals import *
from libs.Utils import *

class Label(pygame.sprite.Sprite):	
    def __init__(self, text, position, size, font_size=12, colour=(10,10,10), alignment=None):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.size = size
        self.font_size = font_size
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.colour = colour
        self.alignment = alignment
        self.position = position		
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(position)
        self.font = pygame.font.Font(None, self.font_size)
        self.text_render = self.font.render(self.text, 1, self.colour)
        if (self.alignment == "CENTER"):
            self.image.blit(self.text_render, self.text_render.get_rect(centerx=self.image.get_width()/2, centery=self.image.get_height()/2))
        elif (self.alignment == "RIGHT"):
            self.image.blit(self.text_render, self.text_render.get_rect(right=self.image.get_width(), centery=self.image.get_height()/2))
        else:
            self.image.blit(self.text_render, (0,0))

    def update(self):
        self.tmp = ""