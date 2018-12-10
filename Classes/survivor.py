# This class works to make and control a new character - player and zombie


import pygame
from tiles import Tile
from random import randint
from character import Character
from bullet import *


# main character class
class Survivor(Character):

  # list of player images with differents guns
  survivor_img = pygame.image.load('../Images/Survivor/survivor_automatic.png')

  

  def __init__(self, x, y):

    # give heathy/life for our player
    self.health = 100
    self.score = 0 # keep tracking the player score
    self.isAlive = True  # player start alive, and if his helthy gets bellow 0, he dies
    self.zombieScore = 5 # how many score the play win when he kill a zombie
    
    self.speed = 16 # speed that player walk


    self.direction = 'e' # save the direction we're goint to, we start with west, and we change it and we rotate
    self.img = Survivor.survivor_img

    # have save the future tile number(target/next tile to move)
    self.future_tile_number = None

    Character.__init__(self, x, y)


  # function to draw and update the position(move) of the player in the scrren
  def update(self, screen, clock_elapsed):

    self.img = Survivor.survivor_img
    rotateDirection = self.direction
    self.direction = ''
    self.rotate(rotateDirection)

    if self.tx != None and self.ty != None: 
      self.movement(clock_elapsed)
      # have to change here, instead get where we are, get where we are going to
      targetTileNumber = ((self.x // self.width) + Tile.H) + ((self.y // self.height) * Tile.V)
          
    screen.blit(self.img, (self.x, self.y))
        

  def rotate(self, direction):

    # first, load the survivor picture with currently gun
    self.img = Survivor.survivor_img

    if direction == 's':
      if self.direction != 's': 
        self.direction = 's'
        south = pygame.transform.rotate(self.img, 90)
        self.img = pygame.transform.flip(south, False, True)

    if direction == 'n':
      if self.direction != 'n':
        self.direction = 'n'
        self.img = pygame.transform.rotate(self.img, 90) # CCW

    if direction == 'e':
      if self.direction != 'e':
        self.direction = 'e'
        self.img = Survivor.survivor_img # original image already points to east

    if direction == 'w':
      if self.direction != 'w':
        self.direction = 'w'
        self.img = pygame.transform.flip(self.img, True, False)

  
  def movement(self, clock_elapsed):

    if self.tx != None and self.ty != None: # Target is set

      X = self.x - self.tx
      Y = self.y - self.ty

      if X < 0: # --->
        self.x += self.speed #* clock_elapsed
      elif X > 0: # <----
        self.x -= self.speed #* clock_elapsed

      if Y > 0: # up
        self.y -= self.speed #* clock_elapsed
      elif Y < 0: # dopwn
        self.y += self.speed #* clock_elapsed

      if X == 0 and Y == 0:
        self.tx, self.ty = None, None
