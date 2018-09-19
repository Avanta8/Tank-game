class Turret:
    pass


class StdTurret(Turret):

    turret = r'Assets\TankParts\UserTank\blue_turret_std.png'

    def __init__(self):
        self.type = 'standard'


class MinigunTurret(Turret):

    turret = r'Assets\TankParts\UserTank\blue_turret_minigun.png'
    last_turret_shot = {'left'}
    all_turrets = {'left', 'right'}

    def __init__(self):
        self.type = 'minigun'


class CannonTurret(Turret):

    turret = r'Assets\TankParts\UserTank\blue_turret_big.png'

    def __init__(self):
        self.type = 'cannon'


class StdAiTurret(Turret):

    turret = r'Assets\TankParts\AiTank\red_turret_std.png'

    def __init__(self):
        self.type = 'standard'


class CannonAiTurret(Turret):

    turret = r'Assets\TankParts\AiTank\green_turret_big.png'

    def __init__(self):
        self.type = 'cannon'


class RedBossTurretMain(Turret):

    turret = r'Assets\TankParts\AiTank\red_boss_turret_main.png'

    def __init__(self):
        self.type = 'redBoss'


class RedBossTurretLeft(Turret):

    turret = r'Assets\TankParts\AiTank\red_boss_turret_left.png'

    def __init__(self):
        self.type = 'redBoss'


class RedBossTurretRight(Turret):

    turret = r'Assets\TankParts\AiTank\red_boss_turret_right.png'

    def __init__(self):
        self.type = 'redBoss'
