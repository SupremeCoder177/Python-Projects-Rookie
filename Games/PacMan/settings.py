# settings 

from os import listdir

FPS = 60
WALL_WIDTH = WALL_HEGIHT = 50 # the sprite height
WALL_MAP_WIDTH = WALL_MAP_HEIGHT = WALL_WIDTH / 2 # projected wall size on the map
SCREEN_SIZE = (WALL_WIDTH * 20, WALL_HEGIHT * 12) # for the level maker
TILE_SIZE = WALL_MAP_WIDTH # don't change this please
OFFSET_CHANGE_SPEED = 10 # pixels per second, only for the levelMaker file, in the actual game the offset changes according to player movement speed

PLAYER_WIDTH = PLAYER_HEIGHT = int(TILE_SIZE)
PLAYER_PROJECTED_MULTIPLIER = 0.75
ENEMY_PROJECTED_MULTIPLIER = PLAYER_PROJECTED_MULTIPLIER
PLAYER_MAP_WIDTH = PLAYER_MAP_HEIGHT = int(PLAYER_WIDTH * PLAYER_PROJECTED_MULTIPLIER)
ENEMY_WIDTH = ENEMY_HEIGHT = PLAYER_WIDTH
ENEMY_MAP_WIDTH = ENEMY_MAP_HEIGHT = int(ENEMY_WIDTH * ENEMY_PROJECTED_MULTIPLIER)

COIN_WIDTH = COIN_HEIGHT = int(TILE_SIZE)
COIN_MAP_WIDTH = COIN_MAP_HEIGHT = int(PLAYER_WIDTH / 2)

GAME_SCREEN_SIZE = (TILE_SIZE * 25, TILE_SIZE * 20) # for the actual game window, personally I think this is the perfect size but you can change if you want
MAX_ENEMY_COUNT = 4 # change this if you want to add more enemies to the game, although it will be laggy

# loading all the level file names
# P.S. there should always be a single level made in the levels folder or this might crash
# Naming convention for levels is = level + level number + .json
LEVELS = [level for level in listdir("levels") if level.endswith(".json")]
CURRENT_LEVEL = 0
MAX_LEVEL = len(LEVELS) - 1

# animation settings
# coins
COIN_ANIM_SPEED = 0.2
# player
PLAYER_ANIM_SPEED = 0.8
# enemy
ENEMY_ANIM_SPEED = 0.8

# movement settings
PLAYER_MOVE_SPEED = 1 / 5 # tiles per second
ENEMY_MOVE_SPEED = 1 / 4 # tiles per second
# enemy moves faster in the original pac-man as well

# random useful variables (don't change them)
OPP_MAP = {
		  "right" : "left",
		  "left" : "right",
		  "up" : "down",
		  "down" : "up"
		}

VECTOR_MAP = {
	"horizontal" : ["left", "right"],
	"vertical" : ["up", "down"]
}

DIRECTIONAL_ADDER = {
	"up" : [0, -1],
	"down": [0, 1],
	"left": [-1, 0],
	"right": [1, 0]
}