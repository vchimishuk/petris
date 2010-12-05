import curses
import time
import math
import random
from screen import Screen
from figurei import FigureI
from figureo import FigureO
from figurel import FigureL
from figurej import FigureJ
from figuret import FigureT
from figures import FigureS
from figurez import FigureZ


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

        random.seed()

        self.figures = []
        self.figures.append(FigureI())
        self.figures.append(FigureO())
        self.figures.append(FigureL())
        self.figures.append(FigureJ())
        self.figures.append(FigureT())
        self.figures.append(FigureS())
        self.figures.append(FigureZ())


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
        return self.figures[random.randint(0, len(self.figures) - 1)]


    def run(self):
        """
        Run main application loop.
        Return True if game was aborted by user, or False if he lose the game.
        """
        figure = None
        exiting = False
        fast_falling = False
        paused = False
        sleep_time = 0
        # Sleep with little portions to make keyboard more interactive.
        sleep_chunk = 0.2

        next_figure = self._generate_figure()
        
        while not exiting:
            # Create and initialize new figure.
            if not figure:
                figure = next_figure
                self.screen.move_figure_to_start(figure)

                next_figure = self._generate_figure()
                self.screen.set_next_figure(next_figure)

            self.screen.draw(figure)

            if sleep_time <= 0:
                sleep_time = self._get_game_delay()

            if sleep_time > sleep_chunk:
                sleep_time -= sleep_chunk
                time.sleep(sleep_chunk)
            else:
                time.sleep(sleep_time)
                sleep_time = 0
            
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
            elif ch == ord("p") or ch == ord("P"):
                # Pause.
                paused = not paused
                if paused:
                    self.screen.status = "PAUSED"
                else:
                    self.screen.status = None
            elif ch == ord("q") or ch == ord("Q"):
                # Quit.
                return True

            if paused:
                continue

            if sleep_time == 0 and not self._fall_down(figure):
                figure = None
                fast_falling = False
            else:
                if fast_falling:
                    while self._fall_down(figure):
                        pass
                    figure = None
                    fast_falling = False

            # Check for the end of game.
            if figure == None and self.screen.glass.is_full():
                # Quit
                return False
                                

    def _fall_down(self, figure):
        """
        Do one falling down step.
        """
        if not self.screen.move_figure_down(figure):
            lines = self.screen.delete_full_lines()
            score = self._lines_to_score(lines)

            self.lines += lines
            self.score += score

            self.level = int(1 + self.lines / 10)

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
        status = petris.run()
        petris.destroy()

        if not status:
            print("Ha-ha! You lose.");
        else:
            print("Why you don't wonna play with me no more?")

        print()
        print("Score:" + "{0:>6}".format(petris.screen.score))
        print("Lines:" + "{0:>6}".format(petris.screen.lines))
        print("Level:" + "{0:>6}".format(petris.screen.level))

    except Exception as err:
        petris.destroy()
        raise err


if __name__ == '__main__':
    main()
