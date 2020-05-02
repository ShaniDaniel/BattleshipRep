import pygame

pygame.init()
x_start_board = 20
x_end_board = 420
y_start_board = 120
y_end_board = 520
screen = pygame.display.set_mode((900, 600))
screen.fill((252, 168, 78))
done = False
board_x = []
board_y = []
clock = pygame.time.Clock()

pygame.display.set_caption("© Battleship by Shani Daniel ©")  # set window title

WHITE = (255, 255, 255)
BLUE = (0,   0, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Cooper Black", 76)  # set font
text = font.render("B a t t l e s h i p", True, BLACK)  # set text


class ShipUI:
    def __init__(self, ship_id, size, ship_coordinates):
        self.ship_id = ship_id
        self.size = size
        self.ship_coordinates = ship_coordinates


class BoardUI:
    cube_and_space = int((x_end_board - x_start_board) / 10)

    @staticmethod
    def print_board():
        for x in range(x_start_board, x_end_board, BoardUI.cube_and_space):
            for y in range(y_start_board, y_end_board, BoardUI.cube_and_space):
                pygame.draw.rect(screen, (217, 217, 217),
                                 pygame.Rect(x+1, y+1, BoardUI.cube_and_space-1, BoardUI.cube_and_space-1))
                if x not in board_x:
                    board_x.append(x)
                if y not in board_y:
                    board_y.append(y)

    @staticmethod
    def print_opponent_board():
        ocx = []
        ocy = []
        for x in range(480, 880, 40):
            for y in range(120, 520, 40):
                pygame.draw.rect(screen, (217, 217, 217), pygame.Rect(x+1, y+1, 39, 39))
                ocx.append(x)
                ocy.append(y)

    @staticmethod
    def DrawX(screen, x_start, y_start, size):
        pygame.draw.line(screen, BLACK, (x_start + 3, y_start + 3), (x_start + size - 3, y_start + (size - 3)), 3)
        pygame.draw.line(screen, BLACK, (x_start + 3, y_start + (size - 3)), (x_start + (size - 3), y_start + 3), 3)

    @staticmethod
    def DrawShip(screen, ship, size_x=29, size_y=68):  # size_x=29, size_y=68
        pygame.draw.ellipse(screen, BLUE, pygame.Rect(ship.x_start + 6, ship.y_start + 6, size_x, size_y))

    @staticmethod
    def DrawDot(screen, x_start, y_start):
        pygame.draw.circle(screen, BLUE, (x_start + 20, y_start + 20), 2)


BoardUI.print_board()
BoardUI.print_opponent_board()



while not done:
    pressed_cube = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:  # check for mouse button click
            pos = pygame.mouse.get_pos()
            for x in range(0, len(board_x)):
                if board_x[x] + 1 <= pos[0] <= board_x[x] + BoardUI.cube_and_space-1:
                    for y in range(0, len(board_y)):
                        if board_y[y] + 1 <= pos[1] <= board_y[y] + BoardUI.cube_and_space-1:
                            print("cube at: ", board_x[x], board_y[y])
                            pressed_cube = (board_x[x], board_y[y])
                            break
                    break

    screen.blit(text, (420 - text.get_width() // 2, 5))

    ship_1 = ShipUI(1, 2, [4, 5])

    pygame.display.flip()
    clock.tick(60)

