

import pygame
import random
import sys
from time import sleep
from tiles import Tile 
from interaction import interaction
from bullet import *
from survivor import *
from zombies import *
import DisplayText 

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GRAY = [153, 153, 153]
BEGE = [222,184,135]
GREEN = [0,255,0]
RED = [255,0,0]
WIDTH = 960
HEiGHT = 640


pygame.init()
pygame.mixer.pre_init()
pygame.mixer.set_num_channels(3)
pygame.font.init() # initialize font class in pygame
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEiGHT)) # 32 x 32  size of tiles
pygame.display.set_caption("Maze Game")

# set up all the tiles
Tile.pre_init(screen)
survivor = Survivor(32, 32*6)

clock = pygame.time.Clock()
FPS = 24 # if we increase this number, the speed of character will be lower
total_frames = 0
total_frames_welcome = 0
pygame.mouse.set_visible(True)
# load and play background welcome page sound again
pygame.mixer.music.load('../Sounds/htd.wav')
pygame.mixer.music.play(-1) # -1 put to loop the music forever

# Loop until the user clicks the close button.
done = False
Zombie.spawn()
while True:
  milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
  clock_elapsed_seconds = milliseconds / 1000.0 # seconds passed since last frame (float)
  Tile.draw_tiles(screen)

  if survivor.isAlive:
    # interaction method from Interaction class. It control all events from the game
    interaction(screen, survivor)

    # move to the new direction, and also draw the player in the screen
    survivor.update(screen,clock_elapsed_seconds)

    # check if there's colision of any bullet, all the time
    Bullet.update(screen,survivor)

    Zombie.update(screen, survivor)
    Zombie.zombie_sounds(total_frames, FPS)

    # display the healthy of the player in the screen
    DisplayText.text_to_screen(screen, 'Health: {0}'.format(survivor.health), 0,0,16, WHITE)

    # display the player score
    DisplayText.text_to_screen(screen, 'Score: {0}'.format(survivor.score), 32*11,0,16, WHITE)

    if Zombie.no_zombis():
      Zombie.reset()
      Zombie.spawn()

  else:
    for event in pygame.event.get():

      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

  total_frames += 1

  pygame.display.flip()
  clock.tick(FPS)

pygame.quit()





