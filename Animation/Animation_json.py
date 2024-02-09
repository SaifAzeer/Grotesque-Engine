'''Load Animation from json..  organise it in a dictionary and list
    Add and remove element from json Animation file
'''
from typing import List,Dict
import json

class Animation_json:
    def __init__(self) -> None:
        self.__animationNames : List[str] = []
        self.__tileSize : List[int] = []
        self.__animationNumber : List[int] = [] # amount of animation contained .. e.g idle, moveLeft,moveRight
        #self.__animationOrder : Dict[int,str] = {} # int : frameAmount , " string": left right idle ect....
        self.__l_animationOrders :List[Dict[int,str]]= [] # list of animation order
        self.__l_images : List[Dict[str,str]]= []
        #self.__animationsDetails = self.load_json()

    def get_animation(self,jsonFileName:str) -> dict:
        '''get raw animation details frop json file'''
        self.__animationsDetails = self.load_json(jsonFileName)
        return self.__animationsDetails

    def upload_json(self):
        to_dump = {}
        for i in range(len(self.__animationNames)):

            to_dump[self.__animationNames[i]]={
                    "tileSize" : self.__tileSize[i],
                    "animationNumber" : self.__animationNumber[i],
                    "animationOrder"  : self.__l_animationOrders[i]
                    }
                            
        with open("Animation.json" , "w") as f:           
            json.dump(to_dump, f,  sort_keys=True, indent=4)

    def load_json(self,jsonFileName:str) -> dict:
        """get info from json and add it to appripriate dict"""
        with open(jsonFileName, 'r') as f:
            d_json = json.load(f)
            # get all value from json.. so that if we cant to just add new to json file
            # we just add to it
            for key,value in d_json.items():
                self.__animationNames.append(key)
                self.__tileSize.append(value["tileSize"])
                self.__animationNumber.append(value["animationNumber"])
                self.__l_animationOrders.append(value["animationOrder"])
                self.__l_images.append(value["images"])
            return d_json

    def add_victim(self,name:str,tileSize:List[int],animationNumer:int,animationOrder:Dict[int,str]):
        '''add animation'''
        if name not in self.__animationNames:
            self.__animationNames.append(name)
            self.__tileSize.append(tileSize)
            self.__animationNumber.append(animationNumer)
            self.__l_animationOrders.append(animationOrder)


    def eliminate_victim(self,name):
        '''remove animation from json file'''
        if name in self.__animationNames:
            index = self.__animationNames.index(name)
            self.__animationNames.pop(index)
            self.__tileSize.pop(index)
            self.__animationNumber.pop(index)
            self.__l_animationOrders.pop(index)

    def mass_murder(self):
        '''clear all the entry in json file.. use to add new once to remove dupplicate or useless'''    
        self.__animationNames = []
        self.__tileSize = []
        self.__animationNumber = []
        self.__l_animationOrders = []