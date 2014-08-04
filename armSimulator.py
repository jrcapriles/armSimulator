# -*- coding: utf-8 -*-
"""
Created on Fri May  2 01:17:09 2014

@author: jrcapriles
"""

import pygame, Buttons
from pygame.locals import *
import ode
from math import atan2, acos, asin
from numpy import *
from Point import *
import matplotlib.pyplot as plt


class armSimulator( object ):
    def __init__( self, width, lenght, links):
        self.width, self.lenght, self.links = width, lenght, links
        self.L = ones(self.links)
        # Initialize pygame
        pygame.init()
        # Open a display
        self.srf = pygame.display.set_mode((self.width,self.lenght))
        pygame.display.set_caption(str(links) + "-link pendulum")
        self.fps = 50
        self.dt = 1.0/self.fps
        self.loopFlag = True
        #Parameters
        self.g= -9.81
        self.maxF = 20*ones((1,links))
        self.thetad = zeros((1,links)) 
        self.goal_button = Buttons.Button(self.srf, color = (200,0,0), x = 10, y = 10, length =  50, height = 25, width = 0, text = "Goal", text_color = (255,255,255), font_size = 20, fade_on = False)

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

    def runSimulation(self, case, targets):
        
        self.createIC() 
        self.createArm(case)
        self.setTarget(targets)
        
        # Simulation loop.
        self.clk = pygame.time.Clock()

        while self.loopFlag:
            
            events = pygame.event.get()
            for e in events:
                if e.type==QUIT:
                    self.loopFlag=False
                if e.type==KEYDOWN:
                    if e.type==KEYDOWN:
                        if e.key == K_g:
                            print "New Goals: please click the new goal over the red circle"
                            self.setNewGoal()
                    else:
                        self.loopFlag=False
                elif e.type == MOUSEBUTTONDOWN:
                    if self.goal_button.pressed(pygame.mouse.get_pos()):
                        print "New Goals: please click the new goal over the red circle"
                        self.setNewGoal()


            # Clear the screen
            self.srf.fill((255,255,255))

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
            
            #self.setTarget(-0.8*pi*ones((1,self.links)))
            
            for i in range(0,self.links):
                x1,y1,z1 = self.body[i].getPosition()
                x.append(x1)
                y.append(y1)
                z.append(z1)
                vx1,vy1,vz1 = self.body[i].getAngularVel()
                vx.append(vx1)
                vy.append(vy1)
                vz.append(vz1)
                theta.append(self.j[i].getAngle()) 
                #thetad.append(-0.5*pi)
                errTheta.append(theta[i]- self.getTarget(i))

                thetaDot.append(sum(vz))
                #thetaDotd.append(0.0)
                errThetaDot.append(self.getTarget(i)+thetaDot[i])
                
                if i == 0: #Kinematics
                    xd.append(-self.L[0]*sin(-self.getTarget(0)))
                    yd.append(-self.L[0]*cos(-self.getTarget(0)))
                    #xd.append(-self.L[0]*sin(-self.newGoal[0]))
                    #yd.append(-self.L[0]*cos(-self.newGoal[0]))
                    
                else:
                    xd.append(xd[i-1]+self.L[i]*sin(-sum(self.thetad)))#self.getTargetRange(0,i))+self.getTarget(i)))
                    yd.append(yd[i-1]-self.L[i]*cos(-sum(self.thetad)))#self.getTargetRange(0,i))+self.getTarget(i)))
                
                

                
                T.append(-errTheta[i])

                #Set servo values
                self.j[i].setParam(ode.ParamVel, T[i])
                self.j[i].setParam(ode.ParamFMax, self.getMaxF(i))
            
           #Drawings
           
            #xx,yy = self.FK(self.thetad)           
            #pygame.draw.circle(self.srf, (0,128,0), self.world2screen(xx,yy), 10, 0)   #(Targets) 
           
           
            for i in range(0,self.links):
                pygame.draw.circle(self.srf, (55,0,200), self.world2screen(x[i],y[i]), 10, 0)     #(Motors)
                pygame.draw.circle(self.srf, (55,0,100), self.world2screen(xd[i],yd[i]), 10, 0)   #(Targets) 
                
                if i==0:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(self.IC[0].getPointX(),self.IC[0].getPointY()), self.world2screen(x[i],y[i]), 2)
                    pygame.draw.circle(self.srf, (255,0,0), self.world2screen(self.IC[i].getPointX(),self.IC[i].getPointY()), 5, 0) #(origin)
                else:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(x[i-1],y[i-1]), self.world2screen(x[i],y[i]), 2)

            self.drawBackLines()
            
            self.goal_button.update() #create_button(self.srf, (200,0,0), 10, 10, 50, 25, 0, "Goal", (255,255,255))
        
            pygame.display.flip()

            # Next simulation step
            self.world.step(self.dt)

            # Try to keep the specified framerate    
            self.clk.tick(self.fps)
            
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
            self.j[i].MaxForce = 10
        
    def FK(self,thetas):
        x_e=self.L[0]*sin(thetas[0])+self.L[1]*sin(sum(thetas))
        y_e=self.L[0]*cos(thetas[0])+self.L[1]*cos(sum(thetas))
        return x_e, -y_e
    
    def IK(self, x, y):
        #inverse kinematics
        ang2b = acos(self.clean_cos((x**2+y**2-self.L[0]**2-self.L[1]**2)/(2*self.L[0]*self.L[1])))
        ang1b = atan2(y,x) - atan2(self.L[1]*sin(ang2b),(self.L[0]+self.L[1]*cos(ang2b))) +pi/2
        print "New Angles",ang1b, ang2b
        return  (ang1b, -ang2b)
                
  
    def clean_cos(self,cos_angle):
        return min(1,max(cos_angle,-1))
    
    def setNewGoal(self):
        self.go = (0,0)
        self.newGoal = zeros(self.links)
        i = 0
    
        self.red_circle = (self.width/2,self.lenght/2)
        self.white_circle = (self.width/2,self.lenght/2)
        self.newGoalFlag =True
        

        while self.newGoalFlag:
            # Draw the current circle in red and erase previous
            pygame.draw.circle(self.srf, (255,0,0), (self.red_circle[0],self.red_circle[1]), 130*self.links, 1) 
            pygame.draw.circle(self.srf, (255,0,0), (self.red_circle[0],self.red_circle[1]), 10, 1) 
                        
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
                    desired = pygame.mouse.get_pos()
                    print self.screen2worldX(desired[0]), self.screen2worldY(desired[1])
                    self.white_circle = self.red_circle
                    self.red_circle = desired
                    self.newGoal = self.IK(self.screen2worldX(desired[0]), self.screen2worldY(desired[1]) )                   
                    self.setTarget(self.newGoal)
                    self.newGoalFlag = False
                        
                    #if i==0:
                    #    x01 = self.red_circle[0] - self.white_circle[0]                    
                    #    y01 = self.red_circle[1] - self.white_circle[1]
                    #    self.newGoal[i] = atan2(x01,y01)
                    #    self.red_circle = self.world2screenX(self.L[0]*sin(self.newGoal[i])),self.world2screenY(-self.L[0]*cos(self.newGoal[i]))
#                    elif i==1:
#                        rx,ry = self.screen2world(self.red_circle[0],self.red_circle[1])
#                        wx,wy = self.screen2world(self.white_circle[0],self.white_circle[1])
#                        cos2 = (pow(rx,2)+pow(ry,2) - pow(self.L[0,0],2) - pow(self.L[0,1],2))/(2*self.L[0,0]*self.L[0,1])
#                        cos2 = self.clean_cos(cos2)
#                        
#                        
#                        ang1, ang2 = self.IK(rx,ry)
#                        self.newGoal[i] = ang2  
#                                                
#                        self.red_circle = self.world2screenX(self.L[0,0]*sin(self.newGoal[i])+self.L[0,1]*sin(self.newGoal[i-1]+self.newGoal[i])),self.world2screenY(-self.L[0,0]*cos(self.newGoal[i])+self.L[0,1]*cos(self.newGoal[i-1]+self.newGoal[i]))
#
#                        print self.newGoal[i]
                    #else:
                    #    self.newGoal[i] = 0
                  
                    #i +=1
                    #if i == self.links:
                    #    self.setTarget(self.newGoal)
                    #    self.newGoalFlag = False
