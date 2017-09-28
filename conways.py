#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#######################################
#
# Conway's Game of Life
# Implemented by Ben Mastay
#
#######################################

import time
import curses
import random

def wrap(x, max_x):
    if x < 0:
        return max_x+1 - ((-x)%max_x)
    if x > max_x:
        return x % (max_x+1)
    return x

def wrap_coord(coord, max_coord):
    return [wrap(x, max_x) for x, max_x in zip(coord, max_coord)]
        

def get_wrapped_neighbors(row, column, num_rows, num_columns):
    return [wrap_coord((r,c),(num_rows-1, num_columns-1)) 
            for r,c in get_neighbors(row, column)]

def get_neighbors(row, column):
    return [(r,c) for r in range(row-1,row+2)
            for c in range(column-1,column+2)
            if (r,c) != (row,column)]


class Grid:
    def __init__(self, rows, columns):
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.__num_rows = rows
        self.__num_columns = columns

    def get_cell_neighbors(self, r,c):
        return get_wrapped_neighbors(r, c, self.__num_rows, self.__num_columns)

    def update(self):
        newGrid = [[0 for _ in range(self.__num_columns)] for _ in range(self.__num_rows)]

        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                live_neighbors = sum(self.grid[nr][nc] for (nr,nc) in self.get_cell_neighbors(r,c))

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
                #out += str(cell) + " "
            out += "\n"
        return out


        
    def set_alive(self, row, column):
        self.grid[row][column] = 1

    def draw(self, window):
        window.clear()
        curses.curs_set(0)

        for y,row in enumerate(self.grid):
            for x,cell in enumerate(row):
                if cell:
                    window.addstr(y,x,' ', curses.A_STANDOUT)
                else:
                    window.addstr(y,x,' ')
        window.refresh()



def init_random_grid(r,c):
    g = Grid(r,c)
    for _ in range(random.randint(0, r*c)):
        g.set_alive(random.randint(0,r-1), random.randint(0,c-1))
    return g





def init_glider(r,c):
    g = Grid(r,c)
    g.set_alive(0,1)
    g.set_alive(1,2)
    g.set_alive(2,0)
    g.set_alive(2,1)
    g.set_alive(2,2)
    return g

def game_main(stdscr):
    rows, columns = stdscr.getmaxyx()
    g = init_random_grid(rows-1, columns-1)
    game_loop(stdscr, g)


def game_loop(stdscr, grid):
    while True:
        grid.update()
        grid.draw(stdscr)
#        time.sleep(0.1)

                
if __name__ == "__main__":
    curses.wrapper(game_main)



