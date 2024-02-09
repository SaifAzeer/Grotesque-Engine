import os.path as path
from sys import path as sysPath
sysPath.append(path.dirname(path.abspath(path.join(__file__ ,"../"))))

from Data.Constant import GRID_NUMBER

class FloodFill:
    def __init__(self):
        self.addedloc = []

    def Start(self,maps,start,imageID):
        self.addedloc= []
        self.maps = maps
        self.maps[start[1]][start[0]] = 0
        self.Find_neighbour(start[0],start[1],0,imageID)


    def Find_neighbour(self,x,y,empty_val,visited_val):
        if x <0 or x >= GRID_NUMBER[0] or y <0 or y>= GRID_NUMBER[1] :
            return
        if self.maps[y][x] != empty_val:
            return
        
        self.maps[y][x] = visited_val
        self.addedloc.append([x,y])

        self.Find_neighbour(x-1,y,empty_val,visited_val)
        self.Find_neighbour(x+1,y,empty_val,visited_val)
        self.Find_neighbour(x,y-1,empty_val,visited_val)
        self.Find_neighbour(x,y+1,empty_val,visited_val)
       