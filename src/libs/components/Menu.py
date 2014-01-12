import pygame
from pygame.locals import *
from libs.Utils import *
from libs.misc import gradients
from libs.components.Label import *


class Menu():
    def __init__(self, app, parent, position, size, list, colour=(0,0,0), selector_colour=(255,255,255,255), main_back_colour=None):
        self.app = app
        self.parent = parent
        self.position = position
        self.size = size
        self.list = list
        self.colour = colour
        self.selector_colour = selector_colour
        self.main_back_colour = main_back_colour
        self.selected = 0
        self._init_list()
        self._init_selector()
    
    def _init_list(self):
        self.item_sprites = pygame.sprite.RenderPlain()
    	s = 0
    	for x in self.list:
            label_item = Label(x, (self.position[0], self._calc_menu_y(s)), self.size, calc_h(18), self.colour, "CENTER")
            self.item_sprites.add(label_item)
            s += 1
    
    def _calc_menu_y(self, index):
    	return (self.position[1] + (self.size[1] * index))
    
    def _init_selector(self):
        self.selector = MenuSelector(self.app, self, self.position, self.size, self.selector_colour, self.main_back_colour)
        self.selector_sprites = pygame.sprite.RenderPlain((self.selector))
    
    def draw(self, surface):
        self.selector_sprites.draw(surface)
        self.item_sprites.draw(surface)
    
    def update(self):
        self.selector_sprites.update()        
        self.item_sprites.update()
    
    def check_events(self, event):
        if event.type == KEYDOWN and event.key == K_UP:
            self.up()
            return
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.down()
            return
        elif event.type == KEYDOWN and event.key == K_RETURN:
            return self.process_selected()
        
    def process_selected(self):
        if (self.selected == len(self.list) - 1):
            self.app.running = "QUIT"
        
    def up(self):
    	self.selected = self.selected - 1
    	if (self.selected <= 0):
            self.selected = 0
    	self.selector.move_menu(self.selected)
    	
    def down(self):
    	self.selected = self.selected + 1
    	if (self.selected >= len(self.list)):
            self.selected = len(self.list) - 1
    	self.selector.move_menu(self.selected)
    
    def get_selected(self):
        return self.selected
    
    def get_selected_menu(self):
        return self.list[self.get_selected()]
    
    def focus(self):
        self.selector.focus()
        
    def unfocus(self):
        self.selector.unfocus()


class MenuSelector(pygame.sprite.Sprite):
    def __init__(self, app, parent, pos, size, colour, main_back_colour):
    	pygame.sprite.Sprite.__init__(self)
        self.app = app
        self.parent = parent
        self.pos = pos;
    	self.size = size;
        self.br = 20
        self.br2 = 50
        self.main_back_colour = main_back_colour
        self.main_colour = colour
        self.colour = adjust_c(self.main_colour, self.br)
        print "C: %s %s %s %s" % (self.colour[0],self.colour[1],self.colour[2],self.colour[3])
        self.colour_out = adjust_c(self.colour, self.br2)
        
        self.colour_fade = adjust_c(self.main_colour, 0)
        self.colour_out_fade = adjust_c(self.colour_fade, self.br2)

        self.move_up = False
    	self.move_down = False
    	self.move_pos = [0,0]
    	self.move_speed = calc_h(5)
        
        self.image = pygame.Surface(self.size,pygame.SRCALPHA)
        self._init_menu_bar()
        self.rect = self.image.get_rect()
    	self.rect = self.rect.move(pos)
        self.current_rect = self.rect.copy()
    
    def _init_menu_bar(self):
        self.r = calc_w(10)
        self.menu_bar_width = (self.size[0] - self.r)
        self.menu_bar_left = (self.r) / 2
        self.menu_bar = pygame.Surface(self.size,pygame.SRCALPHA)
        if (self.main_back_colour):
            self.menu_bar.fill(self.main_back_colour)
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour, self.colour_out), (self.menu_bar_left, 0))
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour_out, self.colour), (self.menu_bar_left + (self.menu_bar_width / 2), 0))
        self.image.blit(self.menu_bar, (0,0))
    
    def move_menu(self, selected):
    	if not (self.move_up or self.move_down):
            _m_pos = (self.pos[0], self.pos[1] + (self.size[1] * selected))
            self.next_rect = self.rect.move([0, 0])
            if (self.next_rect.y > _m_pos[1]):
                self.move_up = True
            elif (self.next_rect.y < _m_pos[1]):
                self.move_down = True
            self.next_rect.y = _m_pos[1]
    	
    def update(self):
    	if (self.move_up):
            self.current_rect = self.rect.copy()
            if (self.current_rect.y > self.next_rect.y):
                self.movement = self.current_rect.move([0, -self.move_speed])
            else:
                self.movement = self.next_rect
                self.move_up = False
                self.parent.parent.update_selected()
            self.rect = self.movement
            self.update_app()
    	elif (self.move_down):
            self.current_rect = self.rect.copy()
            if (self.current_rect.y < self.next_rect.y):
                self.movement = self.current_rect.move([0, self.move_speed])
            else:
                self.movement = self.next_rect
                self.move_down = False
                self.parent.parent.update_selected()
            self.rect = self.movement
            self.update_app()
    
    def update_app(self):
        self.app.update()
    
    def focus(self):
        if (self.main_back_colour):
            self.menu_bar.fill(self.main_back_colour)
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour, self.colour_out), (self.menu_bar_left, 0))
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour_out, self.colour), (self.menu_bar_left + (self.menu_bar_width / 2), 0))
        self.image.blit(self.menu_bar, (0,0))
        self.update_app()
        
    def unfocus(self):
        if (self.main_back_colour):
            self.menu_bar.fill(self.main_back_colour)
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour_fade, self.colour_out_fade), (self.menu_bar_left, 0))
        self.menu_bar.blit(gradients.horizontal((self.menu_bar_width / 2, self.size[1]), self.colour_out_fade, self.colour_fade), (self.menu_bar_left + (self.menu_bar_width / 2), 0))
        self.image.blit(self.menu_bar, (0,0))
        self.update_app()