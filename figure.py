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
        if self._is_clockwise_rotateable():
            self.current_sprite_index = self._get_next_sprite_index(self.current_sprite_index)


    def rotate_anticlockwise(self):
        """
        Contraclockwise rotation.
        """
        if self._is_anticlockwise_rotateable():
            self.current_sprite_index = self._get_prev_sprite_index(self.current_sprite_index)


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
        right_edge = self._get_right_edge(self.current_sprite_index)
        return right_edge < self.glass.width - 1


    def _is_left_moveable(self):
        """
        Returns True if this figure can be moved left at least one step.
        """
        left_edge = self._get_left_edge(self.current_sprite_index)
        return left_edge > 0


    def _is_clockwise_rotateable(self):
        """
        Returns True if figure can be rotated clockwise.
        """
        next_sprite_index = self._get_next_sprite_index(self.current_sprite_index)
        right_edge = self._get_right_edge(next_sprite_index)
        left_edge = self._get_left_edge(next_sprite_index)
        return right_edge < self.glass.width and left_edge >= 0


    def _is_anticlockwise_rotateable(self):
        """
        Returns True if figure can be rotated anticlockwise.
        """
        prev_sprite_index = self._get_prev_sprite_index(self.current_sprite_index)
        right_edge = self._get_right_edge(prev_sprite_index)
        left_edge = self._get_left_edge(prev_sprite_index)
        return right_edge < self.glass.width and left_edge >= 0
        

    def _get_right_edge(self, sprite_index):
        """
        Returns X position of the right figure's point in the Glass' coordinates.
        """
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


    def _get_left_edge(self, sprite_index):
        """
        Returns X position of the left figure's point in the Glass' coordinates.
        """
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


    def _get_next_sprite_index(self, i):
        """
        Returns next index for the given current index.
        """
        i += 1
        i %= 4 
        return i


    def _get_prev_sprite_index(self, i):
        """
        Returns previous index for the given current one.
        """
        i -= 1
        if i < 0:
            i = 3
        return i
