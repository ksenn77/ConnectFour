import math
import random
from tabnanny import check

import numpy as np



class ConnectFour:
    def __init__(self):
        self.rows = 6
        self.cols = 7
        self.board = np.zeros((self.rows, self.cols), dtype=int)

    def drop_piece(self, col, piece):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                self.board[r][col] = piece
                return True
        return False

    def is_valid_location(self, col):
        return self.board[self.rows - 1][col] == 0

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.cols):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r

    def evaluate_window(self, window, piece, score):
        opp_piece = (piece + 1) % 2
        count_piece = window.count(piece)
        count_empty = window.count(0)

        if count_piece == 4:
            score += 100
        elif count_piece == 3 and count_empty == 1:
            score += 10
        elif count_piece == 2 and count_empty == 2:
            score += 5

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def is_terminal_node(self):
        return self.check_win(1) or self.check_win(2) or len(
            self.get_valid_locations()) == 0

    def minimax(self, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations()
        if self.is_terminal_node():
            if self.check_win(2):
                return (None, math.inf)
            elif self.check_win(1):
                return (None, -math.inf)
            else:
                return (None, 0)

        if depth == 0:
            return (None, self.score_position(2))

        if maximizing_player:
            score_value = -math.inf
            column = random.choice(valid_locations)
            temp = ConnectFour()
            for c in valid_locations:
                temp.board = self.board.copy()
                temp.drop_piece(c, 2)
                new_score = temp.minimax(depth -1, alpha, beta, False)[1]
                if new_score > score_value:
                    score_value = new_score
                    column = c
                alpha = max(alpha, score_value)
                if alpha >= beta:
                    break
            return column, score_value
        else:
            score_value = math.inf
            column = random.choice(valid_locations)
            temp = ConnectFour()
            for c in valid_locations:
                temp.board = self.board.copy()
                temp.drop_piece(c, 2)
                new_score = temp.minimax(depth - 1, alpha, beta, False)[1]
                if new_score < score_value:
                    score_value = new_score
                    column = c
                beta = min(beta, score_value)
                if alpha >= beta:
                    break
            return column, score_value




    def score_position(self, piece):
        score = 0
        center_array = [int(i) for i in list(self.board[:, self.cols // 2])]
        center_count = center_array.count(piece)
        score += center_count * 6
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.cols - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece, score)

        for c in range(self.cols):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.rows - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece, score)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece, score)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece, score)
        return score

    def pick_best_move(self, piece):
        valid_locations = self.get_valid_locations()
        best_score = -100000
        best_col = random.choice(valid_locations)
        temp = ConnectFour()
        for col in valid_locations:
            temp.board = self.board.copy()
            temp.drop_piece(col, piece)
            score = temp.score_position(piece)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def check_win(self, piece):
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if all(self.board[r, c + i] == piece for i in range(4)): return True

        for r in range(self.rows - 3):
            for c in range(self.cols):
                if all(self.board[r + i, c] == piece for i in range(4)): return True

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if all(self.board[r + i, c + i] == piece for i in range(4)): return True

        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if all(self.board[r - i, c + i] == piece for i in range(4)): return True
        return False

    def print_board(self):
        print(np.flip(self.board, 0))
        print("  0 1 2 3 4 5 6")


def play_console():
    game = ConnectFour()
    game_over = False
    turn = 0

    print("Игра 'Четыре в ряд' началась!")
    game.print_board()

    while not game_over:
        piece = 1 if turn == 0 else 2
        try:
            user_input = input(f"Игрок {piece}, выберите колонку (0-6) или 'q' для выхода: ")
            if user_input.lower() == 'q':
                break

            col = int(user_input)

            if 0 <= col <= 6:
                if game.is_valid_location(col):
                    game.drop_piece(col, piece)
                    game.print_board()

                    if game.check_win(piece):
                        print(f"ПОБЕДА! Игрок {piece} выиграл!")
                        game_over = True

                    turn = (turn + 1) % 2
                else:
                    print("Колонка полна!")
            else:
                print("Число должно быть от 0 до 6.")
        except ValueError:
            print("Ошибка! Введите целое число.")


if __name__ == "__main__":
    play_console()
