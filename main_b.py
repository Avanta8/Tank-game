import play
import screens


class Main:

    def __init__(self):

        all_scenes = {'spsurv': play.SpSurv, 'start': screens.Start,
                      'play': screens.SelectPlayers, 'sp': screens.SpMenu,
                      'spplay': screens.SpSelectMode}

        self.scenes = {scene: scene() for scene in all_scenes.values()}

        next_scene = all_scenes['start']
        while True:
            next_scene = all_scenes[self.change_scene(next_scene)]

    def change_scene(self, scene):
        return self.scenes[scene].run()


Main()
