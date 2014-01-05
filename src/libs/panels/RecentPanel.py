import pygame
from pygame.locals import *
from libs.Utils import *
from libs.components.Label import *


class RecentPanel():
    RECENT_PLAYED=0
    RECENT_ADDED=1
    def __init__(self, app, parent, current_focus, next_focus):
        self.app = app
        self.parent = parent
        self.current_focus = current_focus
        self.next_focus = next_focus
        self.size = (calc_w(512), self.app.get_height());
        self.position = (calc_w(128), 0)
        self._init_background()
        self._init_scroll_panels()
    
    def _init_background(self):
        self.background = pygame.Surface(self.size)
    	self.background.convert()
    	self.background.fill(self.app.theme.recent_panel_b_colour2)
        
    def _init_scroll_panels(self):
        self._focus = RecentPanel.RECENT_PLAYED
        self.played = RecentScrollPanel(self.app, self, (calc_w(128), calc_h(140)), (self.size[0], calc_h(150)), "Recently Played")
        self.added = RecentScrollPanel(self.app, self, (calc_w(128), calc_h(300)), (self.size[0], calc_h(150)), "Recently Added")
    
    def focus(self):
        self.played.focus()
        self.added.unfocus()
        
    def unfocus(self):
        self.played.unfocus()
        self.added.unfocus()
       
    def change_focus(self):
        self.parent.set_focus(self.next_focus)
    
    def check_events(self, event):
        if event.type == KEYDOWN and event.key == K_UP:
            if (self._focus != RecentPanel.RECENT_PLAYED):
                self._focus = RecentPanel.RECENT_PLAYED
                self.added.unfocus()
                self.played.focus()
                self.app.update()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if (self._focus != RecentPanel.RECENT_ADDED):
                self._focus = RecentPanel.RECENT_ADDED
                self.played.unfocus()
                self.added.focus()
                self.app.update()
                
        if (self._focus==RecentPanel.RECENT_PLAYED):
            self.played.check_events(event)
        elif (self._focus==RecentPanel.RECENT_ADDED):
            self.added.check_events(event)
    
    def update(self):
        self.played.update()
        self.added.update()

    def draw(self, surface):
        surface.blit(self.background, self.position)
        self.played.draw(surface)
        self.added.draw(surface)
    
    def display_platform(self, platform):
        self._focus = RecentPanel.RECENT_PLAYED
        self.platform = platform
        self.db_played = self.app.db.find_recently_played_games_by_platform(self.platform, 0, 10)
        self.db_added = self.app.db.find_recently_added_games_by_platform(self.platform, 0, 10)
        self.played.display_platform(platform, self.db_played)
        self.added.display_platform(platform, self.db_added)
    
