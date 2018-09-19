import pygame


pygame.init()

display_x = 1200
display_y = 800
game_display = pygame.display.set_mode((display_x, display_y))

game_clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)


class Screen:

    @staticmethod
    def create_button(button, centre):
        button_rect = button.get_rect(center=centre)
        game_display.blit(button, button_rect)
        return button_rect

    # get_text is not used rn. Maybe make all text and buttons as images
    @staticmethod
    def get_text(text, text_colour, text_center, font, font_size, bg_colour=None):

        # This sets the font for the text
        font = pygame.font.Font(font, font_size)
        # This creates the text
        text = font.render(text, True, text_colour, (45, 77, 56))
        # Creates a rectangle object for the text
        text_rect = text.get_rect()
        # This sets the text rectangle's centre
        text_rect.center = text_center

        # This displays the text onto the text rectangle
        game_display.blit(text, text_rect)

    @staticmethod
    def quit():
        pygame.quit()
        quit()


class Start(Screen):

    def __init__(self, *args, controller, **kwargs):
        self.controller = controller
        self.tank_title = pygame.image.load(
            r'Assets\Menu\Buttons\Tanks_main_menu_button.png')

        self.play_button_selected = pygame.image.load(
            r'Assets\Menu\Buttons\play_button_selected.png')
        self.quit_button_selected = pygame.image.load(
            r'Assets\Menu\Buttons\quit_button_selected.png')

        self.play_button_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\play_button_unselected.png')
        self.quit_button_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\quit_button_unselected.png')

        self.button_pos = {'play': (600, 450), 'quit': (600, 650)}
        self.buttons_on = {'play': False, 'quit': False}
        self.option_rects = {'play': self.play, 'quit': self.quit}
        self.options = [[self.create_button(self.play_button_unselected, self.button_pos['play']), 'play'],
                        [self.create_button(self.quit_button_unselected, self.button_pos['quit']), 'quit']]

    def run(self, *args, **kwargs):

        while True:
            game_display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for option in self.options:
                        if option[0].collidepoint(pygame.mouse.get_pos()):
                            return self.option_rects[option[1]]()

            self.create_button(self.tank_title, (600, 200))

            if self.buttons_on['play']:
                self.options[0][0] = self.create_button(
                    self.play_button_selected, self.button_pos['play'])
            else:
                self.options[0][0] = self.create_button(
                    self.play_button_unselected, self.button_pos['play'])

            if self.buttons_on['quit']:
                self.options[1][0] = self.create_button(
                    self.quit_button_selected, self.button_pos['quit'])
            else:
                self.options[1][0] = self.create_button(
                    self.quit_button_unselected, self.button_pos['quit'])

            for option in self.options:
                if option[0].collidepoint(pygame.mouse.get_pos()):
                    self.buttons_on[option[1]] = True
                else:
                    self.buttons_on[option[1]] = False

            pygame.display.update()
            game_clock.tick(60)

    def play(self):
        print('play')
        self.controller.change_scene('play')

    def quit(self):
        print('quit')
        pygame.quit()
        quit()


class SelectPlayers(Screen):
    def __init__(self, *args, controller, **kwargs):
        self.controller = controller
        self.title_screen = pygame.image.load(
            r'Assets\Menu\Buttons\select_players.png')

        self.sp_selected = pygame.image.load(
            r'Assets\Menu\Buttons\single_player_selected.png')
        self.p2_selected = pygame.image.load(
            r'Assets\Menu\Buttons\two_players_selected.png')
        self.back_selected = pygame.image.load(
            r'Assets\Menu\Buttons\small_back_selected.png')

        self.sp_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\single_player_unselected.png')
        self.p2_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\two_players_unselected.png')
        self.back_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\small_back_unselected.png')

        self.button_pos = {'sp': (600, 450),
                           'p2': (600, 650),
                           'back': (140, 650)}
        self.buttons_on = {'sp': False, 'p2': False, 'back': False}
        self.option_rects = {'sp': self.sp, 'p2': self.p2, 'back': self.back}
        self.options = [[self.create_button(self.sp_unselected, self.button_pos['sp']), 'sp'],
                        [self.create_button(
                            self.p2_unselected, self.button_pos['p2']), 'p2'],
                        [self.create_button(self.back_unselected, self.button_pos['back']), 'back']]

    def run(self, *args, **kwargs):

        while True:
            game_display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for option in self.options:
                        if option[0].collidepoint(pygame.mouse.get_pos()):
                            return self.option_rects[option[1]]()

            self.create_button(self.title_screen, (600, 200))

            if self.buttons_on['sp']:
                self.options[0][0] = self.create_button(
                    self.sp_selected, self.button_pos['sp'])
            else:
                self.options[0][0] = self.create_button(
                    self.sp_unselected, self.button_pos['sp'])

            if self.buttons_on['p2']:
                self.options[1][0] = self.create_button(
                    self.p2_selected, self.button_pos['p2'])
            else:
                self.options[1][0] = self.create_button(
                    self.p2_unselected, self.button_pos['p2'])

            if self.buttons_on['back']:
                self.options[2][0] = self.create_button(
                    self.back_selected, self.button_pos['back'])
            else:
                self.options[2][0] = self.create_button(
                    self.back_unselected, self.button_pos['back'])

            for option in self.options:
                if option[0].collidepoint(pygame.mouse.get_pos()):
                    self.buttons_on[option[1]] = True
                else:
                    self.buttons_on[option[1]] = False

            pygame.display.update()
            game_clock.tick(60)

    def sp(self):
        print('sp')
        self.controller.change_scene('sp')

    def p2(self):
        print('p2')
        self.controller.change_scene('p2')

    def back(self):
        print('start')
        self.controller.change_scene('start')


