import curses

class Glass:
    """
    Glass class representation. Figures fall into this glass and gravitate to its bottom.
    """
    def __init__(self, screen):
        """
        Constructor.
        """
        self.screen = screen
        # 0, 0 point indicates top left corner.
        self.width = 10
        self.height = 20

        # Place for lees on the bottom of the glass.
        self.lees = [[0 for i in range(0, self.width)] for i in range(0, self.height)]

        self.glass_border = screen.window.subwin(self.height + 2,
                                                 self.width + 2,
                                                 1, 1)
        self.glass_border.border()
        self.glass_border.refresh()

        self.window = screen.window.subwin(self.height, self.width, 2, 2)
        self.window.nodelay(1)
        #self.window.border()
        self.window.refresh()


    def clear(self):
        """
        Clear glass window, -- prepare it for figures printing.
        """
        self.window.erase()


    def draw(self):
        """
        Draw less in the glass.
        """
        for y, row in enumerate(self.lees):
            for x, cel in enumerate(row):
                if cel > 0:
                    try:
                        self.window.move(y, x)
                        self.window.echochar(curses.ACS_BLOCK)
                    except:
                        self.window.refresh()

    
    def get_lees_top(self, x):
        """
        Returns y of lees top at the specified x position.
        """
        top = self.height

        if x < 0 or x >= self.width:
            return top
        
        for row in range(self.height - 1, -1, -1):
            if self.lees[row][x] > 0:
                top = row

        return top


    def lees_figure(self, figure):
        """
        Add figure to lees.
        """
        sprite = figure.get_sprite()
        
        for y, row in enumerate(sprite):
            for x, cel in enumerate(row):
                if cel > 0:
                    self.lees[figure.y - 2 + y][figure.x - 2 + x] = 1


    def is_space_free(self, y, x):
        """
        Returns True if fiven point free from lees.
        """
        if y < 0 or y >= self.height \
           or x < 0 or x >= self.width:
            return True
        
        return self.lees[y][x] == 0


    def delete_full_lines(self):
        """
        Remove full lines and return score.
        """
        deleted_lines = 0
        y = self.height - 1
        while y >= 0:
            if self._is_line_full(y):
                self._remove_line(y)
                deleted_lines += 1
            else:
                y -= 1

        return deleted_lines
                    

    def _remove_line(self, y):
        """
        Remove full line. All cells above will be moved one position down.
        """
        for x in range(0, self.width):
            # Empty this line.
            self.lees[y][x] = 0

            # Make upper lines "fall" down.
            for yy in range(y, -1, -1):
                if yy > 0:
                    cel = self.lees[yy -1][x]
                else:
                    cel = 0
                                        
                self.lees[yy][x] = cel


    def _is_line_full(self, y):
        """
        Returns True if specified line is full.
        """
        for cel in self.lees[y]:
            if cel == 0:
                return False

        return True
