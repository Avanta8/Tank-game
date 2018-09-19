import random


class Tank:
    def __init__(self):
        self.speed = 5
        self.hit = False


class StdSizeTank(Tank):
    def __init__(self):
        super().__init__()

        self.x_len = self.y_len = 68
        self.hf_x_len = self.hf_y_len = 34
        self.turrets = {'turret': [0, 0]}

        # self.turret_x_len = 24
        # self.turret_y_len = 90
        # self.turret_hf_x_len = 12
        # self.turret_hf_y_len = 45


class UserTank(StdSizeTank):
    def __init__(self):
        super().__init__()
        self.body = r'Assets\TankParts\UserTank\blue_tank_body.png'
        self.health = self.max_health = 600
        self.shield_health = self.max_shield_health = 600
        self.pred_move_dir = [0, 0]
        self.last_add_shield = 0
        self.shoot = False
        self.shoot_time = 0
        self.cannon_shot_time = 0
        self.minigun_shot_time = 0
        self.start_wave = 1
        self.unlocked_guns = {'standard'}
        self.type = 'standard'

    @property
    def diag_speed(self):
        return (self.speed ** 2 / 2) ** .5


class AiTank(Tank):

    def __init__(self):
        super().__init__()
        self.rand_dir_ver = random.choice(['up', 'down'])
        self.rand_dir_hor = random.choice(['left', 'right'])
        self.next_move_lens = [0, 0]
        self.shoot = True
        self.last_shot_time = 0
        self.last_rand_move = 0
        self.bullets = {'bullet': [0, 0]}


class StdSizeAiTank(StdSizeTank, AiTank):

    def __init__(self):
        StdSizeTank.__init__(self)
        AiTank.__init__(self)
        self.speed = 4
        self.health = 100
        self.keep_user_dist = 300
        self.min_user_dist = 68


class StdAiTank(StdSizeAiTank):

    body = r'Assets\TankParts\AiTank\red_tank_body.png'

    def __init__(self):
        super().__init__()
        self.reload = 1000
        self.max_bullet_move = 30
        self.bullet_speed = 15
        self.rank = 0
        self.smart_aim = True
        self.type = 'standard'


class CannonAiTank(StdSizeAiTank):

    body = r'Assets\TankParts\AiTank\green_tank_body.png'

    def __init__(self):
        super().__init__()
        self.reload = 2000
        self.max_bullet_move = 30
        self.bullet_speed = 12.5
        self.rank = 0
        self.smart_aim = False
        self.type = 'cannon'


class BossTank(AiTank):

    def __init__(self):
        self.x_len = self.y_len = 84
        self.hf_x_len = self.hf_y_len = 42

        super().__init__()

        self.speed = 6
        self.health = 2000
        self.keep_user_dist = 300
        self.min_user_dist = 68


class RedBossTank(BossTank):

    body = r'Assets\TankParts\AiTank\red_boss_body.png'

    def __init__(self):
        super().__init__()
        self.reload = 1000
        self.max_bullet_move = 30
        self.bullet_speed = 15
        self.rank = 1
        self.smart_aim = False
        self.type = 'redBoss'

        self.turrets = {'turretMain': [0, 15],
                        'turretLeft': [-15, -15],
                        'turretRight': [15, -15]}
        self.bullets = {'bullet1': [0, 15],
                        'bullet2': [-15, -15],
                        'bullet3': [15, -15]}


if __name__ == '__main__':
    user_tank = UserTank()