class RecentScrollPanel():
    def __init__(self, app, parent, position, size, text):
        self.app = app
        self.app.update_loading("[Main Screen - Recent Panel(%s)]" % text)
        self.parent = parent
        self.position = position
        self.size = size
        self.text = text
        self.selected = 0
        self.max = 0
        self._init_background()
        self._init_title()
        self._init_scroll()
    
    def _init_background(self):
        self.background = pygame.Surface((self.size[0], calc_h(20)))
        self.background.convert()
    	self.background.fill(self.app.theme.recent_panel_b_colour)
    
    def _init_title(self):
        self.label = Label(self.text, self.position, (self.size[0]-calc_w(5), calc_h(20)), calc_h(18), self.app.theme.recent_panel_f_colour, "RIGHT")
        self.label_sprites = pygame.sprite.RenderPlain((self.label))
    
    def _init_scroll(self):
        self.test_sprite = pygame.sprite.RenderPlain()
        self.scroll_item_size = (self.size[0] / 7, self.size[1]-calc_h(25))
        self.scroll_item_pos = (self.position[0] + calc_w(10), self.position[1]+calc_h(25))
        
    def display_platform(self, platform, data):
        self.platform = platform
        self.data = data
        self.selected = 0
        self.max = 0
        self.test_sprite.remove(self.test_sprite.sprites())
        self.scroll_items = ([])
        if (self.data):
            self.max = len(self.data)
            for x in range(0, self.max):
                w = 10
                pos = (self.scroll_item_pos[0] + ((self.scroll_item_size[0] + calc_w(w)) * x), self.scroll_item_pos[1])
                test = RecentScrollItem(self.app, self, pos, self.scroll_item_size, self.data[x])
                self.scroll_items.append(test)
                self.test_sprite.add(test)
                
    def focus(self):
        self.highlight_selected(True)
        
    def unfocus(self):
        self.highlight_selected(False)

    def highlight_selected(self, value=False):
        if (self.data):
            self.scroll_items[self.selected].selected(value)
            
    def left(self):
        self.highlight_selected(False)
        self.selected = self.selected - 1
    	if (self.selected < 0):
            self.selected = 0
            self.parent.change_focus()
        else:
            self.move_scroll_items(self.selected)
    
    def right(self):
        self.highlight_selected(False)
        self.selected = self.selected + 1
    	if (self.selected >= self.max):
            self.selected = self.max-1
        self.move_scroll_items(self.selected)

    def process_selected(self):
        print "GO GO GO GO"
    
    def move_scroll_items(self, value):
        self.highlight_selected(True)
        self.app.update()
    
    def check_events(self, event):
        if event.type == KEYDOWN and event.key == K_LEFT:
            self.left()
            return
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            self.right()
            return
        elif event.type == KEYDOWN and event.key == K_RETURN:
            return self.process_selected()
    
    def update(self):
        self.label_sprites.update()
        self.test_sprite.update()

    def draw(self, surface):
        surface.blit(self.background, self.position)
        self.label_sprites.draw(surface)
        self.test_sprite.draw(surface)

class RecentScrollItem(pygame.sprite.Sprite):
    def __init__(self, app, parent, position, size, data):
        pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.parent = parent
        self.start_position = position
        self.position = position
        self.size = size
        self.data = data
        self.margin=10
        self.shadow_margin=2
        self.image_size = (size[0]+calc_w(self.shadow_margin), size[1]+calc_h(self.shadow_margin))
        self.image = pygame.Surface(self.image_size, pygame.SRCALPHA)
        self._init_background()
        self._init_image()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.position)
        self._update()
    
    def _init_background(self):
        self.background_pos = (calc_w(self.margin/2), calc_h(self.margin/2));
        self.background = pygame.Surface(self.size, pygame.SRCALPHA)
    	self.background.convert()
    	self.background.fill(self.app.theme.recent_panel_b_colour)
        self.background_shadow_pos = (calc_w(self.shadow_margin), calc_h(self.shadow_margin))
        self.background_shadow = pygame.Surface(self.size, pygame.SRCALPHA)
    	self.background_shadow.convert()
    	self.background_shadow.fill((0,0,0,50))
        
    def _init_image(self):
        self.background_image_size = (self.size[0]-calc_w(self.margin), self.size[1]-calc_h(self.margin));
        self.background_image = pygame.Surface(self.background_image_size, pygame.SRCALPHA)
    	self.background_image.convert()
    	self.background_image.fill((100,100,100,0))
        self.actual_image = pygame.image.load("test.jpg")
        self.actual_image.convert_alpha()
        self.scaled_image = pygame.transform.scale(self.actual_image, self.background_image_size)
        self.background_image.blit(self.scaled_image, (0,0))
    
    def _update(self):
        self.background.blit(self.background_image, self.background_pos)
        self.image.blit(self.background_shadow, self.background_shadow_pos)        
        self.image.blit(self.background, (0,0))
        
    def selected(self, value):
        if (value):
            self.background.fill(self.app.theme.recent_panel_b_highlight_colour)
        else:
            self.background.fill(self.app.theme.recent_panel_b_colour)
        self._update()
        
        
