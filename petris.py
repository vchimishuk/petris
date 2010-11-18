import curses
import time
from screen import Screen
from figurei import FigureI


class Petris():
    """
    Application respresentation class.
    """
    def init(self):
        """
        Initialize application.
        """
        self.lines = 0
        self.score = 0
        self.level = 1

        self.screen = Screen()
        self.screen.init()
        self.screen.level = self.level
        self.screen.lines = self.lines


    def destroy(self):
        """
        Free application resources.
        """
        self.screen.destroy()


    def _generate_figure(self):
        """
        Generate next figure to be fallen.
        """
        return FigureI()


    def run(self):
        """
        Run main application loop.
        """
        figure = None
        exiting = False

        while not exiting:
            # Create and initialize new figure.
            if not figure:
                figure = self._generate_figure()
                self.screen.move_figure_to_start(figure)

            self.screen.draw(figure)
            
            # Keyboard input loop.
            ch = self.screen.getch()

            if ch == curses.ERR:
                # Key was not pressed.
                pass
            elif ch == ord("l") or ch == ord("L"):
                # Move right
                self.screen.move_figure_right(figure)
            elif ch == ord("h") or ch == ord("H"):
                # Move left
                self.screen.move_figure_left(figure)
            elif ch == ord("j") or ch == ord("J"):
                # Rotate anticlockwise.
                self.screen.rotate_figure_anticlockwise(figure)
            elif ch == ord("k") or ch == ord("K"):
                # Rotate clockwise.
                self.screen.rotate_figure_clockwise(figure)
            elif ch == ord("a") or ch == ord("A"):
                if not self.screen.move_figure_down(figure):
                    lines = self.screen.delete_full_lines()
                    score = self._lines_to_score(lines)

                    self.lines += lines
                    self.score += score
                    # TODO: Check if we have to go to the new level.

                    self.screen.score = self.score
                    self.screen.lines = self.lines
                    self.screen.level = self.level

                    figure = None
            elif ch == ord("q") or ch == ord("Q"):
                return

            time.sleep(.05)


    def _lines_to_score(self, lines):
        """
        Get scores for the full lines.
        """
        line_score = [0, 40, 100, 300, 1200]
        return line_score[lines] * self.level


def main():
    petris = Petris()
    petris.init()
    
    try:
        petris.run()
    except Exception as err:
        petris.destroy()
        raise err

    petris.destroy()
    

if __name__ == '__main__':
    main()
