import curses
import math


class Figure:
    def __init__(self, y=0, x=0):
        """
        Constructor.
        """
        self.current_sprite_index = 0
        self.y = y
        self.x = x


    def _is_window_point(self, width, height, y, x):
        """
        Checks if point belongs to the glass window
        and character can be printed at its position.
        """
        if x < 0 or x > width \
           or y < 0 or y > height:
            return False
        else:
            return True
        

    def draw(self, window, width, height):
        """
        Draw figure on the given window.
        """
        current_sprite = self.sprites[self.current_sprite_index]

        x = self.x - 2
        y = self.y - 2

        for r, row in enumerate(current_sprite):
            for c, cell in enumerate(row):
                if cell > 0:
                    xx = x + c
                    yy = y + r
                    
                    if self._is_window_point(width, height, yy, xx):
                        try:
                            window.move(yy, xx)
                            window.echochar(curses.ACS_BLOCK)
                        except:
                            # We have to catch it for the last character in window.
                            window.refresh()

    
    def rotate_clockwise(self):
        """
        Clockwise rotation.
        """
        self.current_sprite_index = self.get_next_sprite_index()


    def rotate_anticlockwise(self):
        """
        Clockwise rotation.
        """
        self.current_sprite_index = self.get_prev_sprite_index()


    def get_right_edge(self, sprite_index=None):
        """
        Returns X position of the right figure's point in the Glass' coordinates.
        """
        if sprite_index == None:
            sprite_index = self.current_sprite_index
        
        sprite = self.sprites[sprite_index]
        
        fourth = third = 0
        for row in sprite:
            third += row[3]
            fourth += row[4]

        right_edge = self.x

        if fourth > 0:
            right_edge += 2
        elif third > 0:
            right_edge += 1

        return right_edge


    def get_left_edge(self, sprite_index=None):
        """
        Returns X position of the left figure's point in the Glass' coordinates.
        """
        if sprite_index == None:
            sprite_index = self.current_sprite_index
            
        sprite = self.sprites[sprite_index]
        
        first = second = 0
        for row in sprite:
            first += row[0]
            second += row[1]

        left_edge = self.x

        if first > 0:
            left_edge -= 2
        elif second > 0:
            left_edge -= 1

        return left_edge


    def get_next_sprite_index(self, current_index=None):
        """
        Returns next index for the given current index.
        """
        if current_index == None:
            current_index = self.current_sprite_index
            
        current_index += 1
        current_index %= 4 
        return current_index
    

    def get_prev_sprite_index(self, current_index=None):
        """
        Returns previous index for the given current one.
        """
        if current_index == None:
            current_index = self.current_sprite_index
            
        current_index -= 1
        if current_index < 0:
            current_index = 3
            
        return current_index


    def get_bottom_positions(self, sprite_index=None):
        """
        Returns list with y positions of bottom figure's
        borrom points.
        """
        if sprite_index == None:
            sprite_index = self.current_sprite_index
            
        sprite = self.sprites[sprite_index]

        res = [-1, -1, -1, -1, -1]

        for row in range(0, 5):
            for col in range(0, 5):
                if sprite[row][col] > 0:
                    res[col] = self.y - 2 + row

        return res


    def get_sprite(self, sprite_index=None):
        """
        Returns sprite by index or current one if index is not specified.
        """
        if sprite_index == None:
            sprite_index = self.current_sprite_index

        return self.sprites[sprite_index]
