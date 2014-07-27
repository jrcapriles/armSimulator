# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 23:01:44 2014

@author: Jose Capriles
"""
import Point, random

class Point_Test:
    def __init__(self):
        self.loopFlag = True
        self.main()
    
    #Update the display and show the button
    def update(self):
        if self.Point.getPointX() == self.x:
            if self.Point.getPointY() == self.y:
                if self.Point.getPointZ() == self.z:
                    return True 
                else: return False
            else: return False
        else: return False
        
    #Run the loop
    def main(self):
        i = 0
        while self.loopFlag:
            self.x = random.random()
            self.y = random.random()
            self.z = random.random()        
            self.Point = Point.Point(self.x,self.y,self.z)
            self.loopFlag = self.update()
            i +=1
            if i>100:
                self.loopFlag = False
                print "Test passed"
                
if __name__ == '__main__':
    obj = Point_Test()
