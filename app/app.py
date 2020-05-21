import tkinter as tk
from tkinter import ttk
from functools import partial

from components import Board


class App (tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Tic-Tac-Toe')
        self.geometry('300x300+500+200')
        self.resizable(width=False, height=False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pick_mark()

    def pick_mark(self):
        self.start_frame = ttk.Frame(master=self)
        self.start_frame.grid()
        self.start_frame.grid_rowconfigure(0, weight=1)
        self.start_frame.grid_rowconfigure(1, weight=1)
        self.start_frame.grid_rowconfigure(2, weight=1)
        self.start_frame.grid_columnconfigure(0, weight=1)

        ttk.Label(master=self.start_frame, text='Pick a mark (X starts)', font=('Roboto', '16'))\
            .grid(row=0, column=0, pady=30)
        ttk.Button(master=self.start_frame, text='X', width=20, command=lambda: self.set_player_mark('X'))\
            .grid(row=1, column=0, pady=3)
        ttk.Button(master=self.start_frame, text='O', width=20, command=lambda: self.set_player_mark('O'))\
            .grid(row=2, column=0, pady=3)

    def set_player_mark(self, side):
        self.player_mark = side
        self.start_frame.destroy()
        self.add_board()

    def add_board(self):
        self.board = Board(master=self, size=300, player_mark=self.player_mark)
        self.board.grid()


if (__name__ == '__main__'):
    app = App()
    app.mainloop()
