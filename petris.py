from screen import Screen
from glass import Glass


class Petris():
    """
    Application respresentation class.
    """
    def init(self):
        """
        Initialize application.
        """
        self.screen = Screen()
        self.screen.init()
        self.glass = Glass(self.screen)
        self.screen.glass = self.glass


    def destroy(self):
        """
        Free application resources.
        """
        self.screen.destroy()


    def run(self):
        """
        Run main application loop.
        """
        self.screen.main_loop()
        

def main():
    petris = Petris()
    petris.init()
    petris.run()
    petris.destroy()


if __name__ == '__main__':
    main()
