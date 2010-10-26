class Figure:
    def __init__(self, glass):
        self.current_sprite_index = 0
        self.glass = glass
        # Put me at the middle top of the glass.
        self.x = 0
        self.y = glass.width / 2

    
    def rotate_right(self):
        # TODO: Check if this figure can be rotated in present position.
        self.current_sprite_index += 1
        self.current_sprite_index %= 4 


    def rotate_left(self):
        self.current_sprite_index += 1
        if self.current_sprite_index < 0:
            self.current_sprite_index = 3


    def move_right(self):
        if _is_right_movable(self):
            self.x += 1

    def move_left(self):
        # TODO: Move left functionality
        pass
    

    def _is_right_movable(self):
        # Find my right edge.
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

        return right_edge < self.glass.width
