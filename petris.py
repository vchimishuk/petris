from figurei import FigureI

def main():
    f = FigureI()
    print(f.current_sprite_index)
    f.rotate_right()
    print(f.current_sprite_index)


if __name__ == '__main__':
    main()
