#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import curses
class Grid:
    def __init__(self, rows, columns):
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.__num_rows = rows
        self.__num_columns = columns

        self.offsets = ((-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1))

    def update(self):
        newGrid = [[0 for _ in range(self.__num_columns)] for _ in range(self.__num_rows)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                live_neighbors = sum(self.cell_state(nr,nc) for (nr,nc) in map(lambda o: (r+o[0], c+o[1]), self.offsets))

                if self.grid[r][c] and live_neighbors in range(2,4):
                    newGrid[r][c] = 1
                elif not self.grid[r][c] and live_neighbors == 3:
                    newGrid[r][c] = 1
                else:
                    newGrid[r][c] = 0
        self.grid = newGrid


    def __str__(self):
        out = ""
        for row in self.grid:
            for cell in row:
                if cell:
                    out += '█'
                else:
                    out += '░'
            out += "\n"
        return out


    def resize(self, new_r, new_c):
        newGrid = [[0 for _ in range(new_c)] for _ in range(new_r)]

        for i in range(min(self.__num_rows, new_r)):
            for j in range(min(self.__num_columns, new_c)):
                newGrid[i][j] = self.grid[i][j]
        self.grid = newGrid
        self.__num_rows = new_r
        self.__num_columns = new_c


    def cell_state(self, r, c):
        while r >= self.__num_rows:
            r -= self.__num_rows
        while c >= self.__num_columns:
            c -= self.__num_columns
        return self.grid[r][c]
    

        
    def set_alive(self, row, column):
        self.grid[row][column] = 1

    def draw(self, window):
        window.erase()
        for y,row in enumerate(self.grid):
            for x,cell in enumerate(row):
                if cell:
                    window.addstr(y,x,' ', curses.A_STANDOUT)
                else:
                    window.addstr(y,x,' ')
        window.noutrefresh()


