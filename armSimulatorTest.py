# -*- coding: utf-8 -*-
"""
Created on Tue May 20 00:33:16 2014

@author: joser
"""

from armSimulator import *

sim =  armSimulator(600,600,5)

sim.setMaxF(None) #([10,10,10,10,0])#,2.5,0])

sim.runSimulation("Rest")

     