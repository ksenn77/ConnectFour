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
