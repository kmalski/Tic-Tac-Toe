import tkinter as tk
from tkinter import ttk


class Field(ttk.Frame):
    def __init__(self, master, size, command):
        super().__init__(master=master, width=size, height=size)

        self.pack_propagate(0)
        self.button = ttk.Button(self, text='', command=command)
        self.button.pack(fill='both', expand=True)

    def is_marked(self):
        return self.button['text'] != ''

    def set_x(self):
        if not self.is_marked():
            self.button['text'] = 'X'
            return True
        return False

    def set_o(self):
        if not self.is_marked():
            self.button['text'] = 'O'
            return True
        return False

    def clear(self):
        self.button['text'] = ''


class Board(ttk.Frame):
    def __init__(self, master, size, **kw):
        super().__init__(master=master, width=size, height=size, **kw)

        self.size = size
        self.field_size = size // 3
        self.mark = 'X'  # X always starts
        self.__add_fields()

    def __add_fields(self):
        self.fields = []
        for i in range(3):
            fields_row = []
            for j in range(3):
                field = Field(master=self, size=self.field_size, command=lambda i=i, j=j: self.__mark_field(i, j))
                field.grid(row=i, column=j)
                fields_row.append(field)
            self.fields.append(fields_row)

    def __trigger_mark(self):
        self.mark = 'X' if self.mark == 'O' else 'O'

    def __mark_field(self, i, j):
        if self.mark == 'X':
            marked = self.fields[i][j].set_x()
        else:
            marked = self.fields[i][j].set_o()

        if marked:
            self.__trigger_mark()

            # TODO: check game state
