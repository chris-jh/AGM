import pygame
from pygame.locals import *
from libs.Utils import *
from libs.misc import gradients
from libs.components.Label import *
from libs.components.Menu import *


class SidePanel():
    def __init__(self, app, parent):
        self.app = app
        self.app.update_loading("[Main Screen - Side Panel]")
        self.parent = parent
        self.size = (calc_w(128), self.app.get_height());
        self.title1_text = "Awesome Games"
        self.title2_text = "Menu"
        self._init_background()
        self._init_title()
        self._init_menu()
    
    def _init_background(self):
        self.background = pygame.Surface(self.size)
    	self.background.convert()
    	self.background.fill(self.app.theme.side_panel_b_colour)
        self.background_fade = gradients.horizontal((calc_w(5), self.size[1]), self.app.theme.side_oanel_b_fade_in_colour, self.app.theme.side_oanel_b_fade_out_colour)
    
    def _init_title(self):
        self.title1 = Label(self.title1_text, (0, calc_h(5)), (self.size[0], calc_h(21)), calc_h(21), self.app.theme.side_panel_f_colour, "CENTER")
    	self.title2 = Label(self.title2_text, (0, calc_h(20)), (self.size[0], calc_h(21)), calc_h(21), self.app.theme.side_panel_f_colour, "CENTER")
        self.title_sprites = pygame.sprite.RenderPlain((self.title1, self.title2))
    
    def _init_menu(self):
        names = ([])
        num_emus = self.app.config["emulators"].as_int("number")
        for x in range(1, num_emus+1):
            names.append(self.app.config["emulator%s" % x]["name"])
        names.append("Quit")
        self.menu = Menu(self.app, self, (calc_w(5), calc_h(80)), (calc_w(118), calc_h(20)), names, self.app.theme.side_panel_menu_f_colour, self.app.theme.side_panel_menu_selector_colour)
    
    def check_events(self, event):
        self.menu.check_events(event)
    
    def update(self):
        self.title_sprites.update()
        self.menu.update()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.background_fade, (self.background.get_width(), 0))
        
        self.title_sprites.draw(surface)
        
        self.menu.draw(surface)
    
    
        
        
