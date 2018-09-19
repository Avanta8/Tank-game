import play
import screens


class Main:

    def __init__(self):

        self.scenes = {'spsurv': play.SpSurv(controller=self),
                       'start': screens.Start(controller=self),
                       'play': screens.SelectPlayers(controller=self),
                       'sp': screens.SpMenu(controller=self),
                       'spplay': screens.SpSelectMode(controller=self)}

        self.change_scene('start')

    def change_scene(self, scene, *args, **kwargs):
        self.scenes[scene].run(*args, **kwargs)


Main()
