from pygame import Surface,image,font
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
    def __init__(self):
        self.surface = Surface((500,50))
        self.surface.fill((150,150,150))
        self.d_dialogueContainer : dict[str,DialogueContainer] = {}
        self.length_dialogueContainer : int
        self.__ImportJson()

        self._font = font.SysFont("arial",15)
        self.startRender = False
        self.text_surface : pygame.Surface = None
        self.currentTime = time.time()

        self.current_iteration : int = -1 #multiple text iteration number
        self.showDialogueType : DialogueType = DialogueType.noDialogue
        self.showDialogueSeconds :int = 0
        self.dialogueName : str = ""

        self.firstIteraion = -1 # multipleDialogueTimer.. render first iteration then start check timer

    def Render(self,display:Surface,location:list[int],textLocation=[10,10])->None:
        display.blit(self.surface,location)
        self.surface.fill((150,150,150))
        if self.startRender and self.text_surface :
            self.surface.blit(self.text_surface,textLocation)
    
    def Update(self):
        if self.showDialogueType == DialogueType.multipleDialogueTimer:
            clock = time.time()
            self.startRender = True
            if self.firstIteraion == -1:
                self.Go_next_dialogue()
                self.currentTime = clock
                self.text_surface = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))
                self.firstIteraion = 0
            if clock - self.currentTime > self.showDialogueSeconds: # automatically go next dialogue every 2 second
                self.Go_next_dialogue()
                self.currentTime = clock
                self.text_surface = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))            
                #close the dialogue afther the end of iteration
                self.firstIteraion +=1
                if self.firstIteraion  == self.length_dialogueContainer +1 :          
                    self.Close()
        
        elif self.showDialogueType == DialogueType.multipleDialogue:
            self.text_surface = self._font.render(self.d_dialogueContainer[self.dialogueName].text[self.current_iteration],True,(10,30,1))
    
    
    def __Animate(self)->None:
        pass

    def Go_next_dialogue(self) -> int:
        if self.current_iteration < self.length_dialogueContainer:
            self.current_iteration += 1
        return self.current_iteration

    def Show_multiple_dialogue_timer(self,dialogueName:str,seconds:int = 2)->None:
        '''Use when there are multiple text that will show after selected amount of seconds'''
        #clock = time.time()
        self.showDialogueSeconds = seconds
        self.dialogueName = dialogueName
        self.showDialogueType = DialogueType.multipleDialogueTimer
        self.firstIteraion = -1
        
    def Show_single_dialogue(self,dialogueName) -> None:
        '''Use when there is only 1 dialogue text '''
        self.text_surface = self._font.render(self.d_dialogueContainer[dialogueName].text,True,(10,30,1))
        self.startRender = True
        self.showDialogueType = DialogueType.singleDialogueLine

    def Show_multiple_dialogue(self,dialogueName) ->None:
        self.text_surface = self._font.render(self.d_dialogueContainer[dialogueName].text,True,(10,30,1))
        self.startRender = True
        self.showDialogueType = DialogueType.multipleDialogue


    def Close(self) -> None:
        self.showDialogueType = DialogueType.noDialogue
        self.startRender = False
        self.current_iteration = -1

    def Skip(self)->None:
        pass

    def __ImportJson(self)->bool:
        with open("J:\PythonProg\Pygame\GrotesqueEngine\RPJ\Dialogue\Dialogue.json",'r') as f:
            d_json = jsonLoad(f)
            for key,value in d_json.items():
                dialogueContainer = DialogueContainer(key,value["img"],value["text"],value["flag"])
                self.d_dialogueContainer[key] = dialogueContainer
            self.length_dialogueContainer = len(self.d_dialogueContainer) - 1



#pygame.init()
#surface = pygame.display.set_mode((600,600))
#background = Surface((600,600))
#background.fill((0,0,32))
#dialogue = Dialogue()
#while True:
#    dialogue.Update()
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            exit()
#        if event.type == pygame.KEYDOWN:
#            if event.key == pygame.K_SPACE:
#                dialogue.Show_multiple_dialogue_timer("testDialogueMultiple")
#            elif event.key == pygame.K_RETURN:
#                dialogue.Close()
#        
#    surface.blit(background,(0,0))  
#    dialogue.Render(surface,(10,10))
#    
#    pygame.display.update()