class SpMenu(Screen):

    def __init__(self, *args, controller, **kwargs):
        self.controller = controller

    def run(self, *args, **kwargs):
        self.controller.change_scene('spplay',
                                     unlocked_guns={'standard',
                                                    'cannon',
                                                    'minigun'},
                                     start_wave=1)


class SpSelectMode(Screen):
    def __init__(self, *args, controller, **kwargs):
        self.controller = controller
        self.title_screen = pygame.image.load(
            r'Assets\Menu\Buttons\choose_gamemode.png')

        self.campaign_selected = pygame.image.load(
            r'Assets\Menu\Buttons\campaign_selected.png')
        self.survival_selected = pygame.image.load(
            r'Assets\Menu\Buttons\survival_selected.png')
        self.back_selected = pygame.image.load(
            r'Assets\Menu\Buttons\small_back_selected.png')

        self.campaign_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\campaign_unselected.png')
        self.survival_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\survival_unselected.png')
        self.back_unselected = pygame.image.load(
            r'Assets\Menu\Buttons\small_back_unselected.png')

        self.button_pos = {'camp': (600, 450),
                           'surv': (600, 650),
                           'back': (140, 650)}
        self.buttons_on = {'camp': False, 'surv': False, 'back': False}
        self.option_rects = {'camp': self.camp,
                             'surv': self.surv,
                             'back': self.back}
        self.options = [[self.create_button(self.campaign_unselected, self.button_pos['camp']), 'camp'],
                        [self.create_button(
                            self.survival_unselected, self.button_pos['surv']), 'surv'],
                        [self.create_button(self.survival_unselected, self.button_pos['back']), 'back']]

    def run(self, *args, **kwargs):

        self.updates = kwargs

        while True:
            game_display.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    for option in self.options:
                        if option[0].collidepoint(pygame.mouse.get_pos()):
                            return self.option_rects[option[1]]()

            self.create_button(self.title_screen, (600, 200))

            if self.buttons_on['camp']:
                self.options[0][0] = self.create_button(
                    self.campaign_selected, self.button_pos['camp'])
            else:
                self.options[0][0] = self.create_button(
                    self.campaign_unselected, self.button_pos['camp'])

            if self.buttons_on['surv']:
                self.options[1][0] = self.create_button(
                    self.survival_selected, self.button_pos['surv'])
            else:
                self.options[1][0] = self.create_button(
                    self.survival_unselected, self.button_pos['surv'])

            if self.buttons_on['back']:
                self.options[2][0] = self.create_button(
                    self.back_selected, self.button_pos['back'])
            else:
                self.options[2][0] = self.create_button(
                    self.back_unselected, self.button_pos['back'])

            for option in self.options:
                if option[0].collidepoint(pygame.mouse.get_pos()):
                    self.buttons_on[option[1]] = True
                else:
                    self.buttons_on[option[1]] = False

            pygame.display.update()
            game_clock.tick(60)

    def camp(self):
        print('spcamp')
        self.controller.change_scene('spcamp', restart=True, **self.updates)

    def surv(self):
        print('spsurv')
        self.controller.change_scene('spsurv', restart=True, **self.updates)

    def back(self):
        print('back')
        self.controller.change_scene('back')


if __name__ == '__main__':
    a = Start()
    a.run()
    b = SelectPlayers()
    b.run()
    d = SpSelectMode()
    d.run()
