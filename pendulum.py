# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 22:45:20 2014

@author: joser
"""

# Based on the pyODE example 2

import pygame
from pygame.locals import *
import ode
from numpy import *


def world2screen(x,y):
    "Convert world coordinates to pixel coordinates."
    return int(512+170*x), int(700-170*y)


# Initialize pygame
pygame.init()

# Open a display
srf = pygame.display.set_mode((1024,820))
pygame.display.set_caption("The pendulum")
# Create a world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((1,2,0))

body2 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body2.setMass(M)
body2.setPosition((2,2,0))

# Add actuated motor
j1 = ode.HingeJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0,2,0) )
j1.setAxis( (0,0,1) )
j1.setParam(ode.ParamLoStop, -5.0) 
j1.setParam(ode.ParamHiStop,5.0) 
MaxForce = 100

# Connect body2 with body1
j2 = ode.HingeJoint(world) #ode.BallJoint(world)
j2.attach(body1, body2)
j2.setAnchor( body1.getPosition() ) 
j2.setAxis ((0,0,1)) 
j2.setParam(ode.ParamLoStop, -5.0) 
j2.setParam(ode.ParamHiStop,5.0) 

# Simulation loop.
fps = 50
dt = 1.0/fps
loopFlag = True
clk = pygame.time.Clock()



while loopFlag:
    events = pygame.event.get()
    for e in events:
        if e.type==QUIT:
            loopFlag=False
        if e.type==KEYDOWN:
            loopFlag=False

    # Clear the screen
    srf.fill((255,255,255))

    # Draw the two bodies
    x1,y1,z1 = body1.getPosition()
    x2,y2,z2 = body2.getPosition()
    
    vx1,vy1,vz1 = body1.getAngularVel()
    vx2,vy2,vz2 = body2.getAngularVel()
     
    #Servo 1 
    S1Angle = j1.getAngle() 
    S1DesiredAngle = -0.5
    S1Error = S1Angle - S1DesiredAngle 
    S1DesiredVelocity = -S1Error 

    #Servo 2 
    S2Angle = j2.getAngle() 
    S2DesiredAngle = -0.4 
    S2Error = S2Angle - S2DesiredAngle 
    S2DesiredVelocity = -S2Error 
    
    #Set servo values
    j1.setParam(ode.ParamVel, S1DesiredVelocity) 
    j1.setParam(ode.ParamFMax, MaxForce) 
    j2.setParam(ode.ParamVel, S2DesiredVelocity) 
    j2.setParam(ode.ParamFMax, MaxForce) 

    
    pygame.draw.circle(srf, (55,0,200), world2screen(x1,y1), 10, 0)
    pygame.draw.line(srf, (55,0,200), world2screen(0,2), world2screen(x1,y1), 2)
    pygame.draw.circle(srf, (55,0,200), world2screen(x2,y2), 10, 0)
    pygame.draw.line(srf, (55,0,200), world2screen(x1,y1), world2screen(x2,y2), 2)

    
    #inverse kinematics
    #x1_des = 1.0*cos(S1DesiredAngle)
    #y1_des = 1.0*sin(S2DesiredAngle)+2 #If it is up +2
    #x2_des = x1_des + 1.0*cos(S1DesiredAngle-S2DesiredAngle)
    #y2_des = y1_des + 1.0*sin(S1DesiredAngle-S2DesiredAngle) 
    #pygame.draw.circle(srf, (55,0,100), world2screen(x1_des,y1_des), 10, 0)
    #pygame.draw.circle(srf, (55,0,100), world2screen(x2_des,y2_des), 10, 0)
    
    pygame.display.flip()

    # Next simulation step
    world.step(dt)

    # Try to keep the specified framerate    
    clk.tick(fps)
    

