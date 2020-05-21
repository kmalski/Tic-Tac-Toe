import tkinter as tk
from tkinter import ttk
from typing import Tuple
from collections import defaultdict
from tkinter import messagebox
from dataclasses import dataclass


@dataclass(eq=True, order=True, frozen=True)
class Move:
    r: int
    c: int


class Player:
    def __init__(self, mark, human=True):
        self.mark = mark
        self.moves = []
        self.human = human
        self.row = [0] * 3
        self.col = [0] * 3
        self.diag = 0
        self.anti_diag = 0

    @classmethod
    def create_opponent(cls, player):
        enemy_mark = 'O' if player.mark == 'X' else 'X'
        return cls(mark=enemy_mark, human=not player.human)

    def starts(self):
        return self.mark == 'X'

    def __str__(self):
        if self.human:
            return 'Player'
        return 'Computer'


class Field(ttk.Frame):
    def __init__(self, master, size, command):
        super().__init__(master=master, width=size, height=size)

        self.pack_propagate(0)
        self.button = ttk.Button(self, text='', command=command)
        self.button.pack(fill='both', expand=True)

    def is_marked(self):
        return self.button['text'] != ''

    def mark(self):
        return self.button['text']

    def set_text(self, mark):
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

        self.player = Player(mark=player_mark)
        self.computer = Player.create_opponent(self.player)

        self.add_fields()

        if not self.player.starts():
            self.ai_make_move()

    def add_fields(self):
        self.fields = []
        for i in range(3):
            fields_row = []
            for j in range(3):
                field = Field(master=self, size=self.field_size, command=lambda i=i, j=j: self.mark_field(i, j))
                field.grid(row=i, column=j)
                fields_row.append(field)
            self.fields.append(fields_row)

    def mark_field(self, i, j):
        marked = self.fields[i][j].set_text(self.player.mark)
        if marked:
            self.player.moves.append(Move(i, j))
            self.check_state(self.player)

            # self.ai_make_move()
            # self.check_state(self.computer)

    def ai_make_move(self):
        pass

    def check_state(self, player):
        r = player.moves[-1].r
        c = player.moves[-1].c
        board_size = 3

        player.row[r] += 1
        player.col[c] += 1
        if r == c:
            player.diag += 1
        if r + c == board_size - 1:
            player.anti_diag += 1

        if (player.row[r] == board_size or player.col[c] == board_size
                or player.diag == board_size or player.anti_diag == board_size):

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
