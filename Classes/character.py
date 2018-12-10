# This class works to make and control a new character - player and zombie


import pygame
from tiles import Tile
from random import randint


class Character(pygame.Rect):

  width  = 32  # set the same size of the bricks
  height = 32

  def __init__(self, x, y):

    # variables to control the next target(tile) of each character
    self.tx, self.ty = None, None # target x position, and target y position
    # is the same line above, but now I save the number os the next tile was well
    self.targetTileNumber = None

    # create the rectangle to hold the main character
    pygame.Rect.__init__(self, x, y, Character.width, Character.height)
    

  #using __ before name(__str), it makes the method private, it works for variable as well
  def __str__(self):
    return str(self.get_number())

  # it's not static because it needs to have a zombie/Characther(object) to have a target
  # and the target is actually the next tile in the better path to get the player, or for the play, the tile you want to move
  # I use this method to move our Character smothy, not with lag
  def set_target(self, next_tile):
    if self.tx == None and self.ty == None:
        self.tx = next_tile.x
        self.ty = next_tile.y # we restart them to none after the character move

  # rotate the character(player and zombi) image for what direction we're moving
  def rotate(self, direction, original_img):

    if direction == 's':
      if self.direction != 's': # direction is where the next target of the zombie is, but then if you go all north, 
      # it's gonna reasignment/load the picture all the time, every loop. So then, whe put if self.direction !='n'
      # it's mean if we are going all north, we are gonna laod and rotate just once, in the first loop. It saves memory 
        self.direction = 's'
        # furst rotate 90, and make it south
        south = pygame.transform.rotate(original_img, 90) # CCW
        # then flip, that turns 180, making north. But we could do just with one line, with rotation of 270
        self.img = pygame.transform.flip(south, False, True)

    if direction == 'n':
      if self.direction != 'n':
        self.direction = 'n'
        # rotate the picture 90
        self.img = pygame.transform.rotate(original_img, 90) # CCW

    if direction == 'w':
      if self.direction != 'w':
        self.direction = 'w'
        # flip means just turn, 180g
        self.img = pygame.transform.flip(original_img, True, False)

    if direction == 'e':
      if self.direction != 'e':
        self.direction = 'e'
        self.img = original_img # we keep just as the original, so just load the original that points to weast


  #important
  def get_number(self):
    return ((self.x // self.width) + Tile.H) + ((self.y // self.height) * Tile.V)
    

  # it return the exactly tile the caracther is on, so basacally this one
  # and the one above works toguether
  def get_tile(self):

    return Tile.get_tile(self.get_number())

  def get_tile_n(self, number):

    return Tile.get_tile(number)

