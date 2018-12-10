import pygame 
from random import randint

# each tile is gonna "be" a rectangle
class Tile(pygame.Rect):
  # list of all tiles in the game, include wall and walkable tiles
  List = []
  width, height = 0,0 # each tile is gonna be a rectangle of 32x32
  total_tiles = 1
  H, V = 1, 30 # use to control the position of the carachter


  # list of invalid titles(Walls)
  invalidsSideWalls = [1,2,3,4,5,6,7,8,9,10,11,12,13,14, 15,16,17,18,19,20,21,22,
        23,24,25,26,27,28,29,30,
        31,60,61,90,91,120,121,150,151,180,181,210,211,240,241,
        270,271,300,301,330,331,360,361,390,391,420,421,450,
        451,480,481,510,511,540,541,570,
        571,572,573,574,575,576,577,578,579,580,581,582,
        583,584,585,586,587,588,589,590,591,592,593,594,595,
        596,597,598,599, 600
        ]

  invalidsCenterWalls= [ 34,36,37,38,40,43,44,50,53,56, # line of walls 2
              74,75,76,78,79,83,87,  # line 3
              94,101,102, # line 4
              124, 126,127,131,132,134,135,136, 138,139,140,141,142,143,145,146,147,148, # line 5
              152,153,157,159,164,169,177, # line 6
              187,189,190,191, 203, # line 7
              212,213,214,215,224,229,230,231,233,235,236,237,238,  # line 8
              245,246,248,251,252,253,254,255,256,257,261,263, # line 9, position 258 it'll be a zombie generator
              276,278,280,281,287,289,290,291,293,295,296,297,299,  # lina 10
              303,304,308,314,317,326,327,  # lina 11
              334,336,340,341,344,347,350,353,359,  # lina 12
              366,368,370,371,374,377,379,380,383,385,386,387,  # lina 13
              396,398,400,401,407,409,410,413,416,417,419,  # lina 14
              422,423,424,425,434,   # line 15
              458,460,461,462,463,464,465,466,467,469,470,471,472,474,475,476,477,478, # line 16
              483,484,486,488,492,508,  # line 17
              514,518,525,526,527,528,529,531,533,534,535,536,  # line 18
              551,552,553 # line 19
              ]

  # just in case I want to have differents pictures for center and side of the walls
  sideWalls_img = pygame.image.load('../Images/Walls/wall7.png')
  centerWalls_img =pygame.image.load('../Images/Walls/wall7.png')

  # load the floor image
  flor_img = pygame.image.load('../Images/Walls/wall5.png')


  """
    method that is called in the main, that sets up all the tiles
  """
  @staticmethod
  def pre_init(screen):
    for y in range(0, screen.get_height(),  screen.get_height() // 20): # increment by the size of each tile
      for x in range(0, screen.get_width(), screen.get_width() // 30):
      
        # we create a new tile, one by one, for the whole frame, so it's call the constructor
        if ( (Tile.total_tiles in Tile.invalidsSideWalls) or (Tile.total_tiles in Tile.invalidsCenterWalls) ):

          # create a tile with a wall
          Tile(x,y, 'solid', screen) # so it's not empty, you cannot move in it

        else:
          Tile(x,y,'empty', screen) 

  # has differents types, because some can be walkable and others not
  # pass screen to get he size of the screen and then set the size of all tiles
  def __init__(self, x, y, Type, screen): 

    # if we hand't set the size of all tiles, we set it now
    if Tile.width  == 0 or Tile.height ==0:
      # the screen is gonna have 30 tiles por line, with 30 lines, and 20 tiles per column, with 20 column, doens't matter the screen size
      Tile.width = screen.get_width() // 30
      Tile.height = screen.get_height() // 20

      # resize the pictures, according with monitor resolution
      Tile.sideWalls_img = pygame.transform.scale(Tile.sideWalls_img, (Tile.width, Tile.height))
      Tile.centerWalls_img = pygame.transform.scale(Tile.centerWalls_img, (Tile.width, Tile.height))
      Tile.flor_img = pygame.transform.scale(Tile.flor_img, (Tile.width, Tile.height))

    # if new tile is located in the side of the wall
    if Tile.checkInvalidLists(Tile.total_tiles, Tile.invalidsSideWalls) :
      self.img = Tile.sideWalls_img

    # if tile is located in the center/ the real walls
    elif Tile.checkInvalidLists(Tile.total_tiles, Tile.invalidsCenterWalls) : 
      self.img = Tile.centerWalls_img

    # rest of the tiles(floor/walkable)
    else:
      self.img = Tile.flor_img

    self.type = Type 
    self.number = Tile.total_tiles # use to indentify every tile by a number
    Tile.total_tiles += 1 # add a new tile everytime we create one

    if Type == 'empty': 
      self.walkable = True 
    else: 
      self.walkable = False

    # set the tile for a rectangle, then it has x and y position
    pygame.Rect.__init__(self, (x, y) , (Tile.width, Tile.height) )

    Tile.List.append(self) # add the title in the list of tiles



  # use to check in with list of invalid the tile is, or it's not(walkable)
  # then, we can set the right image for the tile
  @staticmethod
  def checkInvalidLists(number, invalidList):

    if number in invalidList:
      return True
    else:
      return False

  # check if tile is free
  @staticmethod
  def isTileFree(tileNumber):

    # check if the tile is invalid, for all lists of invalid tiles
    if Tile.checkInvalidLists(tileNumber , Tile.invalidsSideWalls):
      return False # it's mean the tile is nor free

    elif Tile.checkInvalidLists(tileNumber, Tile.invalidsCenterWalls):
      return False

    return True  # it's available if didn't get catch in the ifs above 


# use to get a tile, and it's static because you don't need an object to get a tile
  @staticmethod
  def get_tile(number):
    for tile in Tile.List:
      if tile.number == number:
        return tile

# method to draw all tiles in the screen every frame
  @staticmethod
  def draw_tiles(screen):
    for tile in Tile.List:   
      screen.blit(tile.img, tile);



