import curses
import time
import math
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


    def _get_game_delay(self):
        """
        Returns real number of seconds for sleep time
        between figure falling steps.
        """
        seconds = 0.080 + 0.800 * pow(0.75, self.level - 1)

        if (seconds < 0.01):
            seconds = 0.01

        return seconds


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
        fast_falling = False

        while not exiting:
            # Create and initialize new figure.
            if not figure:
                figure = self._generate_figure()
                self.screen.move_figure_to_start(figure)

            self.screen.draw(figure)

            time.sleep(self._get_game_delay())
            
            # Keyboard input loop.
            ch = self.screen.getch()

            if ch == curses.ERR:
                # Key was not pressed.
                pass
            elif ch == ord("l") or ch == ord("L"):
                # Move right.
                self.screen.move_figure_right(figure)
            elif ch == ord("h") or ch == ord("H"):
                # Move left.
                self.screen.move_figure_left(figure)
            elif ch == ord("j") or ch == ord("J"):
                # Rotate anticlockwise.
                self.screen.rotate_figure_anticlockwise(figure)
            elif ch == ord("k") or ch == ord("K"):
                # Rotate clockwise.
                self.screen.rotate_figure_clockwise(figure)
            elif ch == ord("f") or ch == ord("F"):
                # Fast falling.
                fast_falling = True
            elif ch == ord("q") or ch == ord("Q"):
                # Quit.
                return

            if not self._fall_down(figure):
                figure = None
                fast_falling = False
            else:
                if fast_falling:
                    while self._fall_down(figure):
                        pass
                    figure = None
                    fast_falling = False


    def _fall_down(self, figure):
        """
        Do one falling down step.
        """
        if not self.screen.move_figure_down(figure):
            lines = self.screen.delete_full_lines()
            score = self._lines_to_score(lines)

            self.lines += lines
            self.score += score

            # TODO: Check if we have to go to the new level.

            self.screen.score = self.score
            self.screen.lines = self.lines
            self.screen.level = self.level

            return False
        else:
            return True


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
