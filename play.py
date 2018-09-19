import math
import pygame
import random
import background
import bullets
import fieldObjs
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

user_tank = tanks.UserTank()


class SpSurv:

    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        game_display.fill(white)

        self.init_objs()
        self.set_dicts()

    def init_objs(self):
        # Background
        self.grass_bkg_obj = background.GrassBackground()
        self.grass_bkg = pygame.image.load(self.grass_bkg_obj.background)

        # User tank
        self.user_tank_body = pygame.image.load(user_tank.body)

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

        # Ai Tanks
        # Ai standard
        self.ai_std_tank_body = pygame.image.load(tanks.StdAiTank.body)
        self.ai_std_tank_turret = pygame.image.load(turrets.StdAiTurret.turret)
        self.ai_std_tank_bullet = pygame.image.load(bullets.StdAiBullet.bullet)

        # Ai cannon
        self.ai_cannon_tank_body = pygame.image.load(
            tanks.CannonAiTank.body)
        self.ai_cannon_tank_turret = pygame.image.load(
            turrets.CannonAiTurret.turret)
        self.ai_cannon_tank_bullet = pygame.image.load(
            bullets.CannonAiBullet.bullet)

        # Ai red boss
        self.red_boss_body = pygame.image.load(
            tanks.RedBossTank.body)
        self.red_boss_turret_main = pygame.image.load(
            turrets.RedBossTurretMain.turret)
        self.red_boss_turret_left = pygame.image.load(
            turrets.RedBossTurretLeft.turret)
        self.red_boss_turret_right = pygame.image.load(
            turrets.RedBossTurretRight.turret)
        self.red_boss_bullet = pygame.image.load(
            bullets.RedBossBullet.bullet)

        # Field objs
        self.ai_spawn_img = pygame.image.load(fieldObjs.AiSpawn.body)

        # Should prob put this somewhere else
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
                                      'bullet': bullets.StdAiBullet},
                         'cannon': {'body': tanks.CannonAiTank,
                                    'turret': turrets.CannonAiTurret,
                                    'bullet': bullets.CannonAiBullet},
                         'redBoss': {'body': tanks.RedBossTank,
                                     'turretMain': turrets.RedBossTurretMain,
                                     'turretLeft': turrets.RedBossTurretLeft,
                                     'turretRight': turrets.RedBossTurretRight,
                                     'bullet1': bullets.RedBossBullet,
                                     'bullet2': bullets.RedBossBullet,
                                     'bullet3': bullets.RedBossBullet}}

        self.ai_types_imgs = {'standard': {'body': self.ai_std_tank_body,
                                           'turret': self.ai_std_tank_turret,
                                           'bullet': self.ai_std_tank_bullet},
                              'cannon': {'body': self.ai_cannon_tank_body,
                                         'turret': self.ai_cannon_tank_turret,
                                         'bullet': self.ai_cannon_tank_bullet},
                              'redBoss': {'body': self.red_boss_body,
                                          'turretMain': self.red_boss_turret_main,
                                          'turretLeft': self.red_boss_turret_left,
                                          'turretRight': self.red_boss_turret_right,
                                          'bullet1': self.red_boss_bullet,
                                          'bullet2': self.red_boss_bullet,
                                          'bullet3': self.red_boss_bullet}}

        self.field_objs_types = {'aiSpawn': fieldObjs.AiSpawn}

        self.field_objs_imgs = {'aiSpawn': self.ai_spawn_img}

    def reset_states(self, *args, **kwargs):

        user_tank.pos = [0, 0]

        self.ai_tank_count = 0

        self.left_down = self.right_down = self.up_down = self.down_down = False
        self.mouse_down = False
        user_tank.shoot = False

        self.ai_spawn_x = 1500
        self.ai_spawn_y = 800

        self.bullets = []
        self.ai_tanks = []
        self.ai_bullets = []
        self.field_objs = []

        for p in [[-self.ai_spawn_x, -self.ai_spawn_y],
                  [self.ai_spawn_x, -self.ai_spawn_y],
                  [-self.ai_spawn_x, self.ai_spawn_y],
                  [self.ai_spawn_x, self.ai_spawn_y]]:
            f = self.get_field_objs('aiSpawn')()
            f.pos = p
            self.field_objs.append(f)

        user_tank.body_rect = self.user_tank_body.get_rect(
            center=self.game_centre)

        user_tank.type = 'standard'

        for kw, val in kwargs.items():
            setattr(user_tank, kw, val)

        self.wave_no = user_tank.start_wave
        self.wave_end = True
        self.wave_display_time = 0
        self.extra_end_wave_time = 0
        self.ai_spawn_wait_time = 0

        self.wave_max_tanks = 0
        self.wave_tank_total = 0
        self.last_added_tank = 0

        self.add_ai = False

        user_tank.cannon_shot_time = pygame.time.get_ticks()

    def run(self, *args, restart=True, **kwargs):

        if restart:
            self.reset_states(**kwargs)

        while True:
            print(game_clock.get_fps())
            # print(pygame.time.get_ticks())
            self.check_events()
            self.add_ai_tank()
            self.ai_move()
            self.user_move()
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
                user_tank.shoot = True
                user_tank.shoot_time = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                user_tank.shoot = False
                user_tank.shoot_time = -1
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
                    user_tank.type = 'standard' if 'standard' in user_tank.unlocked_guns else user_tank.type
                if event.key == pygame.K_2:
                    user_tank.type = 'minigun' if 'minigun' in user_tank.unlocked_guns else user_tank.type
                if event.key == pygame.K_3:
                    user_tank.type = 'cannon' if 'cannon' in user_tank.unlocked_guns else user_tank.type
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
            x_change = -user_tank.speed
        elif self.right_down:
            x_change = +user_tank.speed

        if self.up_down is self.down_down:
            y_change = 0
        elif self.up_down:
            y_change = -user_tank.speed
        elif self.down_down:
            y_change = +user_tank.speed

        if x_change and not y_change:
            user_tank.pos[0] += x_change
            user_tank.pred_move_dir = [x_change, 0]
        elif y_change and not x_change:
            user_tank.pos[1] += y_change
            user_tank.pred_move_dir = [0, y_change]
        elif y_change and x_change:
            user_tank.pos[0] += (x_change / user_tank.speed) * \
                user_tank.diag_speed
            user_tank.pos[1] += (y_change / user_tank.speed) * \
                user_tank.diag_speed
            user_tank.pred_move_dir = [(x_change / user_tank.speed) * user_tank.diag_speed,
                                       (y_change / user_tank.speed) * user_tank.diag_speed]
        else:
            user_tank.pred_move_dir = [0, 0]

        user_tank.pos[0] = self.tank_x_min if user_tank.pos[0] < self.tank_x_min \
            else self.tank_x_max if user_tank.pos[0] > self.tank_x_max else user_tank.pos[0]
        user_tank.pos[1] = self.tank_y_min if user_tank.pos[1] < self.tank_y_min \
            else self.tank_y_max if user_tank.pos[1] > self.tank_y_max else user_tank.pos[1]

        for obj in self.field_objs:

            c_x, c_y = self.check_touching(obj, user_tank)

            if abs(c_x) < abs(c_y):
                user_tank.pos[0] -= c_x
            elif abs(c_x) > abs(c_y):
                user_tank.pos[1] -= c_y
            else:
                user_tank.pos[0] -= c_x
                user_tank.pos[1] -= c_y

        for o_tank in self.ai_tanks:

            c_x, c_y = self.check_touching(o_tank, user_tank)

            if abs(c_x) < abs(c_y):
                user_tank.pos[0] -= c_x
            elif abs(c_x) > abs(c_y):
                user_tank.pos[1] -= c_y
            else:
                user_tank.pos[0] -= c_x
                user_tank.pos[1] -= c_y

    def ai_move(self):
        for tank in self.ai_tanks:

            diff = [user_tank.pos[0] - tank.pos[0],
                    user_tank.pos[1] - tank.pos[1]]
            tank.diff_len = (diff[0] ** 2 + diff[1] ** 2) ** .5

            if tank.diff_len > tank.keep_user_dist and tank.last_rand_move <= 1:
                ratio = tank.speed / tank.diff_len
                move_lens = [diff[0] * ratio, diff[1] * ratio]
                tank.pos[0] += move_lens[0]
                tank.pos[1] += move_lens[1]
            elif tank.body_rect.colliderect(user_tank.body_rect):
                ratio = user_tank.speed / tank.diff_len
                move_lens = [diff[0] * ratio, diff[1] * ratio]
                tank.pos[0] -= move_lens[0]
                tank.pos[1] -= move_lens[1]
            else:
                if tank.last_rand_move > 15:
                    tank.rand_dir_ver = random.choice(['up', 'down'])
                    tank.rand_dir_hor = random.choice(['left', 'right'])
                    tank.last_rand_move = 0
                tank.pos[0] += 2 if tank.rand_dir_ver == 'up' else -2
                tank.pos[1] += 2 if tank.rand_dir_hor == 'right' else -2
                tank.last_rand_move += 1

            for o_tank in self.ai_tanks + [user_tank]:
                if o_tank == tank:
                    continue

                c_x, c_y = self.check_touching(o_tank, tank)

                if abs(c_x) < abs(c_y):
                    tank.pos[0] -= c_x
                elif abs(c_x) > abs(c_y):
                    tank.pos[1] -= c_y
                else:
                    tank.pos[0] -= c_x
                    tank.pos[1] -= c_y

    def detect_bullet_collisions(self):
        for tank in self.ai_tanks:
            for bullet in self.bullets:
                if tank.body_rect.colliderect(bullet.rect_centre):
                    tank.health -= bullet.dmg
                    bullet.kill = True

        for bullet in self.ai_bullets:
            if user_tank.body_rect.colliderect(bullet.rect_centre):
                if user_tank.shield_health < bullet.dmg:
                    user_tank.health -= bullet.dmg
                else:
                    user_tank.shield_health -= bullet.dmg
                bullet.kill = True

        self.ai_tanks = list(filter(lambda t: t.health > 0, self.ai_tanks))
        self.ai_tank_count = len(self.ai_tanks)

    def check_touching(self, o, t):

        x = sum([t.hf_x_len, o.hf_x_len]) // 2
        y = sum([t.hf_y_len, o.hf_y_len]) // 2

        t_r = t.pos[0] + x
        t_l = t.pos[0] - x
        t_b = t.pos[1] + x
        t_t = t.pos[1] - x

        o_r = o.pos[0] + y
        o_l = o.pos[0] - y
        o_b = o.pos[1] + y
        o_t = o.pos[1] - y

        if t_l <= o_r <= t_r:
            c_x = t_l - o_r
        elif t_l <= o_l <= t_r:
            c_x = t_r - o_l
        else:
            c_x = 0

        if t_t <= o_t <= t_b:
            c_y = t_b - o_t
        elif t_t <= o_b <= t_b:
            c_y = t_t - o_b
        else:
            c_y = 0

        return c_x, c_y

    def display_all(self):
        self.get_angle()
        self.display_background()
        self.display_field_objs()
        self.display_tank_parts()
        self.display_ai_tanks_parts()
        self.display_boundaries()
        self.move_bullet()
        self.move_tanks_bullet()
        self.display_health()
        self.display_wave()

    def move_bullet(self):
        # print(user_tank.shoot_time)
        # print(user_tank.type)

        if user_tank.type == 'standard':
            if self.mouse_down and user_tank.shoot_time == 0:
                user_tank.shoot = True
                user_tank.shoot_time += 1
            else:
                user_tank.shoot = False

        elif user_tank.type == 'minigun':
            # if self.mouse_down and user_tank.shoot_time <= 0:
            #     user_tank.shoot = True
            #     user_tank.shoot_time = 6
            if self.mouse_down and pygame.time.get_ticks() > user_tank.minigun_shot_time + 100:
                user_tank.shoot = True
                user_tank.minigun_shot_time = pygame.time.get_ticks()
            else:
                user_tank.shoot = False

        elif user_tank.type == 'cannon':
            if self.mouse_down and user_tank.shoot_time == 0 and \
                    pygame.time.get_ticks() > user_tank.cannon_shot_time + 750:
                user_tank.shoot = True
                user_tank.cannon_shot_time = pygame.time.get_ticks()
                user_tank.shoot_time += 1
            else:
                user_tank.shoot = False

        if user_tank.shoot:
            if user_tank.type in ['standard', 'cannon']:
                x = y = 0
            elif user_tank.type == 'minigun':
                minigun_turret = self.curr_user_tank('turret')
                minigun_turret.last_turret_shot = minigun_turret.all_turrets - \
                    minigun_turret.last_turret_shot

                if minigun_turret.last_turret_shot == {'left'}:
                    x = 7 * math.cos(math.radians(self.angle - 90))
                    y = 7 * math.sin(math.radians(self.angle - 90))
                elif minigun_turret.last_turret_shot == {'right'}:
                    x = 7 * math.cos(math.radians(self.angle + 90))
                    y = 7 * math.sin(math.radians(self.angle + 90))

            b = self.curr_user_tank('bullet')()
            b.bullet = pygame.transform.rotate(
                self.curr_user_tank_imgs('bullet'), self.angle - 90)
            b.rect_centre = b.bullet.get_rect(
                center=[self.game_centre[0] + x, self.game_centre[1] - y])
            b.direction = [b.spd * math.cos(-math.radians(self.angle)),
                           b.spd * math.sin(-math.radians(self.angle))]
            b.start_pos = [user_tank.pos[0] + b.direction[0] * 2,
                           user_tank.pos[1] + b.direction[1] * 2]
            # real_pos doesn't actually do anything rn
            b.real_pos = [user_tank.pos[0] + b.direction[0] * 2,
                          user_tank.pos[1] + b.direction[1] * 2]
            # print('bullet start pos:', b.start_pos)
            self.bullets.append(b)
            user_tank.shoot = False

        for bullet in self.bullets:
            if not bullet.kill:
                bullet.move(user_tank.pos)
                # print('bullet centre:', bullet.centre)
                game_display.blit(bullet.bullet, bullet.rect_centre)
            else:
                # TODO: Create explosion effect or maybe only do it when it hits a tank
                pass

        self.bullets = list(filter(lambda b: not b.kill, self.bullets))

    def move_tanks_bullet(self):
        for tank in self.ai_tanks:
            # print(tank.diff_len)
            if pygame.time.get_ticks() > tank.last_shot_time + tank.reload and tank.diff_len <= 17 * tank.max_bullet_move:
                tank.shoot = True
            if tank.shoot:
                tank.last_shot_time = pygame.time.get_ticks()
                for bull, bull_pos in tank.bullets.items():
                    b = self.get_ai_tank(tank.type, bull)()
                    b.bullet = pygame.transform.rotate(
                        self.get_ai_tank_imgs(tank.type, bull), tank.angle - 90)
                    b.rect_centre = b.bullet.get_rect(center=self.game_centre)
                    b.direction = [b.spd * math.cos(-math.radians(tank.angle)),
                                   b.spd * math.sin(-math.radians(tank.angle))]
                    b.start_pos = [tank.pos[0] + bull_pos[0] + b.direction[0] * 2,
                                   tank.pos[1] + bull_pos[1] + b.direction[1] * 2]
                    # real_pos doesn't actually do anything rn
                    b.real_pos = [tank.pos[0] + bull_pos[0] + b.direction[0] * 2,
                                  tank.pos[1] + bull_pos[1] + b.direction[1] * 2]
                    # print('bullet start pos:', b.start_pos)
                    self.ai_bullets.append(b)
                tank.shoot = False

        for bullet in self.ai_bullets:
            if not bullet.kill:
                bullet.move(user_tank.pos)
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

        # print(user_tank.pred_move_dir)
        for tank in self.ai_tanks:
            rel_x = user_tank.pos[0] - \
                tank.pos[0] + user_tank.pred_move_dir[0] * \
                ((.5 * tank.diff_len) / tank.bullet_speed if tank.smart_aim else 1)
            rel_y = user_tank.pos[1] - \
                tank.pos[1] + user_tank.pred_move_dir[1] * \
                ((.5 * tank.diff_len) / tank.bullet_speed if tank.smart_aim else 1)
            tank.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    def display_tank_parts(self):
        if user_tank.health <= 0:
            user_tank.pos = [0, 0]
            user_tank.health = user_tank.max_health
            user_tank.shield_health = user_tank.max_shield_health
        # Displays tank body
        user_tank.body_rect = self.user_tank_body.get_rect(
            center=self.game_centre)
        game_display.blit(self.user_tank_body, user_tank.body_rect)

        # Displays tank turret
        turret_image = pygame.transform.rotate(
            self.curr_user_tank_imgs('turret'), self.angle - 90)
        user_tank.turret_rect = turret_image.get_rect(
            center=self.game_centre)
        game_display.blit(turret_image, user_tank.turret_rect)

    def display_ai_tanks_parts(self):
        for tank in self.ai_tanks:
            # Displays tank body
            tank.body_rect = self.get_ai_tank_imgs(tank.type, 'body').get_rect(
                center=[tank.pos[0] - user_tank.pos[0] + display_x // 2,
                        tank.pos[1] - user_tank.pos[1] + display_y // 2])
            game_display.blit(self.get_ai_tank_imgs(
                tank.type, 'body'), tank.body_rect)

            # Displays tank turret
            for turret, turret_pos in tank.turrets.items():
                turret_image = pygame.transform.rotate(
                    self.get_ai_tank_imgs(tank.type, turret), tank.angle - 90)
                tank.turret_rect = turret_image.get_rect(
                    center=[tank.pos[0] - user_tank.pos[0] + display_x // 2 + turret_pos[0],
                            tank.pos[1] - user_tank.pos[1] + display_y // 2 + turret_pos[1]])
                game_display.blit(turret_image, tank.turret_rect)

    def add_ai_tank(self):
        if self.wave_tank_total < self.wave_max_tanks \
                and pygame.time.get_ticks() > self.last_added_tank + self.ai_spawn_wait_time \
                and self.add_ai and self.ai_tank_count <= 30:
            self.last_added_tank = pygame.time.get_ticks()
            tank = self.wave_tanks.pop()
            ai = self.get_ai_tank(tank, 'body')()
            ai.pos = [random.choice([-self.ai_spawn_x, self.ai_spawn_x]),
                      random.choice([-self.ai_spawn_y, self.ai_spawn_y])]
            ai.body_rect = self.get_ai_tank_imgs(tank, 'body').get_rect(
                center=self.game_centre)
            ai.rank = pygame.time.get_ticks()
            self.ai_tanks.append(ai)
            self.ai_tank_count += 1
            self.wave_tank_total += 1

        if self.ai_tank_count == 0 and self.wave_tank_total >= self.wave_max_tanks:
            if not self.wave_end:
                self.extra_end_wave_time = pygame.time.get_ticks()
                self.wave_end = True
            elif pygame.time.get_ticks() > self.extra_end_wave_time + 1000:
                self.wave_display_time = 0

    def display_health(self):
        health = user_tank.health / user_tank.max_health
        shield = user_tank.shield_health / user_tank.max_shield_health
        pygame.draw.rect(game_display, black,
                         (self.health_bar_bg_pos, self.health_bar_bg_size))
        pygame.draw.rect(game_display, green,
                         (self.health_bar_pos, (self.health_bar_max_size[0] * health, self.health_bar_max_size[1])))
        pygame.draw.rect(game_display, light_blue,
                         (self.shield_bar_pos, (self.health_bar_max_size[0] * shield, self.health_bar_max_size[1])))

        if pygame.time.get_ticks() > user_tank.last_add_shield + 1000:
            user_tank.last_add_shield += 1000
            user_tank.shield_health += min(
                [10, user_tank.max_shield_health - user_tank.shield_health])

    def display_field_objs(self):
        for obj in self.field_objs:
            obj_rect = self.get_field_objs_imgs(obj.type).get_rect(
                center=[obj.pos[0] - user_tank.pos[0] + display_x // 2,
                        obj.pos[1] - user_tank.pos[1] + display_y // 2])
            game_display.blit(self.get_field_objs_imgs(
                obj.type), obj_rect)

    def display_wave(self):
        if self.wave_end and self.wave_display_time == 0:
            self.wave_display_time = pygame.time.get_ticks()
            wave_font = pygame.font.SysFont('gillsansultra', 100)
            self.wave_text = wave_font.render(
                f'Wave {self.wave_no}', True, (0, 0, 0))
            self.text_rect = self.wave_text.get_rect(
                center=[display_x // 2, display_y // 2])
            self.wave_tanks = ['standard' for _ in range({0: self.wave_no,
                                                          1: self.wave_no // 2,
                                                          2: self.wave_no // 2,
                                                          3: self.wave_no // 3}.get(
                self.wave_no // 10, self.wave_no // 2))] \
                + ['cannon' for _ in range(self.wave_no // 5)] \
                + ['redBoss' for _ in range(self.wave_no // 10)]
            random.shuffle(self.wave_tanks)
            # print(self.wave_tanks, self.wave_no)
            self.wave_max_tanks = len(self.wave_tanks)
            self.wave_tank_total = 0
            self.ai_spawn_wait_time = 1000 / self.wave_no ** .25
            self.wave_no += 1
            self.wave_end = False
            self.add_ai = False
        if pygame.time.get_ticks() < self.wave_display_time + 3000:
            game_display.blit(self.wave_text, self.text_rect)
        else:
            self.add_ai = True

    def display_background(self):
        game_display.blit(self.grass_bkg,
                          ((0 - user_tank.pos[0]) % display_x,
                           (0 - user_tank.pos[1]) % display_y))
        game_display.blit(self.grass_bkg,
                          ((0 - user_tank.pos[0]) % display_x - display_x,
                           (0 - user_tank.pos[1]) % display_y))

        game_display.blit(self.grass_bkg,
                          ((0 - user_tank.pos[0]) % display_x,
                           (0 - user_tank.pos[1]) % display_y - display_y))
        game_display.blit(self.grass_bkg,
                          ((0 - user_tank.pos[0]) % display_x - display_x,
                           (0 - user_tank.pos[1]) % display_y - display_y))

    def display_boundaries(self):
        a = [- 1.5 * display_x - user_tank.pos[0] - user_tank.hf_x_len - 10,
             - 1.5 * display_y - user_tank.pos[1] - user_tank.hf_y_len - 10]
        b = [2.5 * display_x - user_tank.pos[0] + user_tank.hf_x_len + 10,
             - 1.5 * display_y - user_tank.pos[1] - user_tank.hf_y_len - 10]
        c = [2.5 * display_x - user_tank.pos[0] + user_tank.hf_x_len + 10,
             2.5 * display_y - user_tank.pos[1] + user_tank.hf_y_len + 10]
        d = [- 1.5 * display_x - user_tank.pos[0] - user_tank.hf_x_len - 10,
             2.5 * display_y - user_tank.pos[1] + user_tank.hf_y_len + 10]

        def add10(x): return [x[0] + 10, x[1]]

        def sub10(x): return [x[0] - 10, x[1]]
        boundaries = [[sub10(a), add10(b)], [b, c],
                      [add10(c), sub10(d)], [d, a]]

        for i in range(len(boundaries)):
            pygame.draw.line(game_display, black, *boundaries[i], 20)

    def curr_user_tank_imgs(self, tank_part):
        return self.user_types_imgs[user_tank.type][tank_part]

    def curr_user_tank(self, tank_part):
        return self.user_types[user_tank.type][tank_part]

    def get_ai_tank_imgs(self, tank_type, tank_part):
        return self.ai_types_imgs[tank_type][tank_part]

    def get_ai_tank(self, tank_type, tank_part):
        return self.ai_types[tank_type][tank_part]

    def get_field_objs_imgs(self, obj):
        return self.field_objs_imgs[obj]

    def get_field_objs(self, obj):
        return self.field_objs_types[obj]


if __name__ == '__main__':
    app = SpSurv()
    app.run()
