# -*- coding: utf-8 -*-
"""
Created on Tue May 20 00:33:16 2014

@author: jrcapriles
"""

import armSimulator as arm
from numpy import pi   

sim =  arm.armSimulator(800,800,2)

sim.setMaxF(None) 
#sim.setMaxF([10,0]) 

sim.runSimulation("Rest",[-pi/2,-pi/2, pi])

       