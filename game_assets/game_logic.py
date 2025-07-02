from PyQt5.QtCore import QRectF

# 게임 설정
GRAVITY = 0.5
JUMP_STRENGTH = -12
MOVE_SPEED = 5

class Player:
    def __init__(self):
        self.rect = QRectF(150, 100, 30, 50) # x, y, width, height
        self.y_velocity = 0
        self.is_jumping = False

    def move(self, dx):
        self.rect.moveLeft(self.rect.left() + dx)

    def jump(self):
        if not self.is_jumping:
            self.y_velocity = JUMP_STRENGTH
            self.is_jumping = True

    def update(self, platforms):
        # 중력 적용
        self.y_velocity += GRAVITY
        self.rect.moveTop(self.rect.top() + self.y_velocity)

        # 플랫폼 충돌 확인
        self.is_jumping = True
        for p in platforms:
            if self.rect.bottom() > p.rect.top() and self.rect.bottom() < p.rect.top() + 20 and \
               self.rect.right() > p.rect.left() and self.rect.left() < p.rect.right() and self.y_velocity > 0:
                self.rect.moveBottom(p.rect.top())
                self.y_velocity = 0
                self.is_jumping = False
                # 움직이는 발판에 올라탔을 때 플레이어도 함께 움직임
                if isinstance(p, MovingPlatform):
                    self.rect.moveLeft(self.rect.left() + p.speed)
                break

class Platform:
    def __init__(self, x, y, w, h):
        self.rect = QRectF(x, y, w, h)

class MovingPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.speed = 2
        self.initial_x = x
        self.move_range = 100

    def update(self):
        self.rect.moveLeft(self.rect.left() + self.speed)
        if self.rect.left() < self.initial_x - self.move_range or \
           self.rect.left() > self.initial_x + self.move_range:
            self.speed *= -1

class Hazard:
    def __init__(self, x, y, w, h):
        self.rect = QRectF(x, y, w, h)