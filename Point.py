# -*- coding: utf-8 -*-
"""
Created on Fri May  2 01:17:09 2014

@author: Jose Capriles 
"""

class Point( object ):
    def __init__( self, x, y, z):
        self.x, self.y, self.z = x, y, z
        
    def distFrom( self, x, y, z ):
        return math.sqrt( (self.x-x)**2 + (self.y-y)**2 + (self.z-z)**2 )
        
    def getPoint(self):
        return ((self.x, self.y, self.z))

    def getPointX(self):
        return self.x

    def getPointY(self):
        return self.y

    def getPointZ(self):
        return self.z


class PendulumState( object ):
    def __init__( self, x, y):
        self.x, self.y = x, y
        
    def getState(self):
        return ((self.x, self.y))
        
    def getStateX(self):
        return self.x
        
    def getStateY(self):
        return self.y
        
    def __add__(self, other):
        return PendulumState(self.x + other.x,self.y + other.y)
        
    def __sub__(self, other):
        return PendulumState(self.x - other.x,self.y - other.y)
    
    def __abs__(self):
        return PendulumState(abs(self.x),abs(self.y))