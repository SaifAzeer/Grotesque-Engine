import pygame
from sys import exit
import time
import math


class Particle:
    def __init__(self,x,y):
        self.x :int = x
        self.y :int = y
        self.r :int =10
        self.velocity = [0,0]
        self.rad : int=0
        self.timeStart = time.time()

        self.isDone = False # time to remove instances of object to be garbage collected
        
    
    def update(self):
        if (time.time() - self.timeStart) > 0.01:
            self.timeStart = time.time()
            if self.r > 0.1: self.r -= 0.3
            else: self.isDone = True
            self.x += self.velocity[0]
            self.y += self.velocity[1]

    def event(self):
        self.velocity[0] = 2 * math.cos(self.rad)
        self.velocity[1] = 2 * math.sin(self.rad)
         
         
    def render(self):
        pygame.draw.circle(display,(10,100,200),(self.x,self.y),self.r)


l_particles = []

pygame.init()
display = pygame.display.set_mode((300,300))

surface = pygame.Surface((300,300))
surface.fill((50,50,50))



while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #_particle.event()
            rad = 0
            for i in range(36):
                rad += 0.174
                _particle = Particle(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                _particle.rad = rad
                l_particles.append(_particle)
                _particle.event()
    
    display.blit(surface,(0,0))
    for i in l_particles:
        i.update()
        i.render()
        if i.isDone:
            l_particles.remove(i)


    pygame.display.update()