from glass import Glass
import math
import curses


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

        self.width = 40 # 14
        self.height = 30 # 20

        self.level = 1
        self.score = 0
        self.lines = 0

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


    def move_figure_to_start(self, figure):
        """
        Move figure to start position.
        Figure shoud appears at the middle top of the glass.
        """
        figure.y = 0
        figure.x = math.floor(self.glass.width / 2)


    def draw(self, figure):
        """
        Redraw the screen.
        """
        x = self.glass.width + 4
        self.window.move(10, x)
        self.window.addstr("Score:" + "{0:>6}".format(self.score))
        self.window.move(11, x)
        self.window.addstr("Lines:" + "{0:>6}".format(self.lines))
        self.window.move(12, x)
        self.window.addstr("Level:" + "{0:>6}".format(self.level))
        
        
        self.glass.clear()
        self.glass.draw()
        
        figure.draw(self.glass.window, self.glass.width, self.glass.height)

        
    def getch(self):
        """
        Return pressed key.
        """
        return self.window.getch()
    

    def move_figure_down(self, figure):
        """
        Move figure down for one position, -- falling.
        Returns False if figure was joined to lees.
        """
        if self._is_figure_down_moveable(figure):
            figure.y += 1
            return True
        else:
            # Figure should be joined to lees.
            self.glass.lees_figure(figure)
            return False


    def _is_figure_down_moveable(self, figure):
        """
        Returns True if figure can be moved down.
        """
        bottoms = figure.get_bottom_positions()

        for i, y in enumerate(bottoms):
            lees_top = self.glass.get_lees_top(figure.x - 2 + i)
            if y >= lees_top - 1 or y >= self.glass.height:
                return False

        return True


    def move_figure_right(self, figure):
        """
        Move figure one position right.
        """
        if self._is_figure_right_moveable(figure):
            figure.x += 1


    def move_figure_left(self, figure):
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
        sprite = figure.get_sprite()
        return right_edge < self.glass.width - 1 and self._is_space_free(figure.y, figure.x + 1, sprite)


    def _is_figure_left_moveable(self, figure):
        """
        Returns True if this figure can be moved left at least one step.
        """
        left_edge = figure.get_left_edge()
        sprite = figure.get_sprite()
        return left_edge > 0 and self._is_space_free(figure.y, figure.x - 1, sprite)
    

    def rotate_figure_anticlockwise(self, figure):
        """
        Rotate figure contraclockwise.
        """
        i = figure.get_prev_sprite_index()

        # We can't rotate if figure will be outside the glass.
        right_edge = figure.get_right_edge(i)
        left_edge = figure.get_left_edge(i)
        if right_edge >= self.glass.width or left_edge < 0:
            return

        # Or figure will be under the glass's floor.
        bottoms = figure.get_bottom_positions(i)
        for y in bottoms:
            if y >= self.glass.height:
                return

        # And we have free place for future sprite.
        i = figure.get_prev_sprite_index()
        sprite = figure.get_sprite(i)
        if not self._is_space_free(figure.y, figure.x, sprite):
            return        
            
        figure.rotate_anticlockwise()


    def rotate_figure_clockwise(self, figure):
        """
        Rotate figure clockwise, if it can be rotated.
        """
        i = figure.get_next_sprite_index()

        # Block rotation if figure will be moved outside the glass.
        right_edge = figure.get_right_edge(i)
        left_edge = figure.get_left_edge(i)
        if right_edge >= self.glass.width or left_edge < 0:
            return

        # Or under the floor.
        bottoms = figure.get_bottom_positions(i)
        for y in bottoms:
            if y >= self.glass.height:
                return

        # And we have free place for the next sprite.
        i = figure.get_next_sprite_index()
        sprite = figure.get_sprite()
        if not self._is_space_free(figure.y, figure.x, sprite):
            return
                
        figure.rotate_clockwise()


    def _is_space_free(self, y, x, sprite):
        """
        Returns True if space for the given sprite is fee (without lees) in glass.
        """
        for yy, row in enumerate(sprite):
            for xx, cel in enumerate(row):
                if cel > 0:
                    if not self.glass.is_space_free(y - 2 + yy, x - 2 + xx):
                        return False

        return True


    def delete_full_lines(self):
        """
        Remove full lines and returns their count.
        """
        return self.glass.delete_full_lines()

