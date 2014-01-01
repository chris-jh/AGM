import pygame
from pygame.locals import *
from libs.Utils import *
from libs.components.Label import *
from libs.panels.SidePanel import *
from libs.panels.RecentPanel import *

class MainScreen():
    def __init__(self, app):
        self.app = app
        self.app.update_loading("[Main Screen]")
        self.size = self.app.display_size;
        self.position = (0, 0)
        self._init_panels()
            
    def _init_panels(self):
        self.side_panel = SidePanel(self.app, self)
        self.recent_panel = RecentPanel(self.app, self)
    
    def check_events(self, event):
        self.recent_panel.check_events(event)
        self.side_panel.check_events(event)
    
    def update(self):
        self.recent_panel.update()
        self.side_panel.update()

    def draw(self, surface):
        self.recent_panel.draw(surface)
        self.side_panel.draw(surface)