import pygame
from include.colors import COLORS
from include.constants import DIMENSIONS
from include.constants import MOUSE_BUTTONS
from collections import deque

class Node:
    def __init__(self, location=None, parents=[]):
        self.location = location
        self.parents = parents
    def __eq__(self, other):
        return self.location == other.location

def main():
    # initial parameters

    START_NODE = (1, 2)
    END_NODE = (8, 7)

    EXPLORED_NODES = []
    NODE_QUEUE = deque([Node(location=START_NODE, parents=[])])

    PATH = []

    # handling cell click
    def handle_cell_click(cell_location, event_btn):

        x, y = cell_location

        nonlocal START_NODE
        nonlocal END_NODE

        if event_btn == MOUSE_BUTTONS['LEFT'] and cell_location != END_NODE:
            START_NODE = (x, y)
        elif event_btn == MOUSE_BUTTONS['RIGHT'] and cell_location != START_NODE:
            END_NODE = (x, y)

    # initialize pygame
    pygame.init()

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

                start_visualization = True

                # TODO: Replace this with a neater comprehension

                # finding out which cell has been clicked
                for i in range(len(cells)):
                    for j in range(len(cells[0])):
                        if cells[i][j].collidepoint(event.pos):
                            handle_cell_click((j, i), event.button)

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

                if (j, i) in PATH and (j, i) != START_NODE:
                    pygame.draw.rect(window_surface, COLORS['PATH'], cells[i][j], border_radius=2)

        if start_visualization and len(NODE_QUEUE) != 0:

            # Complete BFS Implementation -- Start

            node = NODE_QUEUE.popleft()

            if node.location == END_NODE:
                PATH = [parent.location for parent in node.parents]
                start_visualization = False
                continue

            frontiers = [
                (node.location[0] - 1, node.location[1]),
                (node.location[0] + 1, node.location[1]),
                (node.location[0], node.location[1] - 1),
                (node.location[0], node.location[1] + 1)
            ]

            parents = list(node.parents)
            parents.append(node)

            frontiers = [
                Node(location=f, parents=parents)
                for f in frontiers
                if f[0] in range(DIMENSIONS['GRID_SIZE']) and
                   f[1] in range(DIMENSIONS['GRID_SIZE']) and
                   f not in EXPLORED_NODES and
                   Node(location=f) not in NODE_QUEUE
            ]

            NODE_QUEUE.extend(frontiers)

            EXPLORED_NODES.append(node.location)

            # -- BFS END


        pygame.display.flip()
        pygame.display.update()
        FPS_CLOCK.tick(30)







if __name__ == '__main__':
    main()
