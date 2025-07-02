from PyQt5.QtCore import QRectF

# 게임 설정
PLAYER_SPEED = 5
PLAYER_BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5

# 스테이지별 설정
STAGE_CONFIG = {
    1: {'enemies': 10, 'enemy_speed': 2, 'enemy_shoot_interval': 1000, 'boss': False},
    2: {'enemies': 15, 'enemy_speed': 3, 'enemy_shoot_interval': 800, 'boss': False},
    3: {'enemies': 0, 'enemy_speed': 0, 'enemy_shoot_interval': 0, 'boss': True, 'boss_health': 100, 'boss_size': (80, 80)},
    4: {'enemies': 20, 'enemy_speed': 4, 'enemy_shoot_interval': 600, 'boss': False},
    # 더 많은 스테이지를 추가할 수 있습니다.
}

class Player:
    def __init__(self, x, y, width, height):
        self.rect = QRectF(x, y, width, height)
        self.lives = 3
        self.score = 0

    def move(self, dx, game_width):
        self.rect.moveLeft(self.rect.left() + dx)
        # 화면 밖으로 나가지 않도록 제한
        if self.rect.left() < 0:
            self.rect.setLeft(0)
        if self.rect.right() > game_width:
            self.rect.setRight(game_width)

class Bullet:
    def __init__(self, x, y, width, height, speed, is_player_bullet=True):
        self.rect = QRectF(x, y, width, height)
        self.speed = speed
        self.is_player_bullet = is_player_bullet

    def move(self):
        if self.is_player_bullet:
            self.rect.moveTop(self.rect.top() - self.speed)
        else:
            self.rect.moveTop(self.rect.top() + self.speed)

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = QRectF(x, y, width, height)
        self.direction = 1 # 1: 오른쪽, -1: 왼쪽
        self.move_counter = 0
        self.max_move = 100 # 좌우 이동 범위
        self.speed = speed
        self.health = 1 # 일반 적은 체력 1

    def move(self):
        self.rect.moveLeft(self.rect.left() + self.direction * self.speed)
        self.move_counter += 1
        if self.move_counter >= self.max_move:
            self.direction *= -1
            self.move_counter = 0
            self.rect.moveTop(self.rect.top() + 20) # 아래로 조금 이동

    def shoot(self):
        bullet_x = self.rect.center().x() - 2.5 # 총알 너비의 절반
        bullet_y = self.rect.bottom()
        return Bullet(bullet_x, bullet_y, 5, 10, ENEMY_BULLET_SPEED, is_player_bullet=False)

class Boss(Enemy):
    def __init__(self, x, y, width, height, health, speed=1):
        super().__init__(x, y, width, height, speed)
        self.health = health
        self.max_health = health
        self.direction = 1 # 1: 오른쪽, -1: 왼쪽
        self.move_counter = 0
        self.max_move = 200 # 보스의 좌우 이동 범위

    def move(self):
        self.rect.moveLeft(self.rect.left() + self.direction * self.speed)
        self.move_counter += 1
        if self.move_counter >= self.max_move:
            self.direction *= -1
            self.move_counter = 0
            # 보스는 아래로 이동하지 않음

    def shoot(self):
        # 보스는 여러 발의 총알을 발사할 수 있도록 구현 가능
        bullets = []
        bullets.append(Bullet(self.rect.center().x() - 10, self.rect.bottom(), 5, 10, ENEMY_BULLET_SPEED, is_player_bullet=False))
        bullets.append(Bullet(self.rect.center().x() + 5, self.rect.bottom(), 5, 10, ENEMY_BULLET_SPEED, is_player_bullet=False))
        return bullets