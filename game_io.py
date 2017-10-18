
import curses

def draw_grid(grid, window):
    window.erase()
    for y,row in enumerate(grid):
        for x,cell in enumerate(row):
            if cell:
                window.addstr(y,x,' ', curses.A_STANDOUT)
            else:
                window.addstr(y,x,' ')
    window.noutrefresh()


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



def io_loop(stdscr, game_win, legend_win, output_q, input_q):
    stdscr.nodelay(True)

    def draw_screen(grid):
        draw_grid(grid, game_win)
        legend_win.noutrefresh()
        curses.doupdate()


    while True:
        c = stdscr.getch()
        if c == ord('q'):
            input_q.put("Quit")
            break
        elif c == ord('p'):
            input_q.put("PAUSE")
        elif c == ord('r'):
            input_q.put("RESTART")
        elif c == curses.KEY_RESIZE:
            input_q.put("RESIZE")
            break
        
        if not output_q.empty():
            g = output_q.get()
            draw_screen(g)



