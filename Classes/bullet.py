# This class works to make and control a new character - player and zombie


import pygame
from tiles import Tile
from random import randint
from zombies import Zombie
from survivor import *

class Bullet(pygame.Rect):
    
  width, height = 7, 10
  List = []

  img = pygame.image.load('../Images/Survivor/bullet.png') 
  
  gun_dmg = (Zombie.health / 6) + 1 

           
  def __init__(self, x, y, velx, vely, direction):

    self.gun_sounds = pygame.mixer.Sound('../Sounds/automatic_fire.wav')

    try:
      dx = abs(Bullet.List[-1].x - x)
      dy = abs(Bullet.List[-1].y - y)
      if dx < 50 and dy < 50:
        return     

    except: pass

    try:
      sound = self.gun_sounds
      vol = sound.get_volume()
      sound.set_volume(min(vol*1,0.20))
      sound.play()    
    except: pass
       

    self.direction = direction
    self.velx, self.vely = velx, vely

    # make the rotate of the bullet, just like we did with the character rotate
    if direction == 'n':                        # it get the path of the bullet in the dictio, with key = type
      south = pygame.transform.rotate(Bullet.img, 90) # CCW
      self.img = pygame.transform.flip(south, False, True)

    if direction == 's':
      self.img = pygame.transform.rotate(Bullet.img, 90) # CCW

    if direction == 'e':
      self.img = pygame.transform.flip(Bullet.img, True, False)

    if direction == 'w':
      self.img = Bullet.img

    # create the rectangle to hold the image
    pygame.Rect.__init__(self, x, y, Bullet.width, Bullet.height)
    # add the bullet to the list
    Bullet.List.append(self)


  # check if the bullet go out of the screen, and remove it
  def offscreen(self, screen):

    if self.x < 0:
      return True
    elif self.y < 0:
      return True
    elif self.x + self.width > screen.get_width(): # -->
      return True
    elif self.y + self.height > screen.get_height():
      return True
    
    return False

  # method to draw, update, and check collision
  @staticmethod
  def update(screen,survivor):

    # check bullet by bullet
    for bullet in Bullet.List:

      # first move it
      bullet.x += bullet.velx
      bullet.y += bullet.vely

      # draw it
      screen.blit(bullet.img, (bullet.x , bullet.y))

      # check if it's off of screen, if it's, remove it from the list, and jump for the next loop(buller)
      if bullet.offscreen(screen):
        Bullet.List.remove(bullet)
        continue # jump for next interaction loop
            
      # check zombie by zombie if that bullet hit one of the zombies
      for zombie in Zombie.List:
        # if the bullet hit a zombie
        if bullet.colliderect(zombie): # method that calculate if there's colision between rectangles
            
          # remove ammo from the zombie, depending of each gum
          zombie.health -= Bullet.gun_dmg      # gum demage
          # if player killed zombie, his score is increase
          if zombie.health <= 0 :     
            survivor.score+= survivor.zombieScore  # increase score for user, when he kill a zombie

          # remove the buller, because it can heat just one zombie, and break the for zombie
          Bullet.List.remove(bullet)
          break
                

      # check if bullet colides with any tile not walkable(wall)
      for tile in Tile.List:
          
        if bullet.colliderect(tile) and not(tile.walkable):
          try:
            # then remove that tile
            Bullet.List.remove(bullet)
          except:
            break # if bullet cannot be removed, then GTFO


