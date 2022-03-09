import pygame
from colors import COLORS
from constants import DIMENSIONS


def main():
    # initial parameters

    # start -> end
    MODE = 'start'
    START_NODE = (0, 0)

    # handling cell click
    def handle_cell_click(cell_location):
        x, y = cell_location

        if MODE == 'start':
            nonlocal START_NODE
            START_NODE = (j, i)

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

    while is_running:

        # event handlers
        for event in pygame.event.get():

            # quitting the sim
            if event.type == pygame.QUIT:
                is_running = False

            # if mouse has been clicked
            if event.type == pygame.MOUSEBUTTONDOWN:

                # TODO: Replace this with a neater comprehension

                # finding out which cell has been clicked
                for i in range(len(cells)):
                    for j in range(len(cells[0])):
                        if cells[i][j].collidepoint(event.pos):
                            handle_cell_click((j, i))

        window_surface.blit(background, (0, 0))

        for i in range(len(cells)):
            for j in range(len(cells)):

                # TODO: Replace this with get_cell_color later

                if START_NODE == (j, i):
                    pygame.draw.rect(window_surface, COLORS['OBSTACLE'], cells[i][j], border_radius=2)
                else:
                    pygame.draw.rect(window_surface, COLORS['CELL'], cells[i][j], border_radius=2)
        #
        # for row in cells:
        #     for cell in row:
        #         pygame.draw.rect(window_surface, COLORS['CELL'], cell)

        pygame.display.flip()
        pygame.display.update()
        FPS_CLOCK.tick(30)


if __name__ == '__main__':
    main()
