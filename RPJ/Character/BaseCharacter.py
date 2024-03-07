import os.path as path
from sys import path as sysPath
sysPath.append(path.dirname(path.abspath(path.join(__file__, "../../"))))

from pygame import image as pyImage
from pygame.math import Vector2
from RPJ.Dialogue.Dialogue import Dialogue
from RPJ.Grid import Grid
from enum import Enum
from AI.State import State
from AI.States_machine import States_machine
from Animation.Animation import Animation
from dataclasses import dataclass

@dataclass
class AnimationImageKey:
    idle_location = "idle_location"
    movement_location = "movement_location"
    idle_down  = "idle_down"
    idle_up    = "idle_up"
    idle_right = "idle_right"
    idle_left  = "idle_left"
    walk_down  = "w_down"
    walk_up    = "w_up"
    walk_right = "w_right"
    walk_left  = "w_left"


class MovementDirection(int,Enum):
    up = 1
    down = 2
    left = 3
    right =4


class BaseCharacter:
    def __init__(self, display,imageName,dialogueJson):
        # self.image = pyImage.load(image)
        self.display = display
        #self.image = Surface((50, 50))
        #_______________ Movement
        self.location: Vector2
        self.gridPosition: Vector2
        self.nextGridPosition = Vector2(0, 0)
        self.lastGridPosition = Vector2(0, 0)
        self.nextWorldPosition = Vector2(0,0)
        self.move_dir_vec: Vector2 = Vector2(0, 0)
        self.moveDirection = MovementDirection.down
        self.movementSpeed: int = 1
        self.directionVector: Vector2 = Vector2(0, 0)
        self.isMoving = False
        #_______________ Stats
        self.attackSpeed: int
        self.attackDamage: int
        self.mana: int
        # ect.....

        self.dialogue = Dialogue(dialogueJson)
        self.grid = Grid()
        self.gridSize = self.grid.gridSize
        self.d_image = {}
        # _______________ Animation
        self.animation = Animation()
        self.animation_info = self.animation.load_from_json("J:\\PythonProg\\Pygame\\GrotesqueEngine\\RPJ\\Character\\animation.json",imageName)
        self.d_animation = self.animation_info.animation_image
        self.animationNumber = self.animation_info.animation_number
        self.animation_image = self.d_animation[AnimationImageKey.idle_down]
        self.imgLoc = self.d_animation[AnimationImageKey.idle_location]
        self.animation.load_from_image(self.imgLoc+self.animation_image,self.animationNumber,[64,64])
        #_________________ State Machine
        self.state_idle = State_Idle(self)
        self.state_move = State_Movement(self)
        self.stateMachine = States_machine()
        self.stateMachine.currentState = self.state_idle
        self.stateMachine.currentState.Start()

        self.load_image()
    # ----------------------------------------MOVEMENT
    def SetGridPosition(self, position):
        '''Initial position of character'''
        self.location = self.grid.GetWorldLoc(position)
        self.gridPosition = position
        self.nextGridPosition = position

    def set_new_movement_position(self):
        self.nextGridPosition = self.gridPosition + self.move_dir_vec
        self.nextWorldPosition = self.grid.GetWorldLoc(self.nextGridPosition)
        self.lastGridPosition = self.gridPosition

    def MoveRight(self):
        if self.move_dir_vec  == Vector2(0,0):
            self.move_dir_vec = Vector2(1, 0)
            self.isMoving = True
            self.moveDirection = MovementDirection.right
            self.set_new_movement_position()

    def MoveLeft(self):
        if self.move_dir_vec  == Vector2(0,0):
            self.move_dir_vec = Vector2(-1, 0)
            self.isMoving = True
            self.moveDirection = MovementDirection.left
            self.set_new_movement_position()

    def moveUp(self):
        if self.move_dir_vec  == Vector2(0,0):
            self.move_dir_vec = Vector2(0, -1)
            self.isMoving = True
            self.moveDirection = MovementDirection.up
            self.set_new_movement_position()

    def moveDown(self):
        if self.move_dir_vec  == Vector2(0,0):
            self.move_dir_vec = Vector2(0, 1)
            self.isMoving = True
            self.moveDirection = MovementDirection.down
            self.set_new_movement_position()

    def keyRelease(self):
        self.isMoving = False

    #------------------------------------------ANIMATION
    def reloadAnimation(self):
        self.animation.load_from_image(self.imgLoc+self.animation_image,self.animationNumber,[64,64])

    def load_image(self):
        '''Get animations name e.g(move left, attack left) from json and load its image in items'''
        for key,value in self.d_animation.items():
            if key == AnimationImageKey.idle_location:
                continue
            if key == AnimationImageKey.movement_location:
                continue
            self.d_image[key] =pyImage.load( self.d_animation[AnimationImageKey.idle_location]+ value)
            
        print(self.d_image)

    def reload_animation_image_location(self,location):
        self.imgLoc = self.d_animation[location]

    def Update(self) -> None:
        self.stateMachine.update()
        self.dialogue.Update()

    def Render(self, display) -> None:
        #self.image.fill((100, 200, 100))
        self.animation.play(self.display,self.location)  
        self.dialogue.Render(display)
        #display.blit(self.image, self.location)
   


