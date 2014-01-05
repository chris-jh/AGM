import pygame
from pygame.locals import *
from libs.Utils import *
from libs.components.Label import *
from libs.panels.SidePanel import *
from libs.panels.RecentPanel import *

class MainScreen():
    SIDE_PANEL=0
    RECENT_PANEL=1
    def __init__(self, app):
        self.app = app
        self.app.update_loading("[Main Screen]")
        self.size = self.app.display_size;
        self.position = (0, 0)
        self._init_panels()
            
    def _init_panels(self):
        self.focus = MainScreen.SIDE_PANEL
        self.side_panel = SidePanel(self.app, self, MainScreen.SIDE_PANEL, MainScreen.RECENT_PANEL)
        self.recent_panel = RecentPanel(self.app, self, MainScreen.RECENT_PANEL, MainScreen.SIDE_PANEL)
        self.side_panel.update_selected()
    
    def get_recent_panel(self):
        return self.recent_panel
    
    def get_focus(self):
        return self.focus
    
    def set_focus(self, focus):
        self.focus = focus
        if (self.get_focus()==MainScreen.SIDE_PANEL):
            self.recent_panel.unfocus()
            self.side_panel.focus()
        elif (self.get_focus()==MainScreen.RECENT_PANEL):
            self.side_panel.unfocus()
            self.recent_panel.focus()
        self.app.update()
    
    def check_events(self, event):
        if (self.get_focus()==MainScreen.SIDE_PANEL):
            self.side_panel.check_events(event)
        elif (self.get_focus()==MainScreen.RECENT_PANEL):
            self.recent_panel.check_events(event)
    
    def update(self):
        self.side_panel.update()
        self.recent_panel.update()

    def draw(self, surface):
        self.recent_panel.draw(surface)
        self.side_panel.draw(surface)
