# -*- coding: utf-8 -*-
"""
Created on Fri May  2 01:17:09 2014

@author: jrcapriles
"""

import pygame, Buttons
from pygame.locals import *
import ode
import random
from math import atan2, acos, asin
from numpy import *
from Point import *
import matplotlib.pyplot as plt

from sympy import solve,symbols, Eq
from sympy import sin as nsin
from sympy import cos as ncos


class armSimulator( object ):
    def __init__( self, width, lenght, links):
        self.width, self.lenght, self.links = width, lenght, links
        self.L = ones(self.links)
        self.desired = None
        # Initialize pygame
        pygame.init()
        
        # Open a display
        self.srf = pygame.display.set_mode((self.width,self.lenght))
        pygame.display.set_caption(str(links) + "-Link Arm")
        self.fps = 50
        self.dt = 1.0/self.fps
        self.loopFlag = True
        #Parameters
        self.g= -9.81
        self.maxF = 20*ones((1,links))
        self.thetad = zeros((1,links)) 
        self.switch_counter = 0
        
        #TODO create trasnformation matrix (n=2,3,4...)
        self.T = []
        for count in range(0,self.links):
            self.T.append(zeros(shape=(4,4)))
        
        #Buttons
        self.goal_button = Buttons.Button(self.srf, color = (200,0,0), x = 10, y = 10, length =  50, height = 25, width = 0, text = "Goal", text_color = (255,255,255), font_size = 20, fade_on = False)
        self.switch_button = Buttons.Button(self.srf, color = (200,0,0), x = 60, y = 10, length =  50, height = 25, width = 0, text = "Switch", text_color = (255,255,255), font_size = 20, fade_on = False)
        self.follow_button = Buttons.Button(self.srf, color = (200,0,0), x = 110, y = 10, length =  50, height = 25, width = 0, text = "Follow", text_color = (255,255,255), font_size = 20, fade_on = False)
        self.noise_button = Buttons.Button(self.srf, color = (200,0,0), x = 160, y = 10, length =  50, height = 25, width = 0, text = "Noise", text_color = (255,255,255), font_size = 20, fade_on = False)
        
        #Button Dictionary
        self.buttons = {0 : self.goal_button,
                        1 : self.switch_button,
                        2 : self.follow_button,
                        3 : self.noise_button}
                        
    def createIC(self):
        rest = [] 
        left = []
        right = []
        up =[]
        #First loop to create all different combinations of IC
        for i in range(0,self.links+1):
            rest.append(Point(0,-i,0))
            left.append(Point(i,0,0))
            right.append(Point(-i,0,0))
            up.append(Point(0,i,0))
           
        #Create the dicionary
        self.ICList = {"Rest":rest,
                       "Left":left,
                       "Right":right,
                       "Up":up}
        
    def setTarget(self,target):
        self.thetad = target
        self.newGoal = target
    
    def getTarget(self, i):
        return self.thetad[i]
        
    def getTargetRange(self, i,j):
        return self.thetad[i:j]
        
    def setIC(self, case):
        self.IC = self.ICList[case]
        
    def getIC(self,i):
        return self.IC[i].getPoint()
    
    def setMaxF(self, F):
        if F is None:
            self.maxF = [10 for i in range(self.links)]
        else:
            self.maxF = F
    
    def getMaxF(self,i):
        return self.maxF[i]
        
    def getWidth(self):
        return self.width

    def getLenght(self):
            return self.leght
    
    def world2screen(self,x,y):
        return int(self.width/2 + 128*x), int(self.lenght/2 - 128*y)
    
    def world2screenX(self,x):
        return int(self.width/2 + 128*x)
    
    def world2screenY(self,y):
        return int(self.lenght/2 - 128*y)
        
    def screen2worldX(self,x):
        return (float(x - self.width/2)/128)
        
    def screen2worldY(self,y):
        return (float(-y + self.lenght/2)/128)
    
    def screen2world(self,x,y):
        return (float(x - self.width/2)/128), (float(-y + self.lenght/2)/128)
    
    def surf(self, x,y):
        return (pow(x-pi/2,2) + pow(0.9*pi*y,2) - pow(pi/2,2))

    def phi(self, y):
        return -y -(2*self.a/sqrt(pow(self.a,2)-1))*arctan(sqrt((self.a-1)/(self.a+1))*tan(y/2)) 

    def checkEvents(self):
        #Get the list of events from Pygame         
        events = pygame.event.get()
        for e in events:
            if e.type==QUIT:
                self.loopFlag=False
            elif e.type==KEYDOWN:
                if e.key == K_g:
                    print "New Goals: please click the new goal over the red circle"
                    self.setNewGoal()
                elif e.key == K_f:
                    self.follow = not self.follow
                    if self.follow:
                        self.updateBottons(2,(100,0,0))
                    else:
                        self.updateBottons(2,(200,0,0))
                elif e.key == K_s:
                    print "Switching side"
                    self.switchSide()
                elif e.key == K_n:
                    self.noise = not self.noise
                    if self.noise:
                        self.updateBottons(3,(100,0,0))
                    else:
                        self.updateBottons(3,(200,0,0))
                else:
                    self.loopFlag=False
            elif e.type == MOUSEBUTTONDOWN:
                if self.goal_button.pressed(pygame.mouse.get_pos()):
                    print "New Goals: please click the new goal over the red circle"
                    self.setNewGoal()
                elif self.switch_button.pressed(pygame.mouse.get_pos()):
                    print "Switching side"
                    self.switchSide()
                elif self.follow_button.pressed(pygame.mouse.get_pos()):
                    self.follow = not self.follow
                    if self.follow:
                        self.updateBottons(2,(100,0,0))
                    else:
                        self.updateBottons(2,(200,0,0))
                elif self.noise_button.pressed(pygame.mouse.get_pos()):
                    self.noise = not self.follow
                    if self.noise:
                        self.updateBottons(3,(100,0,0))
                    else:
                        self.updateBottons(3,(200,0,0))
                        
                       


    def runSimulation(self, case, targets):
        
        self.createIC() 
        self.createArm(case)
        self.setTarget(targets)
        
        # Simulation loop.
        self.clk = pygame.time.Clock()
        self.follow = False
        self.noise = False

        
        while self.loopFlag:
            # Check for events
            self.checkEvents()     
            
            if self.follow:
                self.desired = pygame.mouse.get_pos()
                print self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1])
                self.newGoal = self.IK(self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1]) )                   
                self.setTarget(self.newGoal)
                        
            # Clear the screen
            self.srf.fill((255,255,255))

            
            if self.follow:
                pygame.draw.circle(self.srf, (255,0,0), (self.world2screen(0,0)), 130*self.links, 1) 

            x = []
            xd = []
            y = []
            yd = []
            z = []
            vx = []
            vy = []
            vz = []
            theta = []
            #thetad = []
            errTheta = []            
            thetaDot = []
            errThetaDot = []            
            T = []
            
            for i in range(0,self.links):
                
                x1,y1,z1 = self.body[i].getPosition()
                
                if self.noise:
                    x1 += random.uniform(-0.01, 0.01)
                    y1 += random.uniform(-0.01, 0.01)
                
                x.append(x1)
                y.append(y1)
                z.append(z1)
                vx1,vy1,vz1 = self.body[i].getAngularVel()
                vx.append(vx1)
                vy.append(vy1)
                vz.append(vz1)
                theta.append(self.j[i].getAngle())
                
                #Compute error  (normalized)
                if (theta[i]- self.getTarget(i)) > pi:
                    err = theta[i] - self.getTarget(i) - 2*pi
                elif (theta[i]- self.getTarget(i)) < -pi:
                    err = theta[i] - self.getTarget(i) + 2*pi
                else:
                    err = theta[i] - self.getTarget(i)
                    
                errTheta.append(err) #theta[i]- self.getTarget(i))
                #if i == 0:
                #    print errTheta[0]
                thetaDot.append(sum(vz))
                errThetaDot.append(self.getTarget(i)+thetaDot[i])
                
                if i == 0: #Kinematics
                    xd.append(-self.L[0]*sin(-self.getTarget(0)))
                    yd.append(-self.L[0]*cos(-self.getTarget(0)))
                    
                else:
                    xd.append(xd[i-1]+self.L[i]*sin(-sum(self.thetad)))
                    yd.append(yd[i-1]-self.L[i]*cos(-sum(self.thetad)))
                
                #print "theta ", i, theta[i]
                T.append(-errTheta[i])

                #Set servo values
                self.j[i].setParam(ode.ParamVel, T[i])
                self.j[i].setParam(ode.ParamFMax, self.getMaxF(i))

            if self.desired is not None: #(Targets) 
                pygame.draw.circle(self.srf, (200,45,10), (self.desired[0],self.desired[1]), 12, 0)   
                pygame.draw.circle(self.srf, (255,255,255), (self.desired[0],self.desired[1]), 10, 0) 
                
            for i in range(0,self.links):
                pygame.draw.circle(self.srf, (55,0,200), self.world2screen(x[i],y[i]), 10, 0)     #(Motors)
                
                if i==0:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(self.IC[0].getPointX(),self.IC[0].getPointY()), self.world2screen(x[i],y[i]), 10)
                    pygame.draw.circle(self.srf, (255,0,0), self.world2screen(self.IC[i].getPointX(),self.IC[i].getPointY()), 5, 0) #(origin)
                else:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(x[i-1],y[i-1]), self.world2screen(x[i],y[i]), 10)

            self.drawBackLines()
            self.updateBottons()
            
            pygame.display.flip()

            # Next simulation step
            self.world.step(self.dt)

            # Try to keep the specified framerate    
            self.clk.tick(self.fps)
            

            
    def updateBottons(self,i=None,color = None):
        #Function to update the buttons defined at the button dictionary.
        if i is None and color is None:
            self.goal_button.update()
            self.switch_button.update()
            self.follow_button.update()
            self.noise_button.update()
            return True
        elif color is None:
            self.buttons[i].update()
        else:
            self.buttons[i].color = color
            self.buttons[i].update()

    def drawBackLines(self):    
        #Draw the back lines of the screen
        pygame.draw.line(self.srf, (0,0,0), self.world2screen(0,-self.lenght/2), self.world2screen(0,self.lenght/2), 1)    
        pygame.draw.line(self.srf, (0,0,0), self.world2screen(-self.width/2,0), self.world2screen(self.width/2,0), 1) 
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(1,-self.lenght/2),self.world2screen(1,self.lenght/2), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(2,-self.lenght/2),self.world2screen(2,self.lenght/2), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-1,-self.lenght/2),self.world2screen(-1,self.lenght/2), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-2,-self.lenght/2),self.world2screen(-2,self.lenght/2), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-self.width/2,1),self.world2screen(self.width/2,1), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-self.width/2,2),self.world2screen(self.width/2,2), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-self.width/2,-1),self.world2screen(self.width/2,-1), 1)    
        pygame.draw.line(self.srf, (192,192,192), self.world2screen(-self.width/2,-2),self.world2screen(self.width/2,-2), 1)    
    
    
    def createArm(self,case):
        #This routine create the arm and set the initial condition accordingly.
        self.setIC(case)
        # Create a world object
        self.world = ode.World()
        self.world.setGravity((0,self.g,0))
        
        # Create the bodies
        self.body = []        
        self.M = []
        self.j = []
        for i in range(0,self.links):
            self.body.append(ode.Body(self.world))
            self.M.append(ode.Mass())
            self.M[i].setSphere(2500, 0.025)
            self.body[i].setMass(self.M[i])
            self.body[i].setPosition(self.getIC(i+1))
            
            self.j.append(ode.HingeJoint(self.world))
            if i==0:
                self.j[i].attach(self.body[0], ode.environment)
                self.j[i].setAnchor(self.getIC(0))
            else:
                self.j[i].attach(self.body[i-1], self.body[i])
                self.j[i].setAnchor(self.body[i-1].getPosition())
            
            self.j[i].setAxis( (0,0,1) )
            self.j[i].setParam(ode.ParamLoStop, -5.0) 
            self.j[i].setParam(ode.ParamHiStop,5.0) 
            self.j[i].MaxForce = 1
        
    def FK(self,thetas):
        
        self.T[0][0][0] = cos(thetas[0]) 
        self.T[0][0][1] = -sin(thetas[0])
        self.T[0][1][0] = sin(thetas[0])
        self.T[0][1][1] = cos(thetas[0])
        #self.T[1][0][3] = self.L[0]       
        self.T[0][2][2] = 1 
        self.T[0][3][3] = 1 
        
        self.T[1][0][0] = cos(thetas[1]) 
        self.T[1][0][1] = -sin(thetas[1])
        self.T[1][1][0] = sin(thetas[1])
        self.T[1][1][1] = cos(thetas[1])
        self.T[1][0][3] = self.L[0]
        self.T[1][1][3] = self.L[0]
        self.T[1][2][2] = 1 
        self.T[1][3][3] = 1 
        
        Tend = zeros(shape=(4,4)) 
        Tend[0][0] = 1
        Tend[1][1] = 1
        Tend[2][2] = 1
        Tend[3][3] = 1
        Tend[0][3] = self.L[1]
        Tend[1][3] = self.L[1]
        
        
        prod = self.T[0]*(self.T[1]*Tend)
        
        
        print sum(prod2[0])
        print sum(prod2[1])
        
        x_e=self.L[0]*sin(thetas[0])+self.L[1]*sin(sum(thetas))
        y_e=self.L[0]*cos(thetas[0])+self.L[1]*cos(sum(thetas))
        
        print x_e, y_e
        return x_e, -y_e
    
    def IK(self, x, y,switch = None):
        #inverse kinematics
        if self.links == 2:        
            ang2b = acos(self.clean_cos((x**2+y**2-self.L[0]**2-self.L[1]**2)/(2*self.L[0]*self.L[1])))
            if switch is not None:
                ang2b = -ang2b
            ang1b = atan2(y,x) - atan2(self.L[1]*sin(ang2b),(self.L[0]+self.L[1]*cos(ang2b))) +pi/2
            #print "New Angles",ang1b, ang2b
            return  (ang1b, -ang2b)
        
