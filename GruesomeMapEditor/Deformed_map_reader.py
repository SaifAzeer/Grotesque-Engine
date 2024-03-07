from optparse import Values
import os.path as path
from sys import path as sysPath
sysPath.append(path.dirname(path.abspath(path.join(__file__ ,"../../"))))
from pygame import image, Surface,SRCALPHA
import json
#from os import path
#print(path.dirname(path.realpath(__file__)))
from Animation import Animation
from dataclasses import dataclass

@dataclass
class Colliders_surface:
	name :  str
	surface : Surface
	grid_position : list[int]

class Deformed_map_reader:
	def __init__(self,imageLoc):
		'''1 param -> main loc of assets'''
		self.d_json = {}
		self.imageLoc = imageLoc
		
		self.mapImages = {} #put all images of all 3 layers of map here

		self.animation = Animation.Animation(self.imageLoc)
		self.d_animations = {} # dict of all animations on map

	def open_map(self,map) -> None:
		'''map -> .json file'''
		if self.read_json(self.imageLoc + "\\"+ map):
			self.gridNumber = (self.d_json["info"]["grid_number"][0],self.d_json["info"]["grid_number"][1])
			self.gridSize = (self.d_json["info"]["grid_size"][0],self.d_json["info"]["grid_size"][1])
			self.displaySize = (self.d_json["info"]["grid_number"][0] *self.d_json["info"]["grid_size"][0],self.d_json["info"]["grid_number"][1] *self.d_json["info"]["grid_size"][1])
	
		# get dict of images in all layers and concat them to self.mapImages
		mapImages = dict(self.get_image_1()) 
		for d in (self.get_image_2(),self.get_image_3()) : 
			mapImages.update(d)

		self.mapImages = self.import_image(mapImages)
		
		self.map_layer_1 = self.get_map_layer_1()
		self.map_layer_2 = self.get_map_layer_2()
		self.map_layer_3 = self.get_map_layer_3()
		self.map_collider = self.get_colliders()

		self.map_image_1 = self.get_image_1()
		self.map_image_2 = self.get_image_2()
		self.map_image_3 = self.get_image_3()

		self.check_image_if_animation()

	def save_image(self,display):
		image.save(display,"test.png")

	def read_json(self,fileName) -> bool:
		with open(fileName, 'r') as f:
			self.d_json = json.load(f)
			return True
		return False
	
	def instantiate_collider(self) -> list[Colliders_surface]:
		'''organise colliders info from json into a dataclass'''
		l_colliders = []
		for k,v in self.map_collider.items():
			for i in v:
				c_s = Colliders_surface(k,Surface((i[1],i[2])),i[0])
				l_colliders.append(c_s)
		return l_colliders  

	def display_collider(self,display) -> None:
		l_colliders = self.instantiate_collider()
		for i in l_colliders:
			i.surface.fill((100,100,100))
			display.blit(i.surface,(i.grid_position[0]*self.gridSize[0],i.grid_position[1]*self.gridSize[1]))


	#TODO -> add check if animation here and animate where needed
	def render_map_from_tile(self,display)  -> None:
		'''blit all 3 layers 1 after the other'''
		for i in range(self.gridNumber[1]):
			for j in range(self.gridNumber[0]):
				#check if the tile num in maplayer(2d list) exist in out map.. else it wont render
				if self.map_layer_1[i][j] in self.mapImages:	
					display.blit(self.mapImages[self.map_layer_1[i][j]],(j*self.gridSize[0],i*self.gridSize[1]))

					#if self.d_json["layer_1"]["images"].get(str(self.map_layer_1[i][j])) in self.d_animations:
					#	self.d_animations[self.d_json["layer_1"]["images"].get(str(self.map_layer_1[i][j]))].play(display,(j*self.gridSize[0],i*self.gridSize[1]))
					if self.map_image_1[str(self.map_layer_1[i][j])]  in self.d_animations:
						self.d_animations[self.map_image_1[str(self.map_layer_1[i][j])] ].play(display,(j*self.gridSize[0],i*self.gridSize[1]))

				if self.map_layer_2[i][j] in self.mapImages:
					display.blit(self.mapImages[self.map_layer_2[i][j]],(j*self.gridSize[0],i*self.gridSize[1]))
					if self.map_image_2[str(self.map_layer_2[i][j])]  in self.d_animations:
						self.d_animations[self.map_image_2[str(self.map_layer_2[i][j])] ].play(display,(j*self.gridSize[0],i*self.gridSize[1]))
				
				if self.map_layer_3[i][j] in self.mapImages:
					display.blit(self.mapImages[self.map_layer_3[i][j]],(j*self.gridSize[0],i*self.gridSize[1]))
					if self.map_image_3[str(self.map_layer_3[i][j])]  in self.d_animations:
						self.d_animations[self.map_image_3[str(self.map_layer_3[i][j])] ].play(display,(j*self.gridSize[0],i*self.gridSize[1]))
		self.display_collider(display)

	# check if surface is bigger than tile to see if its an animation
	# add in dict with image as key.. check if image is in dict before render
	def check_image_if_animation(self) -> None:
		for key,value in self.get_image_1().items():
			if value[-8:] == "anim.png":
				animation = Animation.Animation(self.imageLoc)
				animation.load_from_img_calc_gridnumber(self.d_json["layer_1"]["images"].get(key),self.gridSize)
				self.d_animations[value] = animation

		for key,value in self.get_image_2().items():
			if value[-8:] == "anim.png":
				animation = Animation.Animation(self.imageLoc)
				animation.load_from_img_calc_gridnumber(self.d_json["layer_2"]["images"].get(key),self.gridSize)
				self.d_animations[value] = animation

		for key,value in self.get_image_3().items():
			if value[-8:] == "anim.png":
				animation = Animation.Animation(self.imageLoc)
				animation.load_from_img_calc_gridnumber(self.d_json["layer_3"]["images"].get(key),self.gridSize)
				self.d_animations[value] = animation


	def import_image(self,dict_image) -> dict:
		''' get image from json file with its key.. and turn it to surface for blitting'''
		tiles = {}
		for key ,value in dict_image.items():		
			surface = Surface(self.gridSize,SRCALPHA).convert_alpha()
			image = image.load(value)
			surface.blit(image,(0,0))
			tiles[int(key)] = surface
		return tiles
		

	def get_map_layer_1(self):
		return self.d_json["layer_1"]["map"]

	def get_map_layer_2(self):
		return self.d_json["layer_2"]["map"]

	def get_map_layer_3(self):
		return self.d_json["layer_3"]["map"]
	
	def get_image_1(self):
		return self.d_json["layer_1"]["images"]

	def get_image_2(self):
		return self.d_json["layer_2"]["images"]

	def get_image_3(self):
		return self.d_json["layer_3"]["images"]
	
	def get_colliders(self):
		return self.d_json["colliders"]["collider_rect"]