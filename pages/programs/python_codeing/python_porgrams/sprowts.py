import pygame as p
import random as r
import math

BACKGROUND_COLOR = (200, 200, 200)
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 840
BORDER_DISTANCE, MIN_DISTANCE_SQR = 150, 150 ** 2
MIN_DOTS, MAX_DOTS = 5, 20
NODE_RADIUS = 7
EDGE_COLOR = (0, 0, 255)
NODE_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)
LINE_COLOR = (255, 0, 0)
FPS = 60
DOT_LINE_THRESHOLD = 15

SCREEN = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
p.display.set_caption('Sprowts')
CLOCK = p.time.Clock()

def generate_dots(mnd=MIN_DOTS, mxd=MAX_DOTS):
    dots = []
    while len(dots) < r.randint(mnd, mxd):
        new_dot = (r.randint(BORDER_DISTANCE, SCREEN_WIDTH - BORDER_DISTANCE),
                   r.randint(BORDER_DISTANCE, SCREEN_HEIGHT - BORDER_DISTANCE))
        if all((new_dot[0] - x) ** 2 + (new_dot[1] - y) ** 2 >= MIN_DISTANCE_SQR for x, y in dots):
            dots.append(new_dot)
    return dots

def get_closest_node(pos, nodes):
    return min(nodes, key=lambda node: (pos[0] - node[0]) ** 2 + (pos[1] - node[1]) ** 2, default=None)

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    return False

class Graph:
    def __init__(self):
        self.nodes = generate_dots()
        self.paths = []

    def add_path(self, start_node, end_node, path, first_pos, last_pos):
        first_node_distance = math.sqrt((first_pos[0] - start_node[0]) ** 2 + (first_pos[1] - start_node[1]) ** 2)
        last_node_distance = math.sqrt((last_pos[0] - end_node[0]) ** 2 + (last_pos[1] - end_node[1]) ** 2)
        if first_node_distance >= DOT_LINE_THRESHOLD or last_node_distance >= DOT_LINE_THRESHOLD:
            return
        if start_node == end_node:
            return
        for existing_start, existing_end, existing_path in self.paths:
            if do_intersect(start_node, end_node, existing_start, existing_end):
                return
            for i in range(len(existing_path) - 1):
                if do_intersect(start_node, end_node, existing_path[i], existing_path[i + 1]):
                    return
        self.paths.append((start_node, end_node, path))

    def draw_graph(self, screen, current_path=None):
        for start_node, end_node, path in self.paths:
            p.draw.lines(screen, EDGE_COLOR, False, path, 2)
            p.draw.circle(screen, HIGHLIGHT_COLOR, start_node, NODE_RADIUS)
            p.draw.circle(screen, HIGHLIGHT_COLOR, end_node, NODE_RADIUS)
        for x, y in self.nodes:
            p.draw.circle(screen, NODE_COLOR, (x, y), NODE_RADIUS)
        if current_path and len(current_path) > 1:
            p.draw.lines(screen, LINE_COLOR, False, current_path, 2)

def main():
    graph = Graph()
    running = True
    drawing_path = False
    current_path = []
    start_node = None
    first_pos = None
    last_pos = None
    while running:
        SCREEN.fill(BACKGROUND_COLOR)
        graph.draw_graph(SCREEN, current_path=current_path)
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_node = get_closest_node(p.mouse.get_pos(), graph.nodes)
                    if start_node:
                        drawing_path = True
                        current_path = [start_node]
                        first_pos = p.mouse.get_pos()
            elif event.type == p.MOUSEMOTION and drawing_path:
                current_path.append(p.mouse.get_pos())
            elif event.type == p.MOUSEBUTTONUP:
                if event.button == 1 and drawing_path:
                    end_node = get_closest_node(p.mouse.get_pos(), graph.nodes)
                    if end_node:
                        current_path.append(end_node)
                        last_pos = p.mouse.get_pos()
                        graph.add_path(start_node, end_node, current_path, first_pos, last_pos)
                    drawing_path = False
                    current_path = []
        p.display.flip()
        CLOCK.tick(FPS)
    p.quit()

if __name__ == '__main__':
    main()