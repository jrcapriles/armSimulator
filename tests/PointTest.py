# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 23:01:44 2014

@author: Jose Capriles
"""

from armSimulator import Point
import unittest
import random

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
        

if __name__ == '__main__':
    unittest.main()
