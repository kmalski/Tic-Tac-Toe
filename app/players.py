from dataclasses import dataclass
from abc import ABC, abstractmethod
from math import inf


@dataclass(eq=True, order=True, frozen=True)
class Move:
    i: int
    j: int


class Player(ABC):
    def __init__(self, mark, board):
        self.board = board
        self.mark = mark
        self.moves = []
        self.row = [0] * 3
        self.col = [0] * 3
        self.diag = 0
        self.anti_diag = 0

    def starts(self):
        return self.mark == 'X'

    @abstractmethod
    def __str__(self):
        pass


class Human(Player):
    def __init__(self, mark, board):
        super().__init__(mark, board)

    def __str__(self):
        return 'Player'

    def create_opponent(self):
        enemy_mark = 'O' if self.mark == 'X' else 'X'
        return Computer(mark=enemy_mark, board=self.board, enemy=self)

    def make_move(self, i, j):
        if self.board.fields[i][j].set_mark(self.mark):
            self.board.moves_count += 1
            self.moves.append(Move(i, j))
            return True
        return False


class Computer(Player):
    def __init__(self, mark, board, enemy):
        super().__init__(mark, board)

        self.enemy = enemy
        self.scores = {self.mark: 10, self.enemy.mark: -10, 'Draw': 0}

    def __str__(self):
        return 'Computer'

    def make_move(self):
        fields = self.board.to_matrix()
        best_score = -inf
        move = None

        for i in range(3):
            for j in range(3):
                if fields[i][j] == '':
                    fields[i][j] = self.mark
                    score = self.minimax(fields, False)
                    fields[i][j] = ''
                    if score > best_score:
                        best_score = score
                        move = Move(i, j)

        self.board.moves_count += 1
        self.board.fields[move.i][move.j].set_mark(self.mark)
        self.moves.append(move)

    def minimax(self, fields, is_maximizing):
        res = self.check_winner(fields)
        if res is not None:
            return self.scores[res]

        if is_maximizing:
            best_score = -inf
            for i in range(3):
                for j in range(3):
                    if fields[i][j] == '':
                        fields[i][j] = self.mark
                        score = self.minimax(fields, False)
                        fields[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = inf
            for i in range(3):
                for j in range(3):
                    if fields[i][j] == '':
                        fields[i][j] = self.enemy.mark
                        score = self.minimax(fields, True)
                        fields[i][j] = ''
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self, fields):
        # horizontal
        for i in range(3):
            if fields[i][0] == fields[i][1] == fields[i][2] != '':
                return fields[i][0]

        # vertical
        for i in range(3):
            if fields[0][i] == fields[1][i] == fields[2][i] != '':
                return fields[0][i]

        # diagonals
        if fields[0][0] == fields[1][1] == fields[2][2] != '':
            return fields[0][0]
        if fields[2][0] == fields[1][1] == fields[0][2] != '':
            return fields[2][0]

        # open spots
        for row in fields:
            for field in row:
                if field == '':
                    return None

        return 'Draw'

    def make_first_move(self):
        move = Move(1, 1)
        self.board.moves_count += 1
        self.board.fields[move.i][move.j].set_mark(self.mark)
        self.moves.append(move)
