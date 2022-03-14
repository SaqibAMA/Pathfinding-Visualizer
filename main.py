import pygame
from include.colors import COLORS
from include.constants import DIMENSIONS
from include.constants import MOUSE_BUTTONS
from collections import deque
import math


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

    # BFS/DFS -> which nodes have already been opened.
    EXPLORED_NODES = []
    # BFS/DFS -> what nodes should be explored next.
    NODE_QUEUE = deque([])

    # any nodes that are in obstacles
    OBSTACLES = []

    # the computed path by the algorithms
    PATH = []

    # BFS, DFS, UCS, and A*
    MODE = 'A*'

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
        # print("Returned Heuristic: ", abs(node_location[0] - END_NODE[0]) + abs(node_location[1] - END_NODE[1]))
        return abs(node_location[0] - END_NODE[0]) + abs(node_location[1] - END_NODE[1])

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
            EXPLORED_NODES.append(node.location)
            # sorted(NODE_QUEUE, key=lambda x: x.get_cost())


        # A* -- End

    # initialize pygame
    pygame.init()

    # fonts
    font = {
        'regular': pygame.font.Font('assets/Poppins-Regular.ttf', 16),
        'bold': pygame.font.Font('assets/Poppins-Bold.ttf', 21)
    }

    # textual content
    text_content = {
        'app_title': font['bold'].render('Pathfinding Visualizer - Saqib Ali', True, COLORS['TEXT']),
        'path_cost': font['regular'].render('Path Cost: 0', True, COLORS['TEXT'])
    }

    app_title_rect = text_content['app_title'].get_rect()
    app_title_rect.top = 550
    app_title_rect.left = 25

    path_cost_rect = text_content['path_cost'].get_rect()
    path_cost_rect.top = 25
    path_cost_rect.left = 550

    # set pygame title
    pygame.display.set_caption('Pathfinding Visualizer - Saqib Ali')

    # set screen size
    window_surface = pygame.display.set_mode((800, 600))

    # setting animation
    FPS_CLOCK = pygame.time.Clock()

    # setting background
    background = pygame.Surface((800, 600))
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

            if event.type == pygame.KEYDOWN:
                # start
                if event.key == pygame.K_s:
                    if MODE == 'BFS' or MODE == 'DFS' or MODE == 'UCS':
                        NODE_QUEUE.append(Node(location=START_NODE, g=0))
                    elif MODE == 'A*':
                        NODE_QUEUE.append(Node(location=START_NODE, g=0, h=a_star_heuristic(START_NODE)))
                    start_visualization = True

                # reset
                if event.key == pygame.K_r:
                    EXPLORED_NODES = []
                    NODE_QUEUE = deque([])
                    OBSTACLES = []
                    PATH = []

                # TODO(Saqib): Add obstacle logic
                # obstacles
                if event.key == pygame.K_o:
                    # finding out which cell has been clicked
                    for i in range(len(cells)):
                        for j in range(len(cells[0])):
                            if cells[i][j].collidepoint(pygame.mouse.get_pos()):
                                OBSTACLES.append((j, i))

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
        text_content['path_cost'] = font['regular'].render('Path Cost: ' + str(len(PATH)), True, COLORS['TEXT'])
        window_surface.blit(text_content['path_cost'], path_cost_rect)


        pygame.display.flip()
        pygame.display.update()
        FPS_CLOCK.tick(30)


if __name__ == '__main__':
    main()
