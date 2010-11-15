from screen import Screen


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
    
    try:
        petris.run()
    except Exception as err:
        petris.destroy()
        raise err

    petris.destroy()
    

if __name__ == '__main__':
    main()
