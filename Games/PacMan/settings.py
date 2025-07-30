# settings 

from os import listdir

FPS = 60
WALL_WIDTH = WALL_HEGIHT = 50 # the sprite height
WALL_MAP_WIDTH = WALL_MAP_HEIGHT = WALL_WIDTH / 2 # projected wall size on the map
SCREEN_SIZE = (WALL_WIDTH * 20, WALL_HEGIHT * 12) # for the level maker
TILE_SIZE = WALL_MAP_WIDTH
OFFSET_CHANGE_SPEED = 10 # pixels per second

PLAYER_WIDTH = PLAYER_HEIGHT = int(TILE_SIZE)
PLAYER_MAP_WIDTH = PLAYER_MAP_HEIGHT = int(PLAYER_WIDTH * 0.75)
ENEMY_WIDTH = ENEMY_HEIGHT = PLAYER_WIDTH

COIN_WIDTH = COIN_HEIGHT = int(TILE_SIZE)
COIN_MAP_WIDTH = COIN_MAP_HEIGHT = int(PLAYER_WIDTH / 2)

GAME_SCREEN_SIZE = (TILE_SIZE * 25, TILE_SIZE * 20) # for the actual game window
MAX_ENEMY_COUNT = 4 # change this if you want to add more enemies to the game, although it will be laggy

# loading all the level file names
# P.S. there should always be a single level made in the levels folder or this might crash
# Naming convention for levels is = level + level number + .json
LEVELS = listdir("levels")
CURRENT_LEVEL = 0
MAX_LEVEL = len(LEVELS) - 1

# animation settings
# coins
COIN_ANIM_SPEED = 0.2
#player
PLAYER_ANIM_SPEED = 0.8

# movement settings
PLAYER_MOVE_SPEED = 1 / 4 # tiles per second