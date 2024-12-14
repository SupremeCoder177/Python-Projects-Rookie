# tetris settings

GAME_SIZE = (700, 800)
SCORE_WIDTH = 500
FPS = 3
COL_SIZE = 50
GRID_COLOR = (20, 20, 20)
GRID_WIDTH = 2
BRICK_COLORS = ('red', 'white', 'purple', 'yellow', 'green', 'orange', 'cyan', 'blue')
BRICK_WIDTH = 5
BRICK_STYLE = BRICK_WIDTH * 4

BRICKS = {
	'brick_1' : {
		0 : lambda x, y: [(x, y), (x + COL_SIZE, y), (x - COL_SIZE, y), (x, y - COL_SIZE)],
		1 : lambda x, y: [(x, y), (x + COL_SIZE, y), (x - COL_SIZE, y), (x, y + COL_SIZE)],
		2 : lambda x, y: [(x, y), (x + COL_SIZE, y), (x, y - COL_SIZE), (x, y + COL_SIZE)],
		3 : lambda x, y: [(x, y), (x - COL_SIZE, y), (x, y - COL_SIZE), (x, y + COL_SIZE)]
	},
	'brick_2' : {
		0 : lambda x, y: [(x, y), (x + COL_SIZE, y), (x, y + COL_SIZE), (x + COL_SIZE, y + COL_SIZE)],
	},
	'brick_3' : {
		0 : lambda x, y: [(x, y), (x, y - COL_SIZE), (x, y + COL_SIZE), (x, y + (2 * COL_SIZE))],
		1 : lambda x, y: [(x, y), (x - COL_SIZE, y), (x + COL_SIZE, y), (x + (2 * COL_SIZE), y)]
	},
	'brick_4' : {
		0 : lambda x, y: [(x, y), (x + COL_SIZE, y), (x, y + COL_SIZE), (x - COL_SIZE, y + COL_SIZE)],
		1 : lambda x, y: [(x, y), (x, y - COL_SIZE), (x + COL_SIZE, y), (x + COL_SIZE, y + COL_SIZE)]
	}

}

FONT_COLOR = (214, 13, 93)