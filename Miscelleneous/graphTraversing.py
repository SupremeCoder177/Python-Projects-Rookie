from PIL import Image, ImageDraw
import os


class GraphNode:

    def __init__(self, parent = None, val = [0, 0], neighbours = None):
        self.parent = parent
        self.neighbours = neighbours if neighbours is not None else []
        self.val = val


class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) < 1: return None
        return self.items.pop()


class Queue(Stack):

    def __init__(self):
        super().__init__()

    def pop(self):
        if len(self.items) < 1: return None
        return self.items.pop(0)


class MapLoader:

    def __init__(self, fp : str, ts : int = 20, wall = "#", space = " ", start = "S", end = "E", show_image = False):
        if not os.path.exists(fp) or not os.path.isfile(fp):
            return

        self.coords = []
        self.tile_size = ts
        self.constructed_graph = False

        text = None
        with open(fp, "r") as f:
            temp = []
            text = f.read()

        for ch in text:
            if ch == wall:
                temp.append(1)
            elif ch in [space, start, end]:
                if ch == space:
                    temp.append(0)
                elif ch == start:
                    temp.append(2)
                elif ch == end:
                    temp.append(3)
            else:
                self.coords.append(temp.copy())
                temp.clear()
        self.coords.append(temp)
            
        width = len(self.coords[0])
        height = len(self.coords)
        self.show = show_image


        for i in range(len(self.coords)):
            for j in range(len(self.coords[0])):
                if self.coords[i][j] == 2:
                    self.start = [j, i]
                elif self.coords[i][j] == 3:
                    self.end = [j, i]

        self.start_node = GraphNode(val = self.start)
        self.visited = [([False] * width) for _ in range(height)]
        
        if self.show:
            self.img = Image.new("RGBA", (width * self.tile_size, height * self.tile_size), color = "#1c1c1c")
            self.draw = ImageDraw.Draw(self.img, "RGBA")
            
            for i in range(height):
                for j in range(width):
                    if self.show:
                        if self.coords[i][j]:
                            self.draw_square(j, i, width = int(self.tile_size * 0.05))
                           
            self.draw_square(self.start[0], self.start[1], color = "yellow", width = int(self.tile_size * 0.07))
            self.draw_square(self.end[0], self.end[1], color = "cyan", width = int(self.tile_size * 0.07))
            
    # only call if self.show is True
    def draw_square(self, x, y, color = "#922e2e", outline = "black", width = 0):
        if not self.show: return
        self.draw.rectangle((x * self.tile_size, y * self.tile_size, x * self.tile_size + self.tile_size, y * self.tile_size + self.tile_size), fill = color, outline = outline, width = width)

    def construct_graph(self):
        if self.constructed_graph: return
        frontier = Stack()
        frontier.push(self.start_node)

        while len(frontier.items) > 0:
            node = frontier.pop()
            for point in self.get_valid_neighbours(node.val):
                if not self.visited[point[1]][point[0]] and self.coords[point[1]][point[0]] in [0, 2, 3]:
                    self.visited[point[1]][point[0]] = True
                    temp_node = GraphNode(val = point, parent = node)
                    node.neighbours.append(temp_node)
                    frontier.push(temp_node)
        self.constructed_graph = True    

    def get_valid_neighbours(self, point):
        POINTS_OFFSET = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        out = []
        for offset in POINTS_OFFSET:
            temp = [point[0] + offset[0], point[1] + offset[1]]
            if 0 <= temp[0] < len(self.coords[0]) and 0 <= temp[1] < len(self.coords):
                out.append(temp.copy())
        return out

    def reset_visited(self):
        self.visited = [[False] * len(self.coords[0]) for _ in range(len(self.coords))]

    def bfsSearch(self):
        self.search(stack = False)

    def search(self, stack = True):
        self.construct_graph()
        self.reset_visited()
        frontier = Queue() if not stack else Stack()

        frontier.push(self.start_node)
        curr_node = self.start_node
        while len(frontier.items) > 0 and curr_node.val != self.end:
            curr_node = frontier.pop()
            self.visited[curr_node.val[1]][curr_node.val[0]] = True
            
            for node in curr_node.neighbours:
                frontier.push(node)

        if self.show:
            for i in range(len(self.visited)):
                for j in range(len(self.visited[0])):
                    if self.visited[i][j] and [j, i] != self.end and [j, i] != self.start:
                        self.draw_square(j, i, color = "#00a0b5", width = int(self.tile_size * 0.1))
            self.img.show()

    def dfsSearch(self):
        self.search()

            
if __name__ == "__main__":
    m = MapLoader("map2.txt", ts = 30, show_image = True)
    m.dfsSearch()
