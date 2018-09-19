import math
import pygame
import random
import background
import bullets
import tanks
import turrets


pygame.init()

display_x = 1200
display_y = 800
game_display = pygame.display.set_mode((display_x, display_y))

game_clock = pygame.time.Clock()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
light_blue = (0, 40, 255)
black = (0, 0, 0)


class SpSurv:

    def __init__(self):
        game_display.fill(white)

        self.init_objs()

        self.user_tank.pos = [0, 0]

        self.ai_tank_count = 0

        self.left_down = self.right_down = self.up_down = self.down_down = False
        self.mouse_down = False
        self.user_tank.shoot = False

        self.bullets = []
        self.ai_tanks = []
        self.ai_bullets = []

        self.set_dicts()

        self.user_tank.body_rect = self.user_tank_body.get_rect(
            center=self.game_centre)

        self.user_tank.type = 'standard'

        self.user_tank.cannon_shot_time = pygame.time.get_ticks()

    def init_objs(self):
        self.grass_bkg_obj = background.GrassBackground()
        self.grass_bkg = pygame.image.load(self.grass_bkg_obj.background)

        self.user_tank = tanks.UserTank()
        self.user_tank_body = pygame.image.load(self.user_tank.body)

        self.user_std_turret = pygame.image.load(turrets.StdTurret.turret)
        self.user_std_bullet = pygame.image.load(bullets.StdBullet.bullet)

        self.user_minigun_turret = pygame.image.load(
            turrets.MinigunTurret.turret)
        self.user_minigun_bullet = pygame.image.load(
            bullets.MinigunBullet.bullet)

        self.user_cannon_turret = pygame.image.load(
            turrets.CannonTurret.turret)
        self.user_cannon_bullet = pygame.image.load(
            bullets.CannonBullet.bullet)

        self.ai_std_tank_body = pygame.image.load(tanks.StdAiTank.body)
        self.ai_std_tank_turret = pygame.image.load(turrets.StdAiTurret.turret)
        self.ai_std_tank_bullet = pygame.image.load(bullets.StdAiBullet.bullet)

        self.tank_x_min = - 2 * display_x
        self.tank_x_max = 2 * display_x
        self.tank_y_min = - 2 * display_y
        self.tank_y_max = 2 * display_y

        self.health_bar_bg_pos = 50, 50
        self.health_bar_bg_size = 200, 100

        self.health_bar_pos = 60, 60
        self.health_bar_max_size = 180, 30

        self.shield_bar_pos = 60, 110
        self.shield_bar_max_size = 180, 30

        self.game_centre = [display_x // 2,
                            display_y // 2]

    def set_dicts(self):
        self.user_types = {'standard': {'turret': turrets.StdTurret, 'bullet': bullets.StdBullet},
                           'minigun': {'turret': turrets.MinigunTurret, 'bullet': bullets.MinigunBullet},
                           'cannon': {'turret': turrets.CannonTurret, 'bullet': bullets.CannonBullet}}

        self.user_types_imgs = {'standard': {'turret': self.user_std_turret, 'bullet': self.user_std_bullet},
                                'minigun': {'turret': self.user_minigun_turret, 'bullet': self.user_minigun_bullet},
                                'cannon': {'turret': self.user_cannon_turret, 'bullet': self.user_cannon_bullet}}

        self.ai_types = {'standard': {'body': tanks.StdAiTank,
                                      'turret': turrets.StdAiTurret,
                                      'bullet': bullets.StdAiBullet}}

        self.ai_types_imgs = {'standard': {'body': self.ai_std_tank_body,
                                           'turret': self.ai_std_tank_turret,
                                           'bullet': self.ai_std_tank_bullet}}

    def run(self):
        while True:
            print(pygame.time.get_ticks())
            self.check_events()
            self.add_ai_tank()
            self.user_move()
            self.ai_move()
            self.detect_bullet_collisions()
            self.display_all()

            pygame.display.update()
            game_clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
                self.user_tank.shoot = True
                self.user_tank.shoot_time = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                self.user_tank.shoot = False
                self.user_tank.shoot_time = -1
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.left_down = True
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.right_down = True
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.up_down = True
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.down_down = True
                if event.key == pygame.K_1:
                    self.user_tank.type = 'standard'
                if event.key == pygame.K_2:
                    self.user_tank.type = 'minigun'
                if event.key == pygame.K_3:
                    self.user_tank.type = 'cannon'
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.left_down = False
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.right_down = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.up_down = False
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.down_down = False

    def user_move(self):
        if self.left_down is self.right_down:
            x_change = 0
        elif self.left_down:
            x_change = -self.user_tank.speed
        elif self.right_down:
            x_change = +self.user_tank.speed

        if self.up_down is self.down_down:
            y_change = 0
        elif self.up_down:
            y_change = -self.user_tank.speed
        elif self.down_down:
            y_change = +self.user_tank.speed

        if x_change and not y_change:
            self.user_tank.pos[0] += x_change
        elif y_change and not x_change:
            self.user_tank.pos[1] += y_change
        elif y_change and x_change:
            self.user_tank.pos[0] += (x_change / self.user_tank.speed) * \
                self.user_tank.diag_speed
            self.user_tank.pos[1] += (y_change / self.user_tank.speed) * \
                self.user_tank.diag_speed

        self.user_tank.pos[0] = self.tank_x_min if self.user_tank.pos[0] < self.tank_x_min \
            else self.tank_x_max if self.user_tank.pos[0] > self.tank_x_max else self.user_tank.pos[0]
        self.user_tank.pos[1] = self.tank_y_min if self.user_tank.pos[1] < self.tank_y_min \
            else self.tank_y_max if self.user_tank.pos[1] > self.tank_y_max else self.user_tank.pos[1]

    def ai_move(self):
        for i, tank in enumerate(self.ai_tanks):
            diff = [self.user_tank.pos[0] - tank.pos[0],
                    self.user_tank.pos[1] - tank.pos[1]]
            tank.diff_len = (diff[0] ** 2 + diff[1] ** 2) ** .5

            collided = self.detect_ai_collide(
                tank, self.ai_tanks[:i] + self.ai_tanks[i + 1:])
            if collided:
                tank.pos[0] += collided.next_move_lens[0]
                tank.pos[1] += collided.next_move_lens[1]

            if tank.body_rect.colliderect(self.user_tank.body_rect):
                ratio = self.user_tank.speed / tank.diff_len
                move_lens = [diff[0] * ratio, diff[1] * ratio]
                tank.next_move_lens = [- diff[0] * ratio, diff[1] * - ratio]
                tank.pos[0] -= move_lens[0]
                tank.pos[1] -= move_lens[1]
            elif tank.diff_len > tank.keep_user_dist and tank.last_rand_move <= 1:
                ratio = tank.speed / tank.diff_len
                tank.pos[0] += tank.next_move_lens[0]
                tank.pos[1] += tank.next_move_lens[1]
                tank.next_move_lens = [diff[0] * ratio, diff[1] * ratio]
            else:
                if tank.last_rand_move > 15:
                    tank.rand_dir_ver = random.choice(['up', 'down'])
                    tank.rand_dir_hor = random.choice(['left', 'right'])
                    tank.last_rand_move = 0
                tank.next_move_lens = [2 if tank.rand_dir_ver == 'up' else -2,
                                       2 if tank.rand_dir_hor == 'right' else -2]
                tank.pos[0] += 2 if tank.rand_dir_ver == 'up' else -2
                tank.pos[1] += 2 if tank.rand_dir_hor == 'right' else -2
                tank.last_rand_move += 1

    def detect_ai_collide(self, tank, other_tanks):
        for o_tank in other_tanks:
            if tank.rank < o_tank.rank and tank.body_rect.colliderect(o_tank.body_rect):
                return o_tank
        return False

    def detect_bullet_collisions(self):
        for tank in self.ai_tanks:
            for bullet in self.bullets:
                if tank.body_rect.colliderect(bullet.rect_centre):
                    tank.health -= bullet.dmg
                    bullet.kill = True

        for bullet in self.ai_bullets:
            if self.user_tank.body_rect.colliderect(bullet.rect_centre):
                if self.user_tank.shield_health < bullet.dmg:
                    self.user_tank.health -= bullet.dmg
                else:
                    self.user_tank.shield_health -= bullet.dmg
                bullet.kill = True

        self.ai_tanks = list(filter(lambda t: t.health > 0, self.ai_tanks))
        self.ai_tank_count = len(self.ai_tanks)

    def display_all(self):
        self.get_angle()
        self.display_background()
        self.display_tank_parts()
        self.display_ai_tanks_parts()
        self.display_boundaries()
        self.move_bullet()
        self.move_tanks_bullet()
        self.display_health()

    def move_bullet(self):
        # print(self.user_tank.shoot_time)
        # print(self.user_tank.type)

        if self.user_tank.type == 'standard':
            if self.mouse_down and self.user_tank.shoot_time == 0:
                self.user_tank.shoot = True
                self.user_tank.shoot_time += 1
            else:
                self.user_tank.shoot = False

        elif self.user_tank.type == 'minigun':
            # if self.mouse_down and self.user_tank.shoot_time <= 0:
            #     self.user_tank.shoot = True
            #     self.user_tank.shoot_time = 6
            if self.mouse_down and pygame.time.get_ticks() > self.user_tank.minigun_shot_time + 100:
                self.user_tank.shoot = True
                self.user_tank.minigun_shot_time = pygame.time.get_ticks()
            else:
                self.user_tank.shoot = False

        elif self.user_tank.type == 'cannon':
            if self.mouse_down and self.user_tank.shoot_time == 0 and \
                    pygame.time.get_ticks() > self.user_tank.cannon_shot_time + 750:
                self.user_tank.shoot = True
                self.user_tank.cannon_shot_time = pygame.time.get_ticks()
                self.user_tank.shoot_time += 1
            else:
                self.user_tank.shoot = False

        if self.user_tank.shoot:
            if self.user_tank.type in ['standard', 'cannon']:
                x = y = 0
            elif self.user_tank.type == 'minigun':
                minigun_turret = self.curr_user_tank_info('turret')
                minigun_turret.last_turret_shot = minigun_turret.all_turrets - \
                    minigun_turret.last_turret_shot

                if minigun_turret.last_turret_shot == {'left'}:
                    x = 7 * math.cos(math.radians(self.angle - 90))
                    y = 7 * math.sin(math.radians(self.angle - 90))
                elif minigun_turret.last_turret_shot == {'right'}:
                    x = 7 * math.cos(math.radians(self.angle + 90))
                    y = 7 * math.sin(math.radians(self.angle + 90))

            b = self.curr_user_tank_info('bullet')()
            b.bullet = pygame.transform.rotate(
                self.curr_user_tank_imgs('bullet'), self.angle - 90)
            b.rect_centre = b.bullet.get_rect(
                center=[self.game_centre[0] + x, self.game_centre[1] - y])
            b.direction = [b.spd * math.cos(-math.radians(self.angle)),
                           b.spd * math.sin(-math.radians(self.angle))]
            b.start_pos = [self.user_tank.pos[0] + b.direction[0] * 2,
                           self.user_tank.pos[1] + b.direction[1] * 2]
            # real_pos doesn't actually do anything rn
            b.real_pos = [self.user_tank.pos[0] + b.direction[0] * 2,
                          self.user_tank.pos[1] + b.direction[1] * 2]
            # print('bullet start pos:', b.start_pos)
            self.bullets.append(b)
            self.user_tank.shoot = False

        for bullet in self.bullets:
            if not bullet.kill:
                bullet.move(self.user_tank.pos)
                # print('bullet centre:', bullet.centre)
                game_display.blit(bullet.bullet, bullet.rect_centre)
            else:
                # TODO: Create explosion effect or maybe only do it when it hits a tank
                pass

        self.bullets = list(filter(lambda b: not b.kill, self.bullets))

    def move_tanks_bullet(self):
        for tank in self.ai_tanks:
            if pygame.time.get_ticks() > tank.last_shot_time + 1000 and tank.diff_len <= 18 * 30:
                tank.shoot = True
            if tank.shoot:
                tank.last_shot_time = pygame.time.get_ticks()
                b = self.get_ai_tank_info(tank.type, 'bullet')()
                b.bullet = pygame.transform.rotate(
                    self.get_ai_tank_imgs(tank.type, 'bullet'), tank.angle - 90)
                b.rect_centre = b.bullet.get_rect(center=self.game_centre)
                b.direction = [b.spd * math.cos(-math.radians(tank.angle)),
                               b.spd * math.sin(-math.radians(tank.angle))]
                b.start_pos = [tank.pos[0] + b.direction[0] * 2,
                               tank.pos[1] + b.direction[1] * 2]
                # real_pos doesn't actually do anything rn
                b.real_pos = [tank.pos[0] + b.direction[0] * 2,
                              tank.pos[1] + b.direction[1] * 2]
                # print('bullet start pos:', b.start_pos)
                self.ai_bullets.append(b)
                tank.shoot = False

        for bullet in self.ai_bullets:
            if not bullet.kill:
                bullet.move(self.user_tank.pos)
                # print('bullet centre:', bullet.centre)
                game_display.blit(bullet.bullet, bullet.rect_centre)

            self.ai_bullets = list(
                filter(lambda b: not b.kill, self.ai_bullets))

    def get_angle(self):
        # Info here. First answer by Ted Klein Bergman:
        # https://gamedev.stackexchange.com/questions/132163/how-can-i-make-the-player-look-to-the-mouse-direction-pygame-2d/134090
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.game_centre[0], \
            mouse_y - self.game_centre[1]
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        # print('angle:', self.angle)

        for tank in self.ai_tanks:
            rel_x, rel_y = self.user_tank.pos[0] - tank.pos[0], \
                self.user_tank.pos[1] - tank.pos[1]
            tank.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    def display_tank_parts(self):
        if self.user_tank.health <= 0:
            self.user_tank.pos = [0, 0]
            self.user_tank.health = self.user_tank.max_health
            self.user_tank.shield_health = self.user_tank.max_shield_health
        # Displays tank body
        self.user_tank.body_rect = self.user_tank_body.get_rect(
            center=self.game_centre)
        game_display.blit(self.user_tank_body, self.user_tank.body_rect)

        # Displays tank turret
        turret_image = pygame.transform.rotate(
            self.curr_user_tank_imgs('turret'), self.angle - 90)
        self.user_tank.turret_rect = turret_image.get_rect(
            center=self.game_centre)
        game_display.blit(turret_image, self.user_tank.turret_rect)

    def display_ai_tanks_parts(self):
        for tank in self.ai_tanks:
            # Displays tank body
            tank.body_rect = self.get_ai_tank_imgs('standard', 'body').get_rect(
                center=[tank.pos[0] - self.user_tank.pos[0] + display_x // 2,
                        tank.pos[1] - self.user_tank.pos[1] + display_y // 2])
            game_display.blit(self.get_ai_tank_imgs(
                'standard', 'body'), tank.body_rect)

            # Displays tank turret
            turret_image = pygame.transform.rotate(
                self.get_ai_tank_imgs('standard', 'turret'), tank.angle - 90)
            tank.turret_rect = turret_image.get_rect(
                center=[tank.pos[0] - self.user_tank.pos[0] + display_x // 2,
                        tank.pos[1] - self.user_tank.pos[1] + display_y // 2])
            game_display.blit(turret_image, tank.turret_rect)

    def add_ai_tank(self):
        if self.ai_tank_count < 5:
            ai = self.get_ai_tank_info('standard', 'body')()
            ai.pos = [random.randint(self.tank_x_min, self.tank_x_max),
                      random.randint(self.tank_y_min, self.tank_y_max)]
            ai.body_rect = self.get_ai_tank_imgs('standard', 'body').get_rect(
                center=self.game_centre)
            ai.rank = pygame.time.get_ticks()
            self.ai_tanks.append(ai)
            self.ai_tank_count += 1

    def display_health(self):
        health = self.user_tank.health / self.user_tank.max_health
        shield = self.user_tank.shield_health / self.user_tank.max_shield_health
        pygame.draw.rect(game_display, black,
                         (self.health_bar_bg_pos, self.health_bar_bg_size))
        pygame.draw.rect(game_display, green,
                         (self.health_bar_pos, (self.health_bar_max_size[0] * health, self.health_bar_max_size[1])))
        pygame.draw.rect(game_display, light_blue,
                         (self.shield_bar_pos, (self.health_bar_max_size[0] * shield, self.health_bar_max_size[1])))

        if pygame.time.get_ticks() > self.user_tank.last_add_shield + 1000:
            self.user_tank.last_add_shield += 1000
            self.user_tank.shield_health += min(
                [10, self.user_tank.max_shield_health - self.user_tank.shield_health])

    def display_background(self):
        game_display.blit(self.grass_bkg,
                          ((0 - self.user_tank.pos[0]) % display_x,
                           (0 - self.user_tank.pos[1]) % display_y))
        game_display.blit(self.grass_bkg,
                          ((0 - self.user_tank.pos[0]) % display_x - display_x,
                           (0 - self.user_tank.pos[1]) % display_y))

        game_display.blit(self.grass_bkg,
                          ((0 - self.user_tank.pos[0]) % display_x,
                           (0 - self.user_tank.pos[1]) % display_y - display_y))
        game_display.blit(self.grass_bkg,
                          ((0 - self.user_tank.pos[0]) % display_x - display_x,
                           (0 - self.user_tank.pos[1]) % display_y - display_y))

    def display_boundaries(self):
        a = [- 1.5 * display_x - self.user_tank.pos[0] - self.user_tank.hf_x_len - 10,
             - 1.5 * display_y - self.user_tank.pos[1] - self.user_tank.hf_y_len - 10]
        b = [2.5 * display_x - self.user_tank.pos[0] + self.user_tank.hf_x_len + 10,
             - 1.5 * display_y - self.user_tank.pos[1] - self.user_tank.hf_y_len - 10]
        c = [2.5 * display_x - self.user_tank.pos[0] + self.user_tank.hf_x_len + 10,
             2.5 * display_y - self.user_tank.pos[1] + self.user_tank.hf_y_len + 10]
        d = [- 1.5 * display_x - self.user_tank.pos[0] - self.user_tank.hf_x_len - 10,
             2.5 * display_y - self.user_tank.pos[1] + self.user_tank.hf_y_len + 10]

        def add10(x): return [x[0] + 10, x[1]]

        def sub10(x): return [x[0] - 10, x[1]]
        boundaries = [[sub10(a), add10(b)], [b, c],
                      [add10(c), sub10(d)], [d, a]]

        for i in range(len(boundaries)):
            pygame.draw.line(game_display, black, *boundaries[i], 20)

    def curr_user_tank_imgs(self, tank_part):
        return self.user_types_imgs[self.user_tank.type][tank_part]

    def curr_user_tank_info(self, tank_part):
        return self.user_types[self.user_tank.type][tank_part]

    def get_ai_tank_imgs(self, tank_type, tank_part):
        return self.ai_types_imgs[tank_type][tank_part]

    def get_ai_tank_info(self, tank_type, tank_part):
        return self.ai_types[tank_type][tank_part]


if __name__ == '__main__':
    app = SpSurv()
    app.run()
