class Bullet:

    def __init__(self):
        self.moved = 0
        self.kill = False

    def move(self, tank_pos):
        self.moved += 1
        if self.moved > self.max_move:
            self.kill = True

        self.rect_centre[0] += self.direction[0] - \
            (tank_pos[0] - self.start_pos[0])
        self.rect_centre[1] += self.direction[1] - \
            (tank_pos[1] - self.start_pos[1])

        self.real_pos[0] += self.direction[0] - \
            (tank_pos[0] - self.start_pos[0])
        self.real_pos[1] += self.direction[1] - \
            (tank_pos[1] - self.start_pos[1])

        self.start_pos = tank_pos[:]


class StdBullet(Bullet):

    bullet = r'Assets\TankParts\UserTank\blue_bullet_small.png'

    def __init__(self):
        super().__init__()
        self.spd = 15
        self.dmg = 50
        self.max_move = 30
        self.type = 'standard'


class MinigunBullet(Bullet):

    bullet = r'Assets\TankParts\UserTank\blue_bullet_tiny.png'

    def __init__(self):
        super().__init__()
        self.spd = 15
        self.dmg = 25
        self.max_move = 30
        self.type = 'minigun'


class CannonBullet(Bullet):

    bullet = r'Assets\TankParts\UserTank\blue_bullet_big.png'

    def __init__(self):
        super().__init__()
        self.spd = 15
        self.dmg = 100
        self.max_move = 30
        self.type = 'cannon'


class StdAiBullet(Bullet):

    bullet = r'Assets\TankParts\AiTank\red_bullet_small.png'

    def __init__(self):
        super().__init__()
        self.spd = 15
        self.dmg = 50
        self.max_move = 30
        self.type = 'standard'


class CannonAiBullet(Bullet):

    bullet = r'Assets\TankParts\AiTank\green_bullet_big.png'

    def __init__(self):
        super().__init__()
        self.spd = 12.5
        self.dmg = 300
        self.max_move = 36
        self.type = 'cannon'


class RedBossBullet(Bullet):

    bullet = r'Assets\TankParts\AiTank\red_boss_bullet_small.png'

    def __init__(self):
        super().__init__()
        self.spd = 15
        self.dmg = 75
        self.max_move = 30
        self.type = 'redBoss'
