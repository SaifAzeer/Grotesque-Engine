''' Get surface for tiles, render ect...
    TODO-> create a dictionary of images name and type -> animation, ground type for ai to work on
           or just a simple big images to extract the tiles
        
    NOTE-> lets just assume that every picture > than tile size is an animation 
'''
import os.path as path
from sys import path as sysPath
sysPath.append(path.dirname(path.abspath(path.join(__file__ ,"../"))))

from typing import List, Tuple
from pygame import Surface,BLEND_RGBA_MULT,Rect
from pygame import image as pyImage
from Data.TileType import TileType,Tile_name_type
from Data.Constant import GRID_SIZE

from Animation.Animation import Animation
from Data.Global import Global
from dataclasses import dataclass


class Tiles:
    def __init__(self,gridPos,type,position,id = 0,image = ""):
        self.type = type
        self.position = position
        self.originalPos: List[int]
        self.gridPos = gridPos
        self.original_gridPos = gridPos
        self.offsetPos = [0,0]# use to drag image
        self.image:pyImage = image
        self.surface = Surface((50,50))
        self.Tile_name_type_direction : TileType = None
        self.ID = id

        self.animationSize : Tuple[int,int]
        self.animation : Animation
        if type == TileType.image:
            self.surface = pyImage.load(image)
            self.animationSize = self.check_if_animation_image(self.surface)
            if self.animationSize:
                self.animation = Animation(Global.tilePos)
                self.animation.load_from_image(image.split('/')[-1],self.animationSize[0],GRID_SIZE)
        self.Change_colour()
        
    def Load_image(self,image):
        self.surface = pyImage.load(image).convert_alpha()
        self.Change_colour()
       
    def Change_colour(self,colour = (150,150,150)):
        '''Change colour of preview tile and selected tile '''
        colour_surface = Surface(self.surface.get_size()).convert_alpha()
        colour_surface.fill(colour)
        self.mouse_preview_surface = self.surface.copy()
        self.mouse_preview_surface.blit(colour_surface,(0,0),special_flags = BLEND_RGBA_MULT)

    def Get_pos_by_grid(self,grid,tileMapMovement):
        '''get new position of tile when moving the map'''
        self.gridPos = grid.GetMainGridLoc((self.originalPos[0]+ tileMapMovement[0],self.originalPos[1]+ tileMapMovement[1]))
        self.position = grid.GetMainWorldLoc(self.gridPos)


    def Render(self,display,offset = [0,0]) -> None:
        if self.animationSize:
            #render animation here if it is one
            self.animation.play(display,[self.position[0]+offset[0],self.position[1]+offset[1]])
        else:
            display.blit(self.surface,[self.position[0]+offset[0],self.position[1]+offset[1]])


    def Render_other_colour(self,display,grid,colour = (150,150,150)):
        '''render in another colour when selected with box select'''
        self.Change_colour(colour)
        if self.animationSize:
            self.animation.play(display,grid.GetMainWorldLoc(self.gridPos),self.mouse_preview_surface)
        else:
            display.blit(self.mouse_preview_surface,grid.GetMainWorldLoc(self.gridPos))


    def Render_other_colour_position(self,display,position,colour = (150,150,150)):
        '''render in another colour when selected with box select.. use absolution position as placement'''
        self.Change_colour(colour)
        if self.animationSize:
            self.animation.play(display,position,self.mouse_preview_surface)
        else:
            display.blit(self.mouse_preview_surface,position)

    def Render_other_position(self,display,position):
        if self.animationSize:
            self.animation.play(display,position,self.mouse_preview_surface)
        else:
            display.blit(self.surface,position)
    
    def Mouse_tile_preview(self,display,grid,mousePos):
        '''Make a preview of the tile where mouse pointer is''' 
        if self.animationSize:
            self.animation.play(display,(grid.GetMainWorldLoc(mousePos)),self.mouse_preview_surface)
        else:   
            display.blit(self.surface,grid.GetMainWorldLoc(mousePos))

    def MouseHover(self,mousePos) -> bool:
        if mousePos[0] >= self.position[0] and mousePos[0] <= self.position[0] + 16:           
            if mousePos[1] >= self.position[1] and mousePos[1] <= self.position[1] + 16:
                return True
            else:
                return False
        else:
            return False
    

    def check_if_animation_image(self,surface:Surface) -> Tuple[int,int]: 
        '''get the surface size.. if its bigger than the tile size. then it must be
         either animation or ground type with 4 sides for AI to work on'''
        size = surface.get_size()
        if size[0]> GRID_SIZE[0]:
            return ((size[0]//GRID_SIZE[0])-1, (size[1]//GRID_SIZE[1])-1)
        else:
            return None

    def check_if_image_need_split(self)->list[Surface]:
        '''check if it a big image containing lots of tiles.. split it into smaller gridSize tile to use'''
        imgWidth = self.image.get_width()
        imgHeight = self.image.get_height()
        if imgWidth > GRID_SIZE[0] or imgHeight > GRID_SIZE[1]:
            images = []
            img_x_num = imgWidth//GRID_SIZE[0]
            img_y_num = imgHeight//GRID_SIZE[1]
            for x in range(img_x_num):
                for y in range(img_y_num):
                    location = Rect(x*GRID_SIZE[0],y*GRID_SIZE[1],GRID_SIZE[0],GRID_SIZE[1])
                    newImage = self.image.subsurface(location)
                    images.append(newImage)
            return images
        return None
    
    def __eq__(self,otherPos):
        '''if GridPos is same.. then its the same obj'''
        return otherPos == self.gridPos
    
    def __gt__(self,otherPos):
        return otherPos > self.gridPos
    
    def __lt__(self,otherPos):
        return otherPos < self.gridPos

    def __ge__(self,otherPos):
        return otherPos >= self.gridPos
    
    def __le__(self,otherPos):
        return otherPos <= self.gridPos