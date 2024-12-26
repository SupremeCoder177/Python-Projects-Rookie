from map import *

class Editor:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption("Editor")
		self.clock = pg.time.Clock()
		self.tile_map = TILE_MAP
		self.offset = [0, 0]
		self.tiles = dict(TILE_MAP)
		self.map = Map(self)
		self.tile_size = TILE_SIZE
		self.move = {'right' : False, 'left' : False, 'up' : False, 'down' : False}
		self.run()

	def run(self):
		while True:
			self.screen.fill('black')

			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if event.type == pg.MOUSEBUTTONDOWN:
					mouse_pos = pg.mouse.get_pos()
					grid_pos = [int((mouse_pos[0] + self.offset[0]) // TILE_SIZE), int((mouse_pos[1] + self.offset[1]) // TILE_SIZE)]
					if pg.mouse.get_pressed()[0]:	
						if str(grid_pos[0]) + ';' + str(grid_pos[1]) not in self.tiles.keys():
							self.tiles[str(grid_pos[0]) + ';' + str(grid_pos[1])] = {"physics" : True}
					if pg.mouse.get_pressed()[2]:
						if str(grid_pos[0]) + ';' + str(grid_pos[1]) in self.tiles.keys():
							del self.tiles[str(grid_pos[0]) + ';' + str(grid_pos[1])]
				if event.type == pg.KEYDOWN and event.key == pg.K_s:
					with open('map.json', 'w') as file:
						json.dump(self.tiles, file, indent = 4, sort_keys = True)
				if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
					self.move['left'] = True
				if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
					self.move['right'] = True
				if event.type == pg.KEYDOWN and event.key == pg.K_UP:
					self.move['up'] = True
				if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
					self.move['down'] = True
				if event.type == pg.KEYUP and event.key == pg.K_LEFT:
					self.move['left'] = False
				if event.type == pg.KEYUP and event.key == pg.K_RIGHT:
					self.move['right'] = False
				if event.type == pg.KEYUP and event.key == pg.K_UP:
					self.move['up'] = False
				if event.type == pg.KEYUP and event.key == pg.K_DOWN:
					self.move['down'] = False
				if event.type== pg.KEYDOWN and event.key == pg.K_DELETE:
					self.tiles.clear()

			if self.move['left']: self.offset[0] -= 10
			if self.move['right']: self.offset[0] += 10
			if self.move['up']: self.offset[1] -= 10
			if self.move['down']: self.offset[1] += 10

			self.map.render(self.screen, self.tiles, self.offset)

			pg.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	Editor()