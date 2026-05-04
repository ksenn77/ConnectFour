import random

import pygame
import sys
import math
from game_logic import ConnectFour

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

SQUARESIZE = 77
WIDTH = 7 * SQUARESIZE
HEIGHT = (6 + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
RADIUS = int(SQUARESIZE / 2 - 5)

PLAYER = 0
BOT = 1
PIECE_PlAYER = 1
PIECE_BOT = 2

def draw_board(board, screen):
    for c in range(7):
        for r in range(6):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(7):
        for r in range(6):
            if board[r][c] == PIECE_PlAYER:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == PIECE_BOT:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def display_winner(screen, winner_text, color):
    pygame.font.init()
    font = pygame.font.SysFont("monospace", 55, bold=False)
    label = font.render(winner_text, True, color)
    label_rect = label.get_rect(center=(WIDTH // 2, SQUARESIZE // 2))
    screen.blit(label, label_rect)
    pygame.display.update()


def run_game():
    pygame.init()
    game = ConnectFour()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect Four: GUI Edition")

    game_over = False
    draw_board(game.board, screen)

    turn = random.randint(0,1)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                color = RED
                pygame.draw.circle(screen, color, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))

                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if game.is_valid_location(col):
                        game.drop_piece(col, PIECE_PlAYER)

                        if game.check_win(PIECE_PlAYER):
                            draw_board(game.board, screen)
                            display_winner(screen, "Красный выиграл", RED)
                            game_over = True

                        turn = (turn + 1) % 2

        # if turn == PLAYER and not game_over:
        #
        #     #col = random.randint(0,6)
        #     #col = game.pick_best_move(PIECE_BOT)
        #     col, minimax_score = game.minimax(5,-math.inf, math.inf, True)
        #     if game.is_valid_location(col):
        #         game.drop_piece(col, PIECE_PlAYER)
        #
        #         if game.check_win(PIECE_PlAYER):
        #             draw_board(game.board, screen)
        #             display_winner(screen, "Красный выиграл", RED)
        #             game_over = True
        #
        #         turn = (turn + 1) % 2
        #         draw_board(game.board, screen)

        if turn == BOT and not game_over:

            #col = random.randint(0,6)
            #col = game.pick_best_move(PIECE_BOT)
            col, minimax_score = game.minimax(5,-math.inf, math.inf, True)
            if game.is_valid_location(col):
                game.drop_piece(col, PIECE_BOT)

                if game.check_win(PIECE_BOT):
                    draw_board(game.board, screen)
                    display_winner(screen, "Желтый выиграл", YELLOW)
                    game_over = True

                turn = (turn + 1) % 2
                draw_board(game.board, screen)

    pygame.time.wait(3000)


if __name__ == "__main__":
    run_game()
