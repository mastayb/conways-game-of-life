#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import curses
import itertools

def wrapped_range(start, stop, limit, minimum=0):
    #generator that wraps at 0 and limit
    for i in range(start,0):
        yield limit+i
    for i in range(max(start,0), min(stop,limit)):
        yield i
    for i in range(limit, stop):
        yield i-limit


def wrapped_neighbor_range(r,c,rows,columns):
    for nr in wrapped_range(r-1,r+2,rows):
        for nc in wrapped_range(c-1,c+2,columns):
            if (nr,nc) == (r,c):
                continue
            else:
                yield (nr,nc)

class Grid:
    def __init__(self, rows, columns):
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.__num_rows = rows
        self.__num_columns = columns

    def update(self):
        newGrid = [[0 for _ in range(self.__num_columns)] for _ in range(self.__num_rows)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                live_neighbors = sum(self.grid[nr][nc] 
                        for (nr,nc) in wrapped_neighbor_range(r,c,self.__num_rows, self.__num_columns)) 

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


