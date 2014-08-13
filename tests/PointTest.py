# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 23:01:44 2014

@author: Jose Capriles
"""

from armSimulator import Point
import unittest
import random
from math import sqrt


class PointTest(unittest.TestCase):
    
    def setUp(self):
        self.x = random.random()
        self.y = random.random()
        self.z = random.random()
        self.Point = Point(self.x,self.y,self.z)
        
    def test_getPointX(self):
        self.assertEqual(self.Point.getPointX(),self.x)
        
    def test_getPointY(self):
        self.assertEqual(self.Point.getPointY(),self.y)
        
    def test_getPointZ(self):
        self.assertEqual(self.Point.getPointZ(),self.z)

    def test_getPoint(self):
        point = self.Point.getPoint()
        self.assertEqual(point[0],self.x)
        self.assertEqual(point[1],self.y)
        self.assertEqual(point[2],self.z)
        
    def test_distFrom(self):        
        d=self.Point.distFrom(0.0,0.0,0.0)
        self.assertEqual(d,sqrt(self.x**2+self.y**2+self.z**2))
        

if __name__ == '__main__':
    unittest.main()
