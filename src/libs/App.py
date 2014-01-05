import os
import pygame
from pygame.locals import *
from libs.components.SideBar import *
from libs.misc.configobj import ConfigObj
from libs.screens.MainScreen import *
from libs.themes.DefaultTheme import *
from libs.db.DB import *

class App():
    def __init__(self, config_file="config.ini"):
        self.draw = True
        self.config_file = config_file
        self._init_config()
        self._init_display()
        self._init_theme()
        self._init_background()
        self._init_db()
        self._init_screens()
        self._init_misc()
        self._run()
        
    def _init_config(self):
        pygame.init()        
        self.config = ConfigObj(self.config_file)
        self.overide_resolution = self.config["display"].as_bool("overide_resolution")
        if (self.overide_resolution):
            self.display_size = (self.config["display"].as_int("width"), int(self.config["display"].as_int("height")))
            self.display_depth = self.config["display"].as_int("depth")
            self.display_flags = 0
            if (self.config["display"].as_bool("fullscreen")):
                self.display_flags = (0 | pygame.FULLSCREEN) # | pygame.HWSURFACE)
        else:
            self.display_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            self.display_depth = 0
            self.display_flags = (0 | pygame.FULLSCREEN)
        
    def _init_display(self):
        self.display = pygame.display.set_mode(self.display_size, self.display_flags , self.display_depth)
        pygame.display.set_caption('AGM')
        pygame.mouse.set_visible(0)
    
    def _init_theme(self):
        self.theme = DefaultTheme()
    
    def _init_background(self):
        self.background = pygame.Surface(self.display_size)
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.update_loading("[INIT]")
    
    def update_loading(self, text):
        self.background.fill((0, 0, 0))
        self.background_font = pygame.font.Font(None, calc_h(25))
        self.background_text_render = self.background_font.render("...Loading...", 1, (255,255,255))
        self.background.blit(self.background_text_render, self.background_text_render.get_rect(centerx=self.background.get_width()/2, centery=self.background.get_height()/2))
        
        self.background_text_render2 = self.background_font.render(text, 1, (255,255,255))
        self.background.blit(self.background_text_render2, self.background_text_render2.get_rect(centerx=self.background.get_width()/2, centery=(self.background.get_height()/2)+calc_h(25) ))
        
        self.background_text_render3 = self.background_font.render("Awesome Games Menu", 1, (255,255,255))
        self.background.blit(self.background_text_render3, self.background_text_render3.get_rect(centerx=self.background.get_width()/2, y=10))
        
        
        self.display.blit(self.background, (0, 0))
        
        pygame.display.flip()
    
    def _init_db(self):
        self.db = DB(self)

    def _init_screens(self):
        self.main_screen = MainScreen(self)
        self.screen = self.main_screen
    
    def _init_misc(self):
        self.clock = pygame.time.Clock()
    
    def _run(self):
        self.running = "RUNNING"
        self.draw = True
        while (self.running == "RUNNING"):
            self.clock.tick(60)
            self._check_events()
            self._update_screen()
            self._draw_screen()
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = "QUIT"
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = "QUIT"
            else:
                if (self.screen):
                    self.screen.check_events(event)
    
    def _update_screen(self):
        self.screen.update()
            
    def update(self):
        self.draw = True
        
    def _draw_screen(self):
        if (self.draw):
            self.screen.draw(self.display)
            pygame.display.update()
            self.draw = False
    
    def get_width(self):
        return self.display_size[0]
    
    def get_height(self):
        return self.display_size[1]