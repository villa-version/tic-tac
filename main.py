import pygame, sys


CELL_SIZE = 100
CELL_NUMBER = 3


class Object:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.vec = pygame.math.Vector2(self.x, self.y)
        self.screen = screen

    def draw(self):
        obj = pygame.Rect(int(self.vec.x * CELL_SIZE), int(self.vec.y * CELL_SIZE), CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.rect(self.screen, (255, 213, 0), obj)


class Grid(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        for i in range(2):
            obj = pygame.Rect(int(self.vec.x * CELL_SIZE), int(self.vec.y * CELL_SIZE), CELL_SIZE - 10 * i,
                              CELL_SIZE - 10 * i)
            pygame.draw.rect(self.screen, (111 * (i + 1), 213, 222), obj)


class Zero(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        obj = pygame.Rect(int(self.vec.x * CELL_SIZE), int(self.vec.y * CELL_SIZE), CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.ellipse(self.screen, (111, 111, 222), obj)


class Cross(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.ocupied_blocks = []
        self.spawn_grid()
        self.zeros = []
        self.crosses = []
        self.progress = 'Zero'

    def update(self):
        self.draw_elements()

    def draw_elements(self):
        for block in self.grid:
            block.draw()
        for block in self.ocupied_blocks:
            block.draw()
        for zero in self.zeros:
            zero.draw()
        for cross in self.crosses:
            cross.draw()

    def spawn_zero(self, x, y):
        self.zeros.append(Zero(x, y, self.screen))

    def spawn_cross(self, x, y):
        self.crosses.append(Cross(x, y, self.screen))

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for y in r:
            for x in r:
                self.grid.append(Grid(x, y, self.screen))

    def spawn_ocupied_blocks(self, x, y):
        self.ocupied_blocks.append(Grid(x, y, self.screen))

    def check_press_on_area(self, mx, my):
        for block in self.grid[:]:
            x = block.x * CELL_SIZE
            y = block.y * CELL_SIZE
            if x < mx < x + CELL_SIZE and y < my < y + CELL_SIZE:
                self.spawn_ocupied_blocks(block.x, block.y)
                if self.progress == 'Zero':
                    self.progress = 'Cross'
                    self.spawn_zero(block.x, block.y)
                elif self.progress == 'Cross':
                    self.progress = 'Zero'
                    self.spawn_cross(block.x, block.y)
                self.grid.remove(block)


def main():
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))

    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                main_controller.check_press_on_area(m_pos[0], m_pos[1])

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()


if __name__ == '__main__':
    main()
