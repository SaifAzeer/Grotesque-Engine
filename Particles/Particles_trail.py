import random
import pygame
from time import time
import math

class Particles_base(object):
    def __init__(self):
        self.position = [0,0]
        self.velocity = [0,0]
        self.target = [0,0]
        self.r = 10
        self.colour = (150,150,150)
        self.timeStart = time()
        self.isDraw = True

    def render(self):
        if self.isDraw:
            pygame.draw.circle(display,self.colour,(self.position[0],self.position[1]),self.r)

#-----------------------------------------------------------------------------------
class Player(Particles_base):
    def __init__(self):
        super(Player,self).__init__()
        self.colour = (200,100,20)
        self.initialSpeed = [0,0]
        self.movementSpeed = [0,0]


    def update(self):
        self.position = pygame.mouse.get_pos()
        if (time() - self.timeStart) >0.1:
            self.initialSpeed = pygame.mouse.get_pos()
            self.timeStart = time()
        self.movementSpeed[0] = self.position[0] - self.initialSpeed[0]
        self.movementSpeed[1] = self.position[1] - self.initialSpeed[1]
        

#-------------------------------------------------------------

class Particles(Particles_base):
    def __init__(self,player):
        super(Particles,self).__init__()
        self.timer = 10
        self.player = player
        self.velocity[0] = self.player.movementSpeed[0]
        self.velocity[1] = self.player.movementSpeed[1]
        self.r = 6
        self.decelerationSpeed = 2
        self.maxSpeed  = 4
        self.rad = 2

    def update(self):
        if (time() - self.timeStart) >0.01:
            
            #set max speed 
            if self.velocity[0] > self.maxSpeed: self.velocity[0] = self.maxSpeed
            elif self.velocity[0] < -self.maxSpeed: self.velocity[0] = -self.maxSpeed
            if self.velocity[1] >self.maxSpeed: self.velocity[1] = self.maxSpeed
            elif self.velocity[1] < -self.maxSpeed: self.velocity[1] = -self.maxSpeed

            self.position[0] += self.velocity[0] * math.cos(random.uniform(-self.rad,self.rad))
            self.position[1] += self.velocity[1] * math.sin(random.uniform(-self.rad,self.rad))
            
            # add deceleration 
            if self.velocity[0] < 0: self.velocity[0] += self.decelerationSpeed
            elif self.velocity[0] > 0: self.velocity[1] -= self.decelerationSpeed
            if self.velocity[1] > 0: self.velocity[1] -= self.decelerationSpeed
            elif self.velocity[1] < 0: self.velocity[1] += self.decelerationSpeed
                
            self.r -= 0.1
            self.timer -=1 
            if self.timer <=0:
                #reset particles location
                self.position[0] = self.player.position[0]
                self.position[1] = self.player.position[1]
                #reset velocity
                self.velocity[0] = self.player.movementSpeed[0] *-1
                self.velocity[1] = self.player.movementSpeed[1] *-1
                
                self.r = 6
                self.timer = random.randint(6,15)
                
                
            self.timeStart = time()
            

#=================================================================================

initTimer = time()
player = Player()
l_particles = []
for i in range(30):
    particles = Particles(player) 
    l_particles.append(particles)

pygame.init()
display = pygame.display.set_mode((800,800))

surface = pygame.Surface((800,800))
surface.fill((50,50,50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    display.blit(surface,(0,0))

    player.update()

    for i in l_particles:
        i.update()
        i.render()
  
    player.render()
    pygame.display.update()