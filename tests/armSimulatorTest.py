# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 14:46:01 2014

@author: joser
"""

from armSimulator import armSimulator
import unittest
import random

class armSimulatorTest(unittest.TestCase):
    
    def setUp(self):
        self.links = 2        
        self.arm = armSimulator(800,800,self.links)        
        self.targets = []
        for i in range(self.links):
            self.targets.append(random.random())
        
    def test_setTarget(self):
        self.arm.setTarget(self.targets)
        for i in range(self.links):
            self.assertEqual(self.arm.thetad[i],self.targets[i])
            self.assertEqual(self.arm.newGoal[i],self.targets[i])
       
    def test_getTarget(self):
        self.arm.thetad = self.targets
        for i in range(self.links):
            self.assertEqual(self.arm.getTarget(i),self.targets[i])

    def test_getTargetRange(self):
        self.arm.thetad = self.targets
        self.assertEqual(self.arm.getTargetRange(0,self.links),self.targets)
      
    def test_setMaxF_wArg(self):
        self.arm.setMaxF(self.targets)        
        for i in range(self.links):
            self.assertEqual(self.arm.maxF[i],self.targets[i])
    
    def test_setMaxF_woArg(self):        
        self.arm.setMaxF(None)
        for i in range(self.links):
            self.assertEqual(self.arm.maxF[i],10)
       
    def test_getMaxF(self):
        self.arm.maxF = self.targets
        for i in range(self.links):
            self.assertEqual(self.arm.getMaxF(i),self.targets[i])

          
    def getMaxF(self,i):
        return self.maxF[i]

if __name__ == '__main__':
    unittest.main()
