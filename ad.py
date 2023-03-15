import pygame as pg
from heapq import *


def get_circle(x, y):
    return (x * TILE + TILE // 2, y * TILE + TILE // 2), TILE // 4


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1], [1, 1], [-1, -1], [1, -1], [-1, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


#cols, rows = 23, 13
cols, rows = 13, 11
TILE = 50

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
grid = ['9999999999999',
        '9999999999999',
        '1118811881111',
        '8811111111188',
        '1111144441111',
        '1881144418881',
        '1111444188881',
        '1111144411111',
        '1884444411111',
        '1881144418881',
        '1111144411111']

grid = [[int(char) for char in string ] for string in grid]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


bg = pg.image.load('img/map.png').convert()
bg = pg.transform.scale(bg, (cols * TILE, rows * TILE))


startflag = False
startflag2 = False
start = (0, 7)
goal = (22, 7)
queue = []
visited = {}
cost_visited = {}

# fill screen

loopa = True
loopd = False
while True:
    while loopa:
        pg.display.set_caption('A*')
        sc.blit(bg, (0, 0))
        # draw BFS work
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = pg.mouse.get_pos()
                    start = (start[0] // (50), start[1] // (50))
                    heappush(queue, (0, start))
                    cost_visited = {start: 0}
                    visited = {start: None}
                if event.button == 3:
                    goal = pg.mouse.get_pos()
                    goal = (goal[0] // (50), goal[1] // (50))


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    loopa = True
                    loopd = False
                if event.key == pg.K_RIGHT:
                    loopa = False
                    loopd = True
                if event.key == pg.K_RETURN:
                    startflag = True

        [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
        [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
        pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
        pg.draw.circle(sc, pg.Color('purple'), *get_circle(*goal))
        # Dijkstra logic
        if startflag:
            if queue:
                cur_cost, cur_node = heappop(queue)
                if cur_node == goal:
                    queue = []
                    continue

                next_nodes = graph[cur_node]
                for next_node in next_nodes:
                    neigh_cost, neigh_node = next_node
                    new_cost = cost_visited[cur_node] + neigh_cost

                    if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                        priority = new_cost + heuristic(neigh_node, goal)
                        heappush(queue, (priority, neigh_node))
                        cost_visited[neigh_node] = new_cost
                        visited[neigh_node] = cur_node

            # draw path
            path_head, path_segment = cur_node, cur_node
            while path_segment:
                pg.draw.circle(sc, pg.Color('brown'), *get_circle(*path_segment))
                path_segment = visited[path_segment]
            pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
            pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))
            # pygame necessary lines
        [exit() for event in pg.event.get() if event.type == pg.QUIT]

        pg.display.flip()
        clock.tick(7)

    while loopd:
        # fill screen
        sc.blit(bg, (0, 0))
        pg.display.set_caption('dijkstra')
        # draw BFS work
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = pg.mouse.get_pos()
                    start = (start[0] // (50), start[1] // (50))
                    heappush(queue, (0, start))
                    cost_visited = {start: 0}
                    visited = {start: None}
                if event.button == 3:
                    goal = pg.mouse.get_pos()
                    goal = (goal[0] // (50), goal[1] // (50))

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    loopa = True
                    loopd = False
                if event.key == pg.K_RIGHT:
                    loopa = False
                    loopd = True
                if event.key == pg.K_RETURN:
                    startflag2 = True

        [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y), 1) for x, y in visited]
        [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(*xy)) for _, xy in queue]
        pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
        pg.draw.circle(sc, pg.Color('purple'), *get_circle(*goal))

        # Dijkstra logic
        if startflag2:
            if queue:
                cur_cost, cur_node = heappop(queue)
                if cur_node == goal:
                    queue = []
                    continue

                next_nodes = graph[cur_node]
                for next_node in next_nodes:
                    neigh_cost, neigh_node = next_node
                    new_cost = cost_visited[cur_node] + neigh_cost

                    if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                        heappush(queue, (new_cost, neigh_node))
                        cost_visited[neigh_node] = new_cost
                        visited[neigh_node] = cur_node

            # draw path
            path_head, path_segment = cur_node, cur_node
            while path_segment:
                pg.draw.circle(sc, pg.Color('brown'), *get_circle(*path_segment))
                path_segment = visited[path_segment]
            pg.draw.circle(sc, pg.Color('blue'), *get_circle(*start))
            pg.draw.circle(sc, pg.Color('magenta'), *get_circle(*path_head))
        # pygame necessary lines
        [exit() for event in pg.event.get() if event.type == pg.QUIT]
        pg.display.flip()
        clock.tick(7)
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
