import pygame
from include.colors import COLORS
from include.constants import DIMENSIONS
from include.constants import MOUSE_BUTTONS


def main():
    # initial parameters

    START_NODE = (0, 0)
    END_NODE = (1, 1)

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
                            handle_cell_click((j, i), event.button)

        window_surface.blit(background, (0, 0))

        for i in range(len(cells)):
            for j in range(len(cells)):
                if START_NODE == (j, i):
                    pygame.draw.rect(window_surface, COLORS['START'], cells[i][j], border_radius=2)
                elif END_NODE == (j, i):
                    pygame.draw.rect(window_surface, COLORS['END'], cells[i][j], border_radius=2)
                else:
                    pygame.draw.rect(window_surface, COLORS['CELL'], cells[i][j], border_radius=2)

        pygame.display.flip()
        pygame.display.update()
        FPS_CLOCK.tick(30)


if __name__ == '__main__':
    main()
