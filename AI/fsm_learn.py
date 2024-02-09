from State import State
from States_machine import States_machine,_stateMachine
import pygame
from sys import exit

class Character:
    def __init__(self):
        self.thirst = 0
        self.state_walk = Walk(self)
        self.state_drink = Drink(self)

class Walk(State):
    def __init__(self,character):
        self.stateName = "walk"
        self.thirst = 0
        self.character = character
    
    def Start(self):
        self.thirst = 0
        print("walking again")

    def Execute(self):
        self.thirst +=1
        if self.thirst == 3:
            _stateMachine.change_state(self.character.state_drink)
        
    def Exit(self):
        print("exiting Walk ")


class Drink(State):
    def __init__(self,character):
        self.stateName = "drink"
        self.thirst = 3
        self.character = character

    def Start(self):
        self.thirst = 3
        print("starting dring")

    def Execute(self):
        self.thirst -= 1
        if self.thirst <= 0:
            _stateMachine.change_state(self.character.state_walk)

    def Exit(self):
        print("stoped drinking")



character = Character()
_stateMachine.currentState = character.state_walk
pygame.init()
display = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

while True:
    clock.tick(1)
    _stateMachine.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
   

