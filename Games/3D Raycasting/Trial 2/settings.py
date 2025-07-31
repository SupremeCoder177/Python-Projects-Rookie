import math

TILE_SIZE = 75

WORLD_MAP = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

FPS = 0
WIDTH, HEIGHT = len(WORLD_MAP[0]) * TILE_SIZE, len(WORLD_MAP) * TILE_SIZE

PLAYER_START_POSITION = [len(WORLD_MAP[0]) / 2, len(WORLD_MAP) / 2]
PLAYER_ANGLE = 0.0
PLAYER_SPEED = 0.3
PLAYER_ROT_SPEED = 0.1

PLAYER_FOV = math.pi / 3
HALF_PLAYER_FOV = PLAYER_FOV / 2
DELTA_ANGLE = 1e-3
NUM_RAYS = int(PLAYER_FOV / DELTA_ANGLE)
MAX_DEPTH = 10 # tiles not pixels

