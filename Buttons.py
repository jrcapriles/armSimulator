# -*- coding: cp1252 -*-
#/usr/bin/env python
#Simon H. Larsen
#Buttons
#Project startet: d. 26. august 2012
import pygame
from pygame.locals import *
pygame.init()
class Button:
    def __init__(self, surface, **kwargs):
        self.surface = surface
        self.text = kwargs.get('text','Button Test')
        self.length = kwargs.get('length',200)        
        self.width = kwargs.get('width',0)        
        self.height = kwargs.get('height',100)        
        self.x = kwargs.get('x',225)        
        self.y = kwargs.get('y',135)        
        self.color = kwargs.get('color', (107,142,35) )
        self.border_color = kwargs.get('border_color', (190,190,190) )        
        self.text_color = kwargs.get('text_color',(255,255,255) )        
        self.fade_on = kwargs.get('fade_on',False )
        self.font_size = kwargs.get('font_size', None)
        self.create_button(surface, self.color, self.border_color, self.x, self.y, self.length, self.height, self.width, self.text, self.text_color, self.font_size, self.fade_on)
        self.draw_button(surface, self.color, self.border_color, self.length, self.height, self.x, self.y, self.width,self.fade_on)           
    
    def create_button(self, surface, color, border_color, x, y, length, height, width, text, text_color, font_size, fade_on):
        surface = self.draw_button(surface, color, border_color, length, height, x, y, width,fade_on)
        surface = self.show_text(surface, text, text_color, length, height, x, y, font_size)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def show_text(self, surface, text, text_color, length, height, x, y, font_size = None):
        if not font_size:
            font_size = int(length//len(text))
            
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, border_color, length, height, x, y, width, fade_on):           
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, border_color, (x,y,length,height), 1)  
        self.show_text(surface,self.text, self.text_color, self.length, self.height, self.x, self.y, self.font_size)
        return surface
    
    def add_fade(self):
        for i in range(1,10):
            s = pygame.Surface((self.length+(i*2),self.height+(i*2)))
            s.fill(self.color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, self.color, (self.x-i,self.y-i,self.length+i,self.height+i), self.width)
            self.surface.blit(s, (self.x-i,self.y-i))
        
    def update(self):
        if self.fade_on:
            self.add_fade()
        self.draw_button(self.surface, self.color, self.border_color, self.length, self.height, self.x, self.y, self.width, self.fade_on)

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print "The button was pressed!"
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
