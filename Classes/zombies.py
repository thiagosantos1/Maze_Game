# This class works to make and control a new character - player and zombie


import pygame
from tiles import Tile
from random import randint
from character import Character
from survivor import *

# control the zombies
class Zombie(Character):

  List = [] # const and static variable, then we can acess all zombies we had created

  # list of zombie images
  survivor_img =[ pygame.image.load('../Images/Enemies/zombie1.png'),
                  pygame.image.load('../Images/Enemies/zombie2.png'),
                  pygame.image.load('../Images/Enemies/zombie3.png')]

  health = 100
  zombie_dmg = 5
  zombies = [51, 68, 77,103,160,165,170,216,260,269,320, 372, 369, 441, 452, 490, 542, 569]

  def __init__(self, x, y):

    # set the image and direction for the rotation/initial
    self.direction = 'e'
    self.img = Zombie.survivor_img[randint(0, 2)]
    self.original_img = self.img
    self.speed = 4

    # set the currently heath when create a new zombie
    self.health = Zombie.health

  # create the character, and position, from inheritante
    Character.__init__(self, x, y)
    Zombie.List.append(self)
  
  # This method put a new zombie in the screen, in a random, from the positions set up on spawn_tiles, just above
  @staticmethod # 
  def spawn():
    for tile_num in Zombie.zombies:
      if tile_num not in Tile.invalidsSideWalls and tile_num not in Tile.invalidsCenterWalls:

        spawn_node = Tile.get_tile(tile_num) # get the tile that represents that tile
        Zombie(spawn_node.x, spawn_node.y) 


  @staticmethod
  def no_zombis():
    if len(Zombie.List) > 0:
      return False

    return True

  @staticmethod
  def reset():
    index=len(Zombie.List)-1

    while index>=0:
        del Zombie.List[index]
        index-=1

    # update all zombies in the screen, static because don't need class instance
    # this include draw, move, etc. Before we were using draw method and a movement method
  @staticmethod
  def update(screen, survivor):

    for zombie in Zombie.List:   

      # then draw the zombies
      screen.blit(zombie.img, (zombie.x, zombie.y))

      # make a if to calculate if the zombie and player is in the exactly same position of the tile, if zombie touch player
      # because zombie and player movies in different speed, so it will be never in the just exaclty position of the tile
      # can be somewhere of that tile
      if survivor.x % Tile.width == 0 and survivor.y % Tile.height == 0: # both of them are in the same tile
        if zombie.x % Tile.width == 0 and zombie.y % Tile.height == 0: 

          # get tile number that player is
          tn = survivor.get_number()

          # get the tiles around of the currently tile
          N = tn + -(Tile.V) # V and H and the number of tiles that we move when we move hor or vert, it define in Tile class
          S = tn +  (Tile.V)
          E = tn +  (Tile.H)
          W = tn + -(Tile.H)

          # create a list just to keep the values of tiles around the player/currently player
          NSEW = [N, S, E, W, tn]

          # then we check if zombie achive one of the tile around the player, cannot be in the same one, because player is there
          #but if it's around, it means zombie "touch the player"
          # then we reduce his healthy
          if zombie.get_number() in NSEW:
            survivor.health -= Zombie.zombie_dmg  # each time the zombie touch the player, it takes 5 emmo
            if survivor.health <1 : # player died
              survivor.isAlive = False
              # play a died/fail music
              deadSound = pygame.mixer.Sound('../Sounds/game_over.wav')
              deadSound.play()
              if survivor.health <0:
                survivor.health = 0
                        

      # remove the zombie if player killed him
      if zombie.health <= 0:
        Zombie.List.remove(zombie)

        
      if zombie.tx != None and zombie.ty != None: # Target is set

        # get the X and Y difference
        # if the result are positive, it means move left or up, and oposite
        X = zombie.x - zombie.tx
        Y = zombie.y - zombie.ty

        if X < 0: # --->
          zombie.x += zombie.speed
          zombie.rotate('e', zombie.original_img) # change the rotation everytime we move the zombie in direction 
                                                  # fo the player

        elif X > 0: # <----
          zombie.x -= zombie.speed
          zombie.rotate('w', zombie.original_img)

        if Y > 0: # up
          zombie.y -= zombie.speed
          zombie.rotate('n', zombie.original_img)

        elif Y < 0: # dopwn
          zombie.y += zombie.speed
          zombie.rotate('s', zombie.original_img)

        if X == 0 and Y == 0: # it moves until get target/next tile - then is time to check next target
          zombie.tx, zombie.ty = None, None

      # set a new target, if none
      else:
        zombie.get_next_target()

  def get_next_target(self):
    tile_num =  self.get_number()
    if self.direction == 'e':
      if tile_num +1 in Tile.invalidsSideWalls or tile_num + 1 in Tile.invalidsCenterWalls: # cannot
        # get next direction to go
        possib = [tile_num -1, tile_num - 30, tile_num +30]
        n = randint(0, 2)
        new_tile = possib[n]
        ok = False
        while not ok:
          if new_tile not in Tile.invalidsSideWalls and new_tile not in Tile.invalidsCenterWalls:
            ok = True
          else:
            n = randint(0, 2)
            new_tile = possib[n]
        self.set_target(self.get_tile_n(new_tile) )

      else:
        self.set_target(self.get_tile_n(tile_num+1) )

    if self.direction == 'w':
      if tile_num - 1 in Tile.invalidsSideWalls or tile_num - 1 in Tile.invalidsCenterWalls: # cannot
        # get next direction to go
        possib = [tile_num +1, tile_num - 30, tile_num +30]
        n = randint(0, 2)
        new_tile = possib[n]
        ok = False
        while not ok:
          if new_tile not in Tile.invalidsSideWalls and new_tile not in Tile.invalidsCenterWalls:
            ok = True
          else:
            n = randint(0, 2)
            new_tile = possib[n]
        self.set_target(self.get_tile_n(new_tile) )

      else:
        self.set_target(self.get_tile_n(tile_num-1) )

    if self.direction == 'n':
      if tile_num -30 in Tile.invalidsSideWalls or tile_num - 30 in Tile.invalidsCenterWalls: # cannot
        # get next direction to go
        possib = [tile_num -1, tile_num +1, tile_num +30]
        n = randint(0, 2)
        new_tile = possib[n]
        ok = False
        while not ok:
          if new_tile not in Tile.invalidsSideWalls and new_tile not in Tile.invalidsCenterWalls:
            ok = True
          else:
            n = randint(0, 2)
            new_tile = possib[n]
        self.set_target(self.get_tile_n(new_tile) )

      else:
        self.set_target(self.get_tile_n(tile_num-30) )

    if self.direction == 's':
      if tile_num +30 in Tile.invalidsSideWalls or tile_num + 30 in Tile.invalidsCenterWalls: # cannot
        # get next direction to go
        possib = [tile_num -1, tile_num - 30, tile_num +1]
        n = randint(0, 2)
        new_tile = possib[n]
        ok = False
        while not ok:
          if new_tile not in Tile.invalidsSideWalls and new_tile not in Tile.invalidsCenterWalls:
            ok = True
          else:
            n = randint(0, 2)
            new_tile = possib[n]
        self.set_target(self.get_tile_n(new_tile) )

      else:
        self.set_target(self.get_tile_n(tile_num+30) )

  @staticmethod 
  def zombie_sounds(total_frames, FPS):
    if total_frames % (FPS * 3) == 0 and total_frames >0:
      r = randint(0, 4)
      sounds = [pygame.mixer.Sound('../Sounds/I_will_kill_you.wav'), 
              pygame.mixer.Sound('../Sounds/zombie_attack.wav'),
              pygame.mixer.Sound('../Sounds/zombie_scream1.wav'),
              pygame.mixer.Sound('../Sounds/zombie_scream2.wav'),
              pygame.mixer.Sound('../Sounds/zombie_come_here.wav')]
      sound = sounds[ r ]
      sound.play()



  