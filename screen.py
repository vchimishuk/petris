from glass import Glass
from figurei import FigureI
import math
import curses
import time


class Screen():
    """
    Represents drawable part of the terminal,
    where other parts (glass, figures) are drawed.
    """

    glass = None
    
    def init(self):
        """
        Initialize curses.
        """
        # Initialize ncurses library.
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(1)
        curses.curs_set(0)

        self.width = 20
        self.height = 24

        # Draw main window.
        self.window = curses.newwin(self.height, self.width, 0, 0)
        self.window.border()
        self.window.refresh()
        self.window.nodelay(1)

        self.glass = Glass(self)


    def destroy(self):
        """
        Free ncurses library resources and back screen to
        normal mode.
        """
        # Release ncurses.
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        curses.curs_set(1)


    def generate_figure(self):
        """
        Generate next figure to be fallen.
        """
        # Figure shoud appears at the middle top of the glass.
        y = 0
        x = math.floor(self.glass.width / 2)
        return FigureI(y, x)


    def main_loop(self):
        """
        Main application loop, -- handling keyboard events, move figure down and so on.
        """
        figure = self.generate_figure()
        
        while True:
            self.glass.clear()
            figure.draw(self.glass.window, self.glass.width, self.glass.height)

            ch = self.window.getch()
            if ch == curses.ERR:
                # Key was not pressed.
                pass
            elif ch == ord("l") or ch == ord("L"):
                # Move right
                self._move_figure_right(figure)
            elif ch == ord("h") or ch == ord("H"):
                # Move left
                self._move_figure_left(figure)
            elif ch == ord("j") or ch == ord("J"):
                # Rotate anticlockwise.
                self._rotate_figure_anticlockwise(figure)
            elif ch == ord("k") or ch == ord("K"):
                # Rotate clockwise.
                self._rotate_figure_clockwise(figure)
            elif ch == ord("q") or ch == ord("Q"):
                # Quit
                # TODO: Make sure that it is safe and correct.
                return
            
            time.sleep(.05)


    def _move_figure_right(self, figure):
        """
        Move figure one position right.
        """
        if self._is_figure_right_moveable(figure):
            figure.x += 1


    def _move_figure_left(self, figure):
        """
        Move figure one position left.
        """
        if self._is_figure_left_moveable(figure):
            figure.x -= 1


    def _is_figure_right_moveable(self, figure):
        """
        Returns True if this figure can be moved right at least one step.
        """
        right_edge = figure.get_right_edge()
        return right_edge < self.glass.width - 1


    def _is_figure_left_moveable(self, figure):
        """
        Returns True if this figure can be moved left at least one step.
        """
        left_edge = figure.get_left_edge()
        return left_edge > 0


    def _rotate_figure_anticlockwise(self, figure):
        """
        Rotate figure contraclockwise.
        """
        i = figure.get_prev_sprite_index()
        right_edge = figure.get_right_edge(i)
        left_edge = figure.get_left_edge(i)

        if right_edge < self.glass.width and left_edge >= 0:
            figure.rotate_anticlockwise()


    def _rotate_figure_clockwise(self, figure):
        """
        Rotate figure clockwise, if it can be rotated.
        """
        i = figure.get_next_sprite_index()
        right_edge = figure.get_right_edge(i)
        left_edge = figure.get_left_edge(i)

        if right_edge < self.glass.width and left_edge >= 0:
            figure.rotate_clockwise()