#        elif self.links == 3:
#            c2 = self.clean_cos((x**2+y**2-self.L[0]**2-self.L[1]**2)/(2*self.L[0]*self.L[1]))
#            s2 = sqrt(1-c2**2)
#            ang2 = atan2(s2,c2)
#            k1 = self.L[0]+self.L[1]*c2
#            k2 = self.L[1]*s2
#            ang1 = atan2(y,x)-atan2(k2,k1) + pi/2            
#            sphi = (y-self.L[0]*sin(ang1)-self.L[1]*sin(ang1+ang2))/self.L[2]
#            cphi = (y-self.L[0]*cos(ang1)-self.L[1]*cos(ang1+ang2))/self.L[2]
#            ang3 = atan2(sphi,cphi) - ang1 - ang2
#            return (ang1, ang2, ang3)

        
  
    def is_odd(self, num):
        return num & 0x1
    
    def clean_cos(self,cos_angle):
        return min(1,max(cos_angle,-1))
    
    def setNewGoal(self):
        self.go = (0,0)
        self.newGoal = zeros(self.links)
        i = 0
        self.red_circle = (self.width/2,self.lenght/2)
        self.white_circle = (self.width/2,self.lenght/2)
        self.newGoalFlag =True
        self.switch_counter = 0

        while self.newGoalFlag:
            # Draw the current circle in red and erase previous
            pygame.draw.circle(self.srf, (255,0,0), (self.world2screen(0,0)), 130*self.links, 1) 
            pygame.display.flip()
            
            events = pygame.event.get()
            
            for e in events:
                if e.type==QUIT:
                    self.loopFlag=False
                    self.newGoalFlag = False
                if e.type==KEYDOWN:
                    self.loopFlag=False
                    self.newGoalFlag = False
                if e.type == MOUSEBUTTONDOWN:
                    self.desired = pygame.mouse.get_pos()
                    print self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1])
                    self.white_circle = self.red_circle
                    self.red_circle = self.desired
                    self.newGoal = self.IK(self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1]) )                   
                    self.setTarget(self.newGoal)
                    
                    self.FK(self.newGoal)

                    self.newGoalFlag = False
        
            self.updateBottons(0,(100,0,0)) #0 for goal

        #After the while
        self.updateBottons(0,(200,0,0))
        

    def switchSide(self):
        if self.is_odd(self.switch_counter):
            self.newGoal = self.IK(self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1]))                   
        else:
            self.newGoal = self.IK(self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1]),True)                   
        #self.newGoal = self.IK(self.screen2worldX(self.desired[0]), self.screen2worldY(self.desired[1]),True)                   
        self.setTarget(self.newGoal)
        self.switch_counter +=1
                    