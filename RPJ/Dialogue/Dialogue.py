# textSurfaceType : general,personal

from pygame import Surface,image,font,transform
import time
import pygame
from sys import exit
from json import load as jsonLoad
from dataclasses import dataclass
from enum import Enum

@dataclass
class DialogueContainer():
    name:str
    img:str
    text:list[str]
    flag:str

class DialogueType(int,Enum):
    singleDialogueLine = 0
    multipleDialogueTimer = 1 # when npc is talking in background
    multipleDialogue = 2
    noDialogue = 3 # use when there is nothing to show
    


class Dialogue:
    def __init__(self,jsonFile:str):
        self.d_dialogueContainer : dict[str,DialogueContainer] = {}
        self.length_dialogueContainer : int
        self.d_image  = {} #str-image
        self.location : list[int] # location of dialogue background image
        self.textLocation :list[int] # location of text calculated to be in the middle of background image
        self.surfaceLocation :list[int] # location of dialogue background image
        self.__ImportJson(jsonFile)

        self._font = font.SysFont("arial",15)
        self.startRender = False
        self.text_dialogue : pygame.Surface = None
        self.currentTime = time.time()

        self.current_iteration : int = -1 #multiple text iteration number
        self.showDialogueType : DialogueType = DialogueType.noDialogue
        self.showDialogueSeconds :int = 0
        self.dialogueName : str = ""

        self.firstIteraion = -1 # multipleDialogueTimer.. render first iteration then start check timer
        self.is_next_dialogue : bool = False # whether or not we pressed space bar.. loop once in update

    def Render(self,display:Surface,)->None:
        if self.startRender and self.text_dialogue :
            display.blit(self.text_surface,self.location)
            display.blit(self.text_dialogue,self.textLocation)
    
    def Update(self):
        if self.showDialogueType == DialogueType.multipleDialogueTimer:
            clock = time.time()
            self.startRender = True
            if self.firstIteraion == -1:
                self.Go_next_dialogue()
                self.currentTime = clock
                self.text_dialogue = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))
                self.firstIteraion = 0
            if clock - self.currentTime > self.showDialogueSeconds: # automatically go next dialogue every 2 second
                self.Go_next_dialogue()
                self.currentTime = clock
                self.text_dialogue = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))            
                #close the dialogue afther the end of iteration
                self.firstIteraion +=1
                if self.firstIteraion  == self.length_dialogueContainer +1 :          
                    self.Close()
        
        elif self.showDialogueType == DialogueType.multipleDialogue:
            if self.is_next_dialogue == False:
                return
            self.Go_next_dialogue()
            self.text_dialogue = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))
            self.firstIteraion +=1
            self.is_next_dialogue = False
            if self.firstIteraion  == self.length_dialogueContainer +1 :          
               self.Close()



    def get_text_location(self):
        width = self.text_surface.get_width() / 2
        height = self.text_surface.get_height() // 4
        self.textLocation = [self.location[0] + 10,self.location[1] + height]

    def __Animate(self)->None:
        pass

    def Go_next_dialogue(self) -> int:
        if self.current_iteration < self.length_dialogueContainer:
            self.current_iteration += 1
        return self.current_iteration

    def Show_multiple_dialogue_timer(self,dialogueName:str,seconds:int = 2,surfType = "general",size = [300,100])->None:
        '''Use when there are multiple text that will show after selected amount of seconds'''    
        self.text_surface = self.d_image[surfType]
        self.text_surface = transform.scale(self.text_surface,size)
        self.get_text_location()
        #clock = time.time()
        self.showDialogueSeconds = seconds
        self.dialogueName = dialogueName
        self.showDialogueType = DialogueType.multipleDialogueTimer
        self.firstIteraion = -1
        
    def Show_single_dialogue(self,dialogueName,surfType = "general",size = [300,100]) -> None:
        '''Use when there is only 1 dialogue text '''
        self.text_surface = self.d_image[surfType]
        self.text_surface = transform.scale(self.text_surface,size)
        self.get_text_location()
        self.text_dialogue = self._font.render(self.d_dialogueContainer[dialogueName].text,True,(10,30,1))
        self.startRender = True
        self.showDialogueType = DialogueType.singleDialogueLine

    def Show_multiple_dialogue(self,dialogueName,surfType = "general",size = [300,100]) ->None:
        self.text_surface = self.d_image[surfType]
        self.text_surface = transform.scale(self.text_surface,size)
        self.get_text_location()
        self.dialogueName = dialogueName
        #self.text_dialogue = self._font.render(self.d_dialogueContainer[dialogueName].text,True,(10,30,1))
        self.startRender = True
        self.is_next_dialogue = True
        self.showDialogueType = DialogueType.multipleDialogue

    def Close(self) -> None:
        self.showDialogueType = DialogueType.noDialogue
        self.startRender = False
        self.current_iteration = -1

    def Skip(self)->None:
        pass

    def __ImportJson(self,jsonFile:str)->bool:
        with open(jsonFile,'r') as f:
            d_json = jsonLoad(f)
            for key,value in d_json.items():
                if key == "imageType": # find image and add to dict
                    self.d_image["general"] = image.load(value["general"])
                    if value["personal"] != "":
                        self.d_image["personal"] = image.load(value["personal]"])
                    continue
                    
                dialogueContainer = DialogueContainer(key,value["imgType"],value["text"],value["flag"])
                self.d_dialogueContainer[key] = dialogueContainer
            self.length_dialogueContainer = len(self.d_dialogueContainer) - 1 # for myltiple dialogue timer


#----------------------------------------------------------------
# TESTING
#----------------------------------------------------------------
pygame.init()
surface = pygame.display.set_mode((600,600))
background = Surface((600,600))
background.fill((0,0,32))
dialogue = Dialogue("J:\PythonProg\Pygame\GrotesqueEngine\RPJ\Dialogue\Dialogue.json")
dialogue.location = [100,130]
while True:
    dialogue.Update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dialogue.Show_multiple_dialogue("testDialogueMultiple")
            elif event.key == pygame.K_RETURN:
                dialogue.Close()
        
    surface.blit(background,(0,0))  
    dialogue.Render(surface)
    
    pygame.display.update()