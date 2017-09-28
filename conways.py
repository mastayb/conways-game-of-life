#!/usr/bin/env python

#######################################
#
# Conway's Game of Life
# Implemented by Ben Mastay
#
#######################################

import time

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
                out += str(cell) + " "
            out += "\n"
        return out
        
    def set_alive(self, row, column):
        self.grid[row][column] = 1


                
if __name__ == "__main__":
    g = Grid(5,5)

    g.set_alive(4,2)
    g.set_alive(0,2)
    g.set_alive(1,2)

    while(True):
        g.update()
        print(g)
        time.sleep(1)


