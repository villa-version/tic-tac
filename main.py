import pygame, sys


CELL_SIZE = 100
CELL_NUMBER = 3
SIGN_ZERO = 'o'
SIGN_CROSS = 'x'


class Object:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.vec = pygame.math.Vector2(self.x, self.y)
        self.screen = screen


class Grid(Object):
    def __init__(self, x, y, screen, occupied):
        Object.__init__(self, x, y, screen)
        self.occupied = occupied

    def draw(self):
        for i in range(2):
            obj = pygame.Rect(int(self.vec.x * CELL_SIZE), int(self.vec.y * CELL_SIZE), CELL_SIZE - 10 * i,
                              CELL_SIZE - 10 * i)
            pygame.draw.rect(self.screen, (111 * (i + 1), 213, 222), obj)


class Zero(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        pygame.draw.circle(self.screen, (111, 111, 222),
                           ((self.vec.x + 1/2) * CELL_SIZE - 5, (self.vec.y + 1/2) * CELL_SIZE - 5),
                           CELL_SIZE/2 - 5)
        # (self.vec.x + 1/2) * CELL_SIZE = self.vec.x * CELL_SIZE + CELL_SIZE/2


class Cross(Object):
    def __init__(self, x, y, screen):
        Object.__init__(self, x, y, screen)

    def draw(self):
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.vec.x * CELL_SIZE, self.vec.y * CELL_SIZE),
                         (self.vec.x * CELL_SIZE + CELL_SIZE - 10, self.vec.y * CELL_SIZE + CELL_SIZE - 10))
        pygame.draw.line(self.screen, (0, 0, 0),
                         (self.vec.x * CELL_SIZE + CELL_SIZE - 10, self.vec.y * CELL_SIZE),
                         (self.vec.x * CELL_SIZE, self.vec.y * CELL_SIZE + CELL_SIZE - 10))


class MainController:
    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.copied_grid = self.grid
        self.zeros = []
        self.crosses = []
        self.progress = SIGN_ZERO

    def update(self):
        self.draw_elements()

    def draw_elements(self):
        for row in self.grid:
            for block in row:
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
        for _ in r:
            self.grid.append([])
        for y in r:
            for x in r:
                self.grid[y].append(Grid(x, y, self.screen, ''))

    def check_press_on_area(self, mx, my):
        for row in self.grid[:]:
            for block in row:
                x = block.x * CELL_SIZE
                y = block.y * CELL_SIZE
                if x < mx < x + CELL_SIZE and y < my < y + CELL_SIZE:
                    if block.occupied != '':
                        pass
                    else:
                        if self.progress == SIGN_ZERO:
                            self.progress = SIGN_CROSS
                            self.spawn_zero(block.x, block.y)
                            block.occupied = SIGN_ZERO
                        elif self.progress == SIGN_CROSS:
                            self.progress = SIGN_ZERO
                            self.spawn_cross(block.x, block.y)
                            block.occupied = SIGN_CROSS

    def check_win(self):
        for sign in (SIGN_CROSS, SIGN_ZERO):
            for col in range(CELL_NUMBER):
                if self.grid[col][0].occupied == sign and self.grid[col][1].occupied == sign and self.grid[col][2].occupied == sign:
                    return sign
            for elem in range(CELL_NUMBER):
                if self.grid[0][elem].occupied == sign and self.grid[1][elem].occupied == sign and self.grid[2][elem].occupied == sign:
                    return sign
            if self.grid[0][0].occupied == sign and self.grid[1][1].occupied == sign and self.grid[2][2].occupied == sign:
                return sign
            elif self.grid[2][0].occupied == sign and self.grid[1][1].occupied == sign and self.grid[2][0].occupied == sign:
                return sign


def main():
    name = "Tic-Tac"
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
    pygame.display.set_caption(name)

    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                main_controller.check_press_on_area(m_pos[0], m_pos[1])
                result = main_controller.check_win()
                if result == SIGN_CROSS:
                    print('CROSS WON')
                    pygame.quit()
                    sys.exit()
                elif result == SIGN_ZERO:
                    print('ZEROS WON')
                    pygame.quit()
                    sys.exit()

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()


if __name__ == '__main__':
    main()
