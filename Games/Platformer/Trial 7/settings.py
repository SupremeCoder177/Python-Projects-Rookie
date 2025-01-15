# settings

import json

def load_map(path):
	try:
		with open(path, 'r') as file:
			return json.load(file)
		if not file.closed: file.close()
	except Exception as e: return {}

GAME_SIZE = (1000, 800)
FPS = 60
TILE_SIZE = 50