# -----------------------------------------------------------------------------
# FSM STATES
class State_Idle(State):
    def __init__(self, character):
        self.character = character

    def Start(self):
        print("starting idle state")
        
        if self.character.moveDirection == MovementDirection.up:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.idle_up]
        if self.character.moveDirection == MovementDirection.down:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.idle_down]
        if self.character.moveDirection == MovementDirection.left:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.idle_left]
        if self.character.moveDirection == MovementDirection.right:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.idle_right]

        self.character.reloadAnimation()

    def Execute(self):
        if self.character.isMoving:
            self.character.reload_animation_image_location(AnimationImageKey.movement_location)
            self.character.stateMachine.change_state(self.character.state_move)
               

    def Exit(self):
        print("exiting Idle State")
        if self.character.moveDirection == MovementDirection.up:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_up]
        if self.character.moveDirection == MovementDirection.down:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_down]
        if self.character.moveDirection == MovementDirection.left:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_left]
        if self.character.moveDirection == MovementDirection.right:
            self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_right]
        self.character.reloadAnimation()

class State_Movement(State):
    def __init__(self, character):
        self.character = character

    def Start(self):
        print("starting movement State")
        

    def Execute(self):
        if self.character.location != self.character.nextWorldPosition:
            delta = self.character.nextWorldPosition - self.character.location
            if delta.length() > (self.character.move_dir_vec * self.character.movementSpeed).length():
                self.character.location += self.character.move_dir_vec * self.character.movementSpeed
            else: # character almost or reached destination and movement button pressed
                self.character.location = self.character.nextWorldPosition
                self.character.nextGridPosition = self.character.gridPosition
                self.character.gridPosition = self.character.gridPosition + self.character.move_dir_vec
                self.character.move_dir_vec = Vector2(0,0)
                #change direction when previous animation was moving animation
                if self.character.moveDirection == MovementDirection.up:
                    self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_up]
                if self.character.moveDirection == MovementDirection.down:
                    self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_down]
                if self.character.moveDirection == MovementDirection.left:
                    self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_left]
                if self.character.moveDirection == MovementDirection.right:
                    self.character.animation_image = self.character.d_animation[AnimationImageKey.walk_right]

                self.character.reloadAnimation()


        else: # if character reached destination
            if self.character.move_dir_vec == Vector2(0,0): # character stoped moving
                self.character.reload_animation_image_location(AnimationImageKey.idle_location)
                self.character.stateMachine.change_state(self.character.state_idle)


    def Exit(self):
        pass


class State_Attack(State):
    def __init__(self, character):
        super.__init__()
        self.character = character
