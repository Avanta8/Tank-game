class Background:
    def __init__(self):
        pass


class GrassBackground(Background):
    def __init__(self):
        self.background = r'Assets\Backgrounds\simple_background.png'


if __name__ == '__main__':
    grass_background = GrassBackground()
