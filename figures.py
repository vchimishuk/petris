from figure import Figure

class FigureS(Figure):
    sprites = (
        ((0, 0, 0, 0, 0),
         (0, 0, 1, 1, 0),
         (0, 1, 2, 0, 0),
         (0, 0, 0, 0, 0),
         (0, 0, 0, 0, 0)),

        ((0, 0, 0, 0, 0),
         (0, 0, 1, 0, 0),
         (0, 0, 2, 1, 0),
         (0, 0, 0, 1, 0),
         (0, 0, 0, 0, 0)),
        
        ((0, 0, 0, 0, 0),
         (0, 0, 0, 0, 0),
         (0, 0, 2, 1, 0),
         (0, 1, 1, 0, 0),
         (0, 0, 0, 0, 0)),

        ((0, 0, 0, 0, 0),
         (0, 1, 0, 0, 0),
         (0, 1, 2, 0, 0),
         (0, 0, 1, 0, 0),
         (0, 0, 0, 0, 0)),
    )


    def __init__(self, y=0, x=0):
        Figure.__init__(self, y, x)
