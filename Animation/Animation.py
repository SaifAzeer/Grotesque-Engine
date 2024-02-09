'''TODO -> Add Animation image details in JSON file in add function'''

''' Manages Animation..  Play, Pause ect...'''

from typing import Dict, List
from pygame import image,time,Surface
from Animation.Animation_json import Animation_json
from dataclasses import dataclass
from enum import  IntEnum

class Animations_type(IntEnum):
    '''animation type not necessary y pos of animation'''
    idle = 0
    move_right = 1
    move_left = 2
    move_up = 3
    move_down = 4

'''Animation container.. all animations from json will be containes in this'''
@dataclass
class Animation_info():
    tileSize : List[int]
    animation_number : int # amount of animation this picture contains.. move left, idle ..
    animation_order :Dict[Animations_type,int]
    animation_image : Dict[str,str]


class Animation:
    def __init__(self,imgPathMain="") -> None:
        self.imageType : int # tile or a single image
        self.imagePathMain = imgPathMain
        self.imagePath  = "" # in case image is in sub directory... add it here
        self.__frameAmount :int
        self.imageInterval = 120 # speed image is changing in seconds
        self.tileSize : List[int] = []

        self.__lastUpdate = 0
        self.__frameDisp =[0,0] # frame currently rendering
        self.__maxFrame = 0
        self.__rect = (0,0,0,0)

        self.__isPlaying = True
        self.__d_animationInfo : Dict[str,Animation_info] = {}
        
        self.AnimationJson = Animation_json()
          

    def load_from_image(self,img:str,rowNum:int,tileSize:List[int],loadImage=True):
        '''get animation without the use of json'''
        if loadImage: self.__load_image(img)
        self.tileSize = tileSize
        self.__maxFrame = rowNum


    def load_from_json(self,jsonFileName:str,name:str):
        self.__get_json(jsonFileName)
        d_info = self.__get_animation_info(name)
        return d_info
        #if d_info:
        #    animationOrder = d_info.animation_order[colName]
        #    self.load_from_image(name,2,d_info.tileSize)

    
    def load_from_img_calc_gridnumber(self,img:str,tileSize:list[int]):
        '''calculate number of row and col from big image based on tile size and load it'''
        self.__load_image(img)
        rowNum = self.image.get_width() // tileSize[0]
        self.load_from_image(img,rowNum,tileSize,False)


    def add_animation_to_json(self,name:str,tileSize:int,animationNumer:int,animationOrder:Dict[int,str]):
        self.AnimationJson.add_victim(name,tileSize,animationNumer,animationOrder)

    def change_column(self,newcol:int):
        self.__frameDisp[1] = newcol

    # newImage: replace the original image with the newImage to render temporily
    def play(self,display:Surface,position:List[int],newImg = None):
        '''loop and render animation a single long image'''     
        if self.__isPlaying == True:             
            if (time.get_ticks() - self.__lastUpdate) >= self.imageInterval:
                self.__lastUpdate = time.get_ticks()
                self.__frameDisp[0] += 1 
                if self.__frameDisp[0] > self.__maxFrame: self.__frameDisp[0] = 0  
                self.__rect = (self.__frameDisp[0] * self.tileSize[0],self.__frameDisp[1]* self.tileSize[1],self.tileSize[0],self.tileSize[1])
        if newImg:
            display.blit(newImg,position,self.__rect)
        else:    
            display.blit(self.image,position,self.__rect)


    def stop_or_start(self):
        '''stop or start animation once when called...'''
        if self.__isPlaying: 
            self.__isPlaying = False
        else: 
            self.__isPlaying = True
    
    def reset(self):
        self.__frameDisp[0] = 0


    def __load_image(self,img):
        if self.imagePathMain == "":
            self.image = image.load(img)
        else:
            self.image = image.load(self.imagePathMain+"/" + self.imagePath+ img)
    

    def __get_json(self,jsonFileName:str):
        '''get all the info from json file'''
        for key,value in self.AnimationJson.get_animation(jsonFileName).items():
            __animationInfo = Animation_info(value["tileSize"],value["animationNumber"],value["animationOrder"],value["images"])
            self.__d_animationInfo[key] = __animationInfo


    def __get_animation_info(self,name:str)->Animation_info:
        if name in self.__d_animationInfo:
            return self.__d_animationInfo[name]
        else:
            return None


    def __get_animation_order(self,name:str):
        '''animation type by column for e.g col 0 = moveLeft and col 1 = idle'''
        if name in self.__d_animationInfo:
            return self.__d_animationInfo[name].animation_order
        else:# wrong name inputted
            return None
        