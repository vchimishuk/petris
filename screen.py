from figurei import FigureI
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
        return FigureI(self.glass)


    def main_loop(self):
        """
        Main application loop, -- handling keyboard events, move figure down and so on.
        """
        figure = self.generate_figure()
        
        while True:
            #self.glass.window.clear()
            #self.glass.window.redrawwin()

            self.glass.clear()
            figure.draw()

            #self.glass.window.refresh()


            ch = self.window.getch() #self.window.getch()
            if ch == curses.ERR:
               pass # Key was not pressed.
            elif ch == ord("l") or ch == ord("L"):
                # Right
                figure.move_right()
            elif ch == ord("h") or ch == ord("H"):
                # Left
                figure.move_left()
            elif ch == ord("q") or ch == ord("Q"):
                # Quit
                # TODO: Make sure that it is safe and correct.
                return
            
            time.sleep(.1)
