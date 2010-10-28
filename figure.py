import curses
import math

class Figure:
    def __init__(self, glass):
        """
        Constructor.
        """
        self.current_sprite_index = 0
        self.glass = glass
        # Put me at the middle top of the glass.
        self.y = 0
        self.x = math.floor(glass.width / 2)


    def _is_window_point(self, y, x):
        """
        Checks if point belongs to the glass window
        and character can be printed at its position.
        """
        if x < 0 or x > self.glass.width \
           or y < 0 or y > self.glass.height:
            return False
        else:
            return True
        

    def draw(self):
        """
        Draw figure on the glass.
        """
        current_sprite = self.sprites[self.current_sprite_index]

        x = self.x - 2
        y = self.y - 2

        for r, row in enumerate(current_sprite):
            for c, cell in enumerate(row):
                if cell > 0:
                    xx = x + c
                    yy = y + r
                    
                    if self._is_window_point(yy, xx):
                        self.glass.window.move(yy, xx)
                        self.glass.window.echochar(curses.ACS_BLOCK)

    
    def rotate_clockwise(self):
        """
        Clockwise rotation.
        """
        if _is_clockwise_rotateable():
            self.current_sprite_index += 1
            self.current_sprite_index %= 4 


    def rotate_anticlockwise(self):
        """
        Contraclockwise rotation.
        """
        if _is_anticlockwise_rotateable():
            self.current_sprite_index += 1
            if self.current_sprite_index < 0:
                self.current_sprite_index = 3


    def move_right(self):
        """
        Move figure one position right.
        """
        if self._is_right_moveable():
            self.x += 1


    def move_left(self):
        """
        Move figure one position left.
        """
        if self._is_left_moveable():
            self.x -= 1


    def _is_right_moveable(self):
        """
        Returns True if this figure can be moved right at least one step.
        """
        current_sprite = self.sprites[self.current_sprite_index]

        fourth = third = 0
        for row in current_sprite:
            third += row[3]
            fourth += row[4]

        right_edge = self.x

        if fourth > 0:
            right_edge += 2
        elif third > 0:
            right_edge += 1

        return right_edge < self.glass.width - 1


    def _is_left_moveable(self):
        """
        Returns True if this figure can be moved left at least one step.
        """
        current_sprite = self.sprites[self.current_sprite_index]

        first = second = 0
        for row in current_sprite:
            first += row[0]
            second += row[1]

        left_edge = self.x

        if first > 0:
            left_edge -= 2
        elif second > 0:
            left_edge -= 1

        return left_edge > 0
