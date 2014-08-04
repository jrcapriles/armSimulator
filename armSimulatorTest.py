# -*- coding: utf-8 -*-
"""
Created on Tue May 20 00:33:16 2014

@author: jrcapriles
"""

from armSimulator import *

sim =  armSimulator(800,800,2)

sim.setMaxF(None) 

sim.runSimulation("Rest",[-pi/2,-pi/2, pi])

      