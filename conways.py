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
from grid import Grid

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


def print_legend(window):
    legend = "Q : quit    P : pause   R : restart"
    y,x = window.getmaxyx()
    window.addstr(y//2,x//2-len(legend)//2, legend)


def init_windows(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    screen_y,screen_x = stdscr.getmaxyx()
    legend_y = 1
    game_win_y, game_win_x = screen_y-legend_y, screen_x

    game_win = curses.newwin(game_win_y, game_win_x, 0,0)
    legend_win = curses.newwin(legend_y, game_win_x, game_win_y,0)
    print_legend(legend_win)
    return game_win, legend_win

def init_game(game_win):
    y,x = game_win.getmaxyx()
    g = init_random_grid(y, x-1)
    return g

def resize_game(game_win, grid):
    y,x = game_win.getmaxyx()
    grid.resize(y,x-1)
    return grid

def game_main(stdscr):

    game_win, legend_win = init_windows(stdscr)
    grid = init_game(game_win)
    while True:
        cmd = game_loop(stdscr, game_win, grid, legend_win)

        if cmd == "RESTART":
            game_win, legend_win = init_windows(stdscr)
            grid = init_game(game_win)
        elif cmd == "RESIZE":
            game_win, legend_win = init_windows(stdscr)
            grid = resize_game(game_win, grid)
        else:
            break
            

def game_loop(stdscr, game_win, grid, legend_win):
    g = grid
    stdscr.nodelay(True)
    paused = False
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
            g.draw(game_win)
            legend_win.noutrefresh()
#            time.sleep(.05)
            curses.doupdate()

if __name__ == "__main__":
    curses.wrapper(game_main)



