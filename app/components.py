import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from players import Human, Computer, Move


class Field(ttk.Frame):
    def __init__(self, master, size, command):
        super().__init__(master=master, width=size, height=size)

        self.pack_propagate(0)
        self.button = ttk.Button(self, text='', command=command)
        self.button.pack(fill='both', expand=True)

    def is_marked(self):
        return self.button['text'] != ''

    def get_mark(self):
        return self.button['text']

    def set_mark(self, mark):
        if not self.is_marked():
            self.button['text'] = mark
            return True
        return False

    def clear(self):
        self.button['text'] = ''


class Board(ttk.Frame):
    def __init__(self, master, size, player_mark, **kw):
        super().__init__(master=master, width=size, height=size, **kw)

        self.size = size
        self.field_size = size // 3
        self.moves_count = 0

        self.human = Human(mark=player_mark, board=self)
        self.computer = self.human.create_opponent()

        self.add_fields()

    def add_fields(self):
        self.fields = []
        for i in range(3):
            fields_row = []
            for j in range(3):
                field = Field(master=self, size=self.field_size, command=lambda i=i, j=j: self.next_turn(i, j))
                field.grid(row=i, column=j)
                fields_row.append(field)
            self.fields.append(fields_row)

    def next_turn(self, i, j):
        if self.human.make_move(i, j):
            curr_status = self.check_game_status(self.human)

            if curr_status is None:
                self.computer.make_move()
                self.check_game_status(self.computer)

    def check_game_status(self, player):
        if self.moves_count == 9:
            self.display_result('Nobody')
            return 'Draw'

        r = player.moves[-1].i
        c = player.moves[-1].j
        board_size = 3

        player.row[r] += 1
        player.col[c] += 1
        if r == c:
            player.diag += 1
        if r + c == board_size - 1:
            player.anti_diag += 1

        if (player.row[r] == board_size or player.col[c] == board_size
                or player.diag == board_size or player.anti_diag == board_size):
            self.display_result(player)
            return str(player)

        return None

    def display_result(self, player):
        if messagebox.askyesno(f'{player} won!', f'{player} won!\nDo you wish to play again?'):
            self.new_game()
        else:
            self.end_game()

    def new_game(self):
        self.grid_remove()
        self.master.pick_mark()
        self.destroy()

    def end_game(self):
        self.master.destroy()

    def to_matrix(self):
        matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(self.fields[i][j].get_mark())
            matrix.append(row)

        return matrix
