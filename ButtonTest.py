# Jose Capriles
# 07/26/2014

import pygame, Buttons
from pygame.locals import *

#Initialize pygame
pygame.init()

class Button_Example:
    def __init__(self):
        self.loopFlag = True
        self.main()
    
    #Create a display
    def display(self):
        self.screen = pygame.display.set_mode((650,370),0,32)
        pygame.display.set_caption("Button.py TEST")

    #Update the display and show the button
    def update_display(self):
        self.screen.fill((30,144,255))
        self.Button1.update() 
        pygame.display.flip()


    #Run the loop
    def main(self):
        self.display()
        self.Button1 = Buttons.Button(self.screen, color = (107,142,35), x = 225, y = 135, length = 200, height = 100, width = 0, text ="Button Test", text_color = (255,255,255), font_size=25, fade_on = False)


        while self.loopFlag:
            self.update_display()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loopFlag = False
                if event.type == KEYDOWN:
                    self.loopFlag=False
                if event.type == MOUSEBUTTONDOWN:
                    if self.Button1.pressed(pygame.mouse.get_pos()):
                        print "Test Passed!"

if __name__ == '__main__':
    obj = Button_Example()
