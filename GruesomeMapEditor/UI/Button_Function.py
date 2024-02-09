from typing import List
from os import walk,getcwd
from pygame import mouse
from Data.Constant import ROOTPOSITION
import pathlib


class Button_Function:
    '''Add functions to be used by all buttons here...'''
    def __init__(self):
        pass

    def open_file_explorer(self) :
        '''open file explorer and return path and other files as string'''       
        #folder = 'J:/PythonProg/Pygame/GrotesqueEngine/GruesomeMapEditor/UI'
        #sub_folders =next(walk('.'))[1]
        l_folders = []
        for i in pathlib.Path(ROOTPOSITION).iterdir():
            if i.is_dir():
                l_folders.append(i.name)
                
        return l_folders
        

    def Change_folder_explorer(self,path) -> List[str]:
        '''change folder when click in file explorer folder buttons'''       
        finalPath =""
        for i in path:
            finalPath = finalPath + "\\"+i
        #print(ROOTPOSITION+finalPath)
        l_folders = []
        for i in pathlib.Path(ROOTPOSITION+finalPath).iterdir():
            if i.is_dir():
                l_folders.append(i.name)
        #print(next(walk(getcwd()+"\\"+finalPath))[1])
        return l_folders
        #return next(walk(getcwd()+"\\"+finalPath))[1]
    
