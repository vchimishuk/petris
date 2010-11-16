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
