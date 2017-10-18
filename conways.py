#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#######################################
#
# Conway's Game of Life
# Implemented by Ben Mastay
#
#######################################

import curses
import game_io 
import grid



def init_game(game_win):
    y,x = game_win.getmaxyx()
    g = grid.init_random_grid(y, x-1)
    return g

def resize_game(game_win, grid):
    y,x = game_win.getmaxyx()
    grid.resize(y,x-1)
    return grid

def game_main(stdscr):

    game_win, legend_win = game_io.init_windows(stdscr)
    grid = init_game(game_win)
    while True:
        cmd = game_loop(stdscr, game_win, grid, legend_win)

        if cmd == "RESTART":
            game_win, legend_win = game_io.init_windows(stdscr)
            grid = init_game(game_win)
        elif cmd == "RESIZE":
            game_win, legend_win = game_io.init_windows(stdscr)
            grid = resize_game(game_win, grid)
        else:
            break

def game_loop(stdscr, game_win, grid, legend_win):
    g = grid
    paused = False
    stdscr.nodelay(True)
    while True:
        c = stdscr.getch()
        if c == ord('q'):
            return None
        elif c == ord('p'):
            paused = not paused
        elif c == ord('r'):
            return "RESTART"
        elif c == curses.KEY_RESIZE:
            return "RESIZE"
        elif not paused:
            g.update()
            game_io.draw_grid(g, game_win)
            legend_win.noutrefresh()
            curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(game_main)



