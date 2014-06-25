# -*- coding: utf-8 -*-
"""
Created on Fri May  2 01:17:09 2014

@author: jrcapriles
"""

import pygame
from pygame.locals import *
import ode
from numpy import *
from Point import *
import matplotlib.pyplot as plt


class armSimulator( object ):
    def __init__( self, width, lenght, links):
        self.width, self.lenght, self.links = width, lenght, links
        self.L = ones((1,self.links))
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
                    self.loopFlag=False

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
                    xd.append(-self.L[0,0]*sin(-self.getTarget(0)))
                    yd.append(-self.L[0,0]*cos(-self.getTarget(0)))
                else:
                    xd.append(xd[i-1]+self.L[0,i]*sin(-sum(self.getTargetRange(0,i))+self.getTarget(i)))
                    yd.append(yd[i-1]-self.L[0,i]*cos(-sum(self.getTargetRange(0,i))+self.getTarget(i)))
                
                T.append(-errTheta[i])

                #Set servo values
                self.j[i].setParam(ode.ParamVel, T[i])
                self.j[i].setParam(ode.ParamFMax, self.getMaxF(i))
            
           #Drawings
            for i in range(0,self.links):
                pygame.draw.circle(self.srf, (55,0,200), self.world2screen(x[i],y[i]), 10, 0)     #(Motors)
                pygame.draw.circle(self.srf, (55,0,100), self.world2screen(xd[i],yd[i]), 10, 0)   #(Targets) 
                
                if i==0:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(self.IC[0].getPointX(),self.IC[0].getPointY()), self.world2screen(x[i],y[i]), 2)
                    pygame.draw.circle(self.srf, (255,0,0), self.world2screen(self.IC[i].getPointX(),self.IC[i].getPointY()), 5, 0) #(origin)
                else:
                    pygame.draw.line(self.srf, (55,0,200), self.world2screen(x[i-1],y[i-1]), self.world2screen(x[i],y[i]), 2)


            self.drawBackLines()
    
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
        

            
