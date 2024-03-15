import os.path as path
from sys import path as sysPath
sysPath.append(path.dirname(path.abspath(path.join(__file__, "../"))))

from AI.State import State
from AI.States_machine import States_machine
#get/set current map/ ect...
#start/track quest..
#pause/unpause game
#get game current time.. day/night
#video animation...

#global state   -> pause/unpause game
#               -> track time..

    

class Grotesque_controller:
    def __init__(self):
        self.isPaused = False
        self.current_map = None

    
    def update(self):
        pass

    def change_map(self) -> None:
        pass


class State_main(State):
    ''' run in global state'''
    def __init__(self,controller):
        self.controller = controller

    def Start(self):
        return super().Start()
    
    def Execute(self):
        self.controller.update()
    
    def Exit(self):
        return super().Exit()
    

    