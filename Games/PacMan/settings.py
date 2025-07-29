# settings 

FPS = 60
WALL_WIDTH = WALL_HEGIHT = 50 # the sprite height
WALL_MAP_WIDTH = WALL_MAP_HEIGHT = WALL_WIDTH / 2 # projected wall size on the map
SCREEN_SIZE = (WALL_WIDTH * 20, WALL_HEGIHT * 12) # for the level maker
TILE_SIZE = WALL_MAP_WIDTH
OFFSET_CHANGE_SPEED = 10 # pixels per second

PLAYER_WIDTH = PLAYER_HEIGHT = int(TILE_SIZE)
ENEMY_WIDTH = ENEMY_HEIGHT = PLAYER_WIDTH

GAME_SCREEN_SIZE = (TILE_SIZE * 20, TILE_SIZE * 15) # for the actual game window

