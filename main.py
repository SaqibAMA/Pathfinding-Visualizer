# TODO: I need to composite the nodeSelectionFunction based on the algorithm and make code cleaner.

import pygame
from include.colors import COLORS
from include.constants import DIMENSIONS
from include.constants import MOUSE_BUTTONS
from collections import deque
from random import random

# keeps the problem node
class Node:

    def __init__(self, location=None, parents=[], g=0, h=0):
        self.location = location
        self.parents = parents
        self.g = g
        self.h = h

    def __eq__(self, other):
        return self.location == other.location

    def __lt__(self, other):
        return self.get_cost() < other.get_cost()

    def __gt__(self, other):
        return self.get_cost() > other.get_cost()

    def get_cost(self):
        return self.g + self.h


def main():
    # initial parameters

    # starting and ending nodes
    START_NODE = (1, 2)
    END_NODE = (8, 7)

    # BFS/DFS/A* -> which nodes have already been opened.
    EXPLORED_NODES = []
    # BFS/DFS/A* -> what nodes should be explored next.
    NODE_QUEUE = deque([])
    NODE_CLOSED = deque([])

    # any nodes that are in obstacles
    OBSTACLES = []

    # the computed path by the algorithms
    PATH = []

    # maze file reading logic
    # with open('maze.txt') as f:
    #     for i, line in enumerate(f):
    #         for j, c in enumerate(line):
    #             if c == '#':
    #                 OBSTACLES.append((j, i))
    #             if c == 'S':
    #                 START_NODE = (j, i)
    #             if c == 'G':
    #                 END_NODE = (j, i)

    # BFS, DFS, UCS, Greedy, and A*
    MODE = 'BFS'

    # handling cell click
    def handle_cell_click(cell_location, event_btn):

        x, y = cell_location

        nonlocal START_NODE
        nonlocal END_NODE

        if event_btn == MOUSE_BUTTONS['LEFT'] and cell_location != END_NODE:
            START_NODE = (x, y)
        elif event_btn == MOUSE_BUTTONS['RIGHT'] and cell_location != START_NODE:
            END_NODE = (x, y)

    # handle a* manhattan heuristic value
    def a_star_heuristic(node_location):
        # manhattan distance
        return abs(node_location[0] - END_NODE[0]) + abs(node_location[1] - END_NODE[1])
        # return math.sqrt( (node_location[0] - END_NODE[0])**2 + (node_location[1] - END_NODE[1])**2 )

    # handling search algorithms and their visualization
    def handle_visualization():

        # finds all possible moves for a given
        # position
        def get_frontiers(node):
            frontiers = [
                (node.location[0] - 1, node.location[1]),
                (node.location[0] + 1, node.location[1]),
                (node.location[0], node.location[1] - 1),
                (node.location[0], node.location[1] + 1)
            ]
            return frontiers

        nonlocal start_visualization
        nonlocal PATH
        nonlocal EXPLORED_NODES

        # Complete BFS/DFS Implementation -- Start

        if MODE == 'BFS' or MODE == 'DFS':

            node = NODE_QUEUE.pop()

            if node.location == END_NODE:
                PATH = [parent.location for parent in node.parents]
                start_visualization = False
                return

            frontiers = get_frontiers(node)

            parents = list(node.parents)
            parents.append(node)

            frontiers = [
                Node(location=f, parents=parents)
                for f in frontiers
                if f[0] in range(DIMENSIONS['GRID_SIZE']) and
                   f[1] in range(DIMENSIONS['GRID_SIZE']) and
                   f not in EXPLORED_NODES and
                   Node(location=f) not in NODE_QUEUE and
                   f not in OBSTACLES
            ]

            if MODE == 'DFS':
                NODE_QUEUE.extend(frontiers)
            elif MODE == 'BFS':
                NODE_QUEUE.extendleft(frontiers)

            EXPLORED_NODES.append(node.location)

        # -- BFS/DFS END

        # Complete UCS -- Start

        if MODE == 'UCS':

            # get the minimum node
            node = min(NODE_QUEUE, key=lambda x: x.get_cost())
            NODE_QUEUE.remove(node)

            # if it is the end node, then terminate
            if node.location == END_NODE:
                PATH = [parent.location for parent in node.parents]
                start_visualization = False
                return

            frontiers = get_frontiers(node)

            parents = list(node.parents)
            parents.append(node)

            frontiers = [
                Node(location=f, parents=parents, g=node.g + 1)
                for f in frontiers
                if f[0] in range(DIMENSIONS['GRID_SIZE']) and
                   f[1] in range(DIMENSIONS['GRID_SIZE']) and
                   f not in EXPLORED_NODES and
                   Node(location=f) not in NODE_QUEUE and
                   f not in OBSTACLES
            ]

            NODE_QUEUE.extend(frontiers)
            EXPLORED_NODES.append(node.location)
            # sorted(NODE_QUEUE, key=lambda x: x.get_cost())

        # UCS -- End

        # Complete A* -- Start

        if MODE == 'A*':

            # get the minimum node

            node = min(NODE_QUEUE, key=lambda x: x.get_cost())

            # it's better to use a child than to go for a parent
            if len(NODE_CLOSED) > 0:
                last_explored = NODE_CLOSED[-1]
                valid_nodes = [vn for vn in NODE_QUEUE if
                               vn.g == last_explored.g + 1 and vn.get_cost() == node.get_cost()]
                if len(valid_nodes) > 0:
                    node = valid_nodes[0]

            NODE_QUEUE.remove(node)

            # if it is the end node, then terminate
            if node.location == END_NODE:
                PATH = [parent.location for parent in node.parents]
                start_visualization = False
                return

            frontiers = get_frontiers(node)

            parents = list(node.parents)
            parents.append(node)

            frontiers = [
                Node(location=f, parents=parents, g=node.g + 1, h=a_star_heuristic(f))
                for f in frontiers
                if f[0] in range(DIMENSIONS['GRID_SIZE']) and
                   f[1] in range(DIMENSIONS['GRID_SIZE']) and
                   f not in EXPLORED_NODES and
                   Node(location=f) not in NODE_QUEUE and
                   f not in OBSTACLES
            ]

            NODE_QUEUE.extend(frontiers)
            NODE_CLOSED.append(node)
            EXPLORED_NODES.append(node.location)
            # sorted(NODE_QUEUE, key=lambda x: x.get_cost())

        # A* -- End

        # Greedy -- start

        if MODE == 'Greedy':

            # get the minimum node

            node = min(NODE_QUEUE, key=lambda x: x.get_cost())

            NODE_QUEUE.remove(node)

            # if it is the end node, then terminate
            if node.location == END_NODE:
                PATH = [parent.location for parent in node.parents]
                start_visualization = False
                return

            frontiers = get_frontiers(node)

            parents = list(node.parents)
            parents.append(node)

            frontiers = [
                Node(location=f, parents=parents, g=0, h=a_star_heuristic(f))
                for f in frontiers
                if f[0] in range(DIMENSIONS['GRID_SIZE']) and
                   f[1] in range(DIMENSIONS['GRID_SIZE']) and
                   f not in EXPLORED_NODES and
                   Node(location=f) not in NODE_QUEUE and
                   f not in OBSTACLES
            ]

            NODE_QUEUE.extend(frontiers)
            NODE_CLOSED.append(node)
            EXPLORED_NODES.append(node.location)
            # sorted(NODE_QUEUE, key=lambda x: x.get_cost())

        # Greedy -- End

    # initialize pygame
    pygame.init()

    # fonts
    font = {
        'regular': pygame.font.Font('assets/Poppins-Regular.ttf', 14),
        'bold': pygame.font.Font('assets/Poppins-Bold.ttf', 21)
    }

    # textual content
    text_content = {
        'app_title': font['bold'].render('Pathfinding Visualizer - Saqib Ali', True, COLORS['TEXT']),
        'path_cost': font['bold'].render('Path Cost: 0', True, COLORS['TEXT'])
    }

    app_title_rect = text_content['app_title'].get_rect()
    app_title_rect.top, app_title_rect.left = (550, 25)

    path_cost_rect = text_content['path_cost'].get_rect()
    path_cost_rect.top, path_cost_rect.left = (25, 550)

    # algo buttons
    algo_buttons = {
        'BFS': font['bold'].render('1 - Breadth-First Search', True, COLORS['TEXT']),
        'DFS': font['bold'].render('2 - Depth-First Search', True, COLORS['TEXT']),
        'UCS': font['bold'].render('3 - Uniform-Cost Search', True, COLORS['TEXT']),
        'A*': font['bold'].render('4 - A* Search', True, COLORS['TEXT']),
        'Greedy': font['bold'].render('5 - Greedy Search', True, COLORS['TEXT']),
    }

    bfs_button_rect, dfs_button_rect, ucs_button_rect, a_star_button_rect, greedy_button_rect = algo_buttons[
                                                                                                    'BFS'].get_rect(), \
                                                                                                algo_buttons[
                                                                                                    'DFS'].get_rect(), \
                                                                                                algo_buttons[
                                                                                                    'UCS'].get_rect(), \
                                                                                                algo_buttons[
                                                                                                    'A*'].get_rect(), \
                                                                                                algo_buttons[
                                                                                                    'Greedy'].get_rect()
    bfs_button_rect.top, bfs_button_rect.left = (100, 550)
    dfs_button_rect.top, dfs_button_rect.left = (150, 550)
    ucs_button_rect.top, ucs_button_rect.left = (200, 550)
    a_star_button_rect.top, a_star_button_rect.left = (250, 550)
    greedy_button_rect.top, greedy_button_rect.left = (300, 550)

    # instructions text
    instructions_text = {
        'algo_select': font['regular'].render('- Press 1, 2, 3, 4, and 5 to for algorithm.', True,
                                              COLORS['TEXT']),
        'start_select': font['regular'].render('- Left click on a cell to select START.', True, COLORS['TEXT']),
        'end_select': font['regular'].render('- Right click on a cell to select END.', True, COLORS['TEXT']),
        'start': font['regular'].render('- Press S to start the visualization.', True, COLORS['TEXT']),
        'reset': font['regular'].render('- Press R to reset the visualization.', True, COLORS['TEXT']),
        'obstacle': font['regular'].render('- Press O over a cell to create obstacle.', True, COLORS['TEXT']),
        'maze': font['regular'].render('- Press M to generate a random maze.', True, COLORS['TEXT'])
    }

    # set pygame title
    pygame.display.set_caption('Pathfinding Visualizer - Saqib Ali')

    # set screen size
    window_surface = pygame.display.set_mode((850, 600))

    # setting animation
    FPS_CLOCK = pygame.time.Clock()

    # setting background
    background = pygame.Surface((850, 600))
    background.fill(pygame.Color('#FFFFFF'))

    # generating cells
    # looping and drawing the grid
    cells = []
    for i in range(0, DIMENSIONS['GRID_SIZE']):
        cells.append([])
        for j in range(0, DIMENSIONS['GRID_SIZE']):
            cells[-1].append(pygame.Rect(j * DIMENSIONS['CELL_SIZE'] + DIMENSIONS['GAP'] + DIMENSIONS['MARGIN'],
                                         i * DIMENSIONS['CELL_SIZE'] + DIMENSIONS['GAP'] + DIMENSIONS['MARGIN'],
                                         DIMENSIONS['CELL_SIZE'] - DIMENSIONS['GAP'],
                                         DIMENSIONS['CELL_SIZE'] - DIMENSIONS['GAP']))

    # main window loop
    is_running = True
    start_visualization = False

    while is_running:

        # event handlers
        for event in pygame.event.get():

            # quitting the sim
            if event.type == pygame.QUIT:
                is_running = False

            # if mouse has been clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                # finding out which cell has been clicked
                for i in range(len(cells)):
                    for j in range(len(cells[0])):
                        if cells[i][j].collidepoint(event.pos):
                            handle_cell_click((j, i), event.button)
                            print(a_star_heuristic((j, i)))

            if event.type == pygame.KEYDOWN:
                # start
                if event.key == pygame.K_s:

                    # reset it first
                    EXPLORED_NODES = []
                    NODE_QUEUE = deque([])
                    PATH = []

                    if MODE == 'BFS' or MODE == 'DFS' or MODE == 'UCS':
                        NODE_QUEUE.append(Node(location=START_NODE, g=0))
                    elif MODE == 'A*' or MODE == 'Greedy':
                        NODE_QUEUE.append(Node(location=START_NODE, g=0, h=a_star_heuristic(START_NODE)))
                    start_visualization = True

                # reset
                if event.key == pygame.K_r:
                    EXPLORED_NODES = []
                    NODE_QUEUE = deque([])
                    OBSTACLES = []
                    PATH = []

                # obstacles
                if event.key == pygame.K_o:
                    # finding out which cell has been clicked
                    for i in range(len(cells)):
                        for j in range(len(cells[0])):
                            if cells[i][j].collidepoint(pygame.mouse.get_pos()):
                                OBSTACLES.append((j, i))

                # handling algo buttons
                if event.key == pygame.K_1:
                    MODE = 'BFS'
                if event.key == pygame.K_2:
                    MODE = 'DFS'
                if event.key == pygame.K_3:
                    MODE = 'UCS'
                if event.key == pygame.K_4:
                    MODE = 'A*'
                if event.key == pygame.K_5:
                    MODE = 'Greedy'

                # handling maze generation
                if event.key == pygame.K_m:
                    OBSTACLES = []
                    for i in range(DIMENSIONS['GRID_SIZE']):
                        for j in range(DIMENSIONS['GRID_SIZE']):
                            if random() > 0.7 and (i, j) != START_NODE and (i, j) != END_NODE:
                                OBSTACLES.append((i, j))

        window_surface.blit(background, (0, 0))

        for i in range(len(cells)):
            for j in range(len(cells)):

                if (j, i) in EXPLORED_NODES:
                    pygame.draw.rect(window_surface, COLORS['EXPLORE'], cells[i][j], border_radius=2)
                else:
                    pygame.draw.rect(window_surface, COLORS['CELL'], cells[i][j], border_radius=2)

                if START_NODE == (j, i):
                    pygame.draw.rect(window_surface, COLORS['START'], cells[i][j], border_radius=2)

                if END_NODE == (j, i):
                    pygame.draw.rect(window_surface, COLORS['END'], cells[i][j], border_radius=2)

                if (j, i) in OBSTACLES:
                    pygame.draw.rect(window_surface, COLORS['OBSTACLE'], cells[i][j], border_radius=2)

                if (j, i) in PATH and (j, i) != START_NODE:
                    pygame.draw.rect(window_surface, COLORS['PATH'], cells[i][j], border_radius=2)

        if start_visualization and len(NODE_QUEUE) != 0:
            handle_visualization()

        # drawing heading
        window_surface.blit(text_content['app_title'], app_title_rect)
        text_content['path_cost'] = font['bold'].render('Path Cost: ' + str(len(PATH)), True, COLORS['END'])
        window_surface.blit(text_content['path_cost'], path_cost_rect)

        # drawing buttons
        algo_buttons['BFS'] = font['bold'].render('1 - Breadth-First Search', True,
                                                  COLORS['TEXT'] if MODE != 'BFS' else COLORS['END'])
        window_surface.blit(algo_buttons['BFS'], bfs_button_rect)
        algo_buttons['DFS'] = font['bold'].render('2 - Depth-First Search', True,
                                                  COLORS['TEXT'] if MODE != 'DFS' else COLORS['END'])
        window_surface.blit(algo_buttons['DFS'], dfs_button_rect)
        algo_buttons['UCS'] = font['bold'].render('3 - Uniform-Cost Search', True,
                                                  COLORS['TEXT'] if MODE != 'UCS' else COLORS['END'])
        window_surface.blit(algo_buttons['UCS'], ucs_button_rect)
        algo_buttons['A*'] = font['bold'].render('4 - A* Search', True,
                                                 COLORS['TEXT'] if MODE != 'A*' else COLORS['END'])
        window_surface.blit(algo_buttons['A*'], a_star_button_rect)
        algo_buttons['Greedy'] = font['bold'].render('5 - Greedy Search', True,
                                                     COLORS['TEXT'] if MODE != 'Greedy' else COLORS['END'])
        window_surface.blit(algo_buttons['Greedy'], greedy_button_rect)

        for idx, it in enumerate(instructions_text):
            it_rect = instructions_text[it].get_rect()
            it_rect.top, it_rect.left = (400 + (idx * 25), 550)
            window_surface.blit(instructions_text[it], it_rect)

        pygame.display.flip()
        pygame.display.update()
        FPS_CLOCK.tick(30)


if __name__ == '__main__':
    main()
