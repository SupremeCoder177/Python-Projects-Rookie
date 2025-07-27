# settings

import math

FPS = 60
TILE_SIZE = 75

WORLD_MAP = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

SCREEN_SIZE = (len(WORLD_MAP[0]) * TILE_SIZE, len(WORLD_MAP) * TILE_SIZE)
PLAYER_POS = (len(WORLD_MAP[0]) // 2, len(WORLD_MAP) // 2)

PLAYER_ANGLE = 0.0
PLAYER_MOVE_SPEED = 0.05
PLAYER_ROT_SPEED = 0.03
PLAYER_FOV = math.pi / 3
PLAYER_HALF_FOV = PLAYER_FOV // 2
RAY_INC_ANGLE = 0.005
NUM_RAYS = int(PLAYER_FOV / RAY_INC_ANGLE)
MAX_DEPTH = 5


