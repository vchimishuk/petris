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
    
    
