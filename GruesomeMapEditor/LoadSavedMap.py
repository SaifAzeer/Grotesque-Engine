import os.path as path
from sys import path as syspath
syspath.append(path.dirname(path.abspath(path.join(__file__,"../"))))
from json import load as json_load

from Animation import Animation
from Tiles import Tiles

class LoadSavedMap:
    def __init__(self):
        self.d_jsonContainer = {}
        self.l_json_keys = ['colliders' , 'info', 'layer_1' , 'layer_2' , 'layer_3' ]
        
        self.l_map_1 = []
        self.l_map_2 = []
        self.l_map_3 = []
        self.layer_1_tiles = [] # contains tiles object
        self.layer_1_tiles = []
        self.layer_1_tiles = []
        self.colliders = []

    def load_json(self,jsonFile:str) -> bool:
        '''Open json file and check if it contains  the right structure'''
        with open(jsonFile, 'r') as f:
            d_json = json_load(f)
            correctKey = False
            for key,value in d_json.items():
                if key in self.l_json_keys:
                    correctKey = True
                else:
                    correctKey = False
                    return False
            return True

    def get_map_layer(self):
        pass

    def get_map_image(self):
        pass

    def get_colliders(self):
        pass


loadSavedMap = LoadSavedMap()
print(loadSavedMap.load_json("RPJ/Dialogue/Dialogue.Json"))