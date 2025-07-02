import random
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QPen
from PyQt5.QtCore import Qt, QTimer
from .game_logic import Player, Bullet, Enemy, Boss, PLAYER_SPEED, PLAYER_BULLET_SPEED, STAGE_CONFIG

class GameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 800)
        self.init_game()

    def init_game(self):
        self.player = Player(self.width() / 2 - 25, self.height() - 70, 50, 50)
        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.boss_enemy = None
        self.game_over = False
        self.game_cleared = False
        self.current_stage = 1

        self.keys_pressed = set()

        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(16) # 약 60 FPS
        
        self.enemy_shoot_timer = QTimer(self)
        self.enemy_shoot_timer.timeout.connect(self.enemies_shoot)

        self.spawn_entities_for_stage()

    def spawn_entities_for_stage(self):
        stage_info = STAGE_CONFIG.get(self.current_stage)
        if not stage_info:
            self.game_cleared = True
            self.game_timer.stop()
            self.enemy_shoot_timer.stop()
            return

        self.enemies = []
        self.enemy_bullets = []
        self.boss_enemy = None

        if stage_info['boss']:
            boss_size = stage_info['boss_size']
            boss_health = stage_info['boss_health']
            self.boss_enemy = Boss(self.width() / 2 - boss_size[0] / 2, 50, boss_size[0], boss_size[1], boss_health)
        else:
            for i in range(stage_info['enemies']):
                enemy_x = random.randint(0, self.width() - 40)
                enemy_y = random.randint(50, 200)
                self.enemies.append(Enemy(enemy_x, enemy_y, 40, 40, stage_info['enemy_speed']))
        
        # 적 총알 발사 타이머 설정
        if stage_info['enemy_shoot_interval'] > 0:
            self.enemy_shoot_timer.start(stage_info['enemy_shoot_interval'])
        else:
            self.enemy_shoot_timer.stop()

    def game_loop(self):
        if self.game_over or self.game_cleared:
            return

        # 플레이어 이동
        if Qt.Key_Left in self.keys_pressed:
            self.player.move(-PLAYER_SPEED, self.width())
        if Qt.Key_Right in self.keys_pressed:
            self.player.move(PLAYER_SPEED, self.width())

        # 플레이어 총알 이동
        for bullet in list(self.player_bullets):
            bullet.move()
            if bullet.rect.bottom() < 0:
                self.player_bullets.remove(bullet)

        # 적 이동
        for enemy in self.enemies:
            enemy.move()
        if self.boss_enemy:
            self.boss_enemy.move()

        # 적 총알 이동
        for bullet in list(self.enemy_bullets):
            bullet.move()
            if bullet.rect.top() > self.height():
                self.enemy_bullets.remove(bullet)

        # 충돌 감지
        self.check_collisions()

        # 스테이지 클리어 조건
        if not self.enemies and not self.boss_enemy and not self.game_over:
            self.enemy_shoot_timer.stop() # 스테이지 클리어 시 적 총알 발사 타이머 중지
            self.current_stage += 1
            self.spawn_entities_for_stage()

        # 게임 오버 조건
        if self.player.lives <= 0:
            self.game_over = True

        self.update()

    def enemies_shoot(self):
        if self.game_over or self.game_cleared:
            return

        # 적이나 보스가 없으면 아무것도 하지 않음
        if not self.enemies and not self.boss_enemy:
            return

        if self.boss_enemy:
            bullets = self.boss_enemy.shoot()
            self.enemy_bullets.extend(bullets)
        elif self.enemies: # 일반 적이 있을 경우에만
            shooter = random.choice(self.enemies)
            self.enemy_bullets.append(shooter.shoot())

    def check_collisions(self):
        bullets_to_remove = set()
        enemies_to_remove = set()
        enemy_bullets_to_remove = set()

        # 플레이어 총알과 적 충돌
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if bullet.rect.intersects(enemy.rect):
                    bullets_to_remove.add(bullet)
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemies_to_remove.add(enemy)
                        self.player.score += 100
                    break # 총알은 하나의 적에게만 영향을 줌

        # 플레이어 총알과 보스 충돌
        if self.boss_enemy:
            for bullet in self.player_bullets:
                if bullet.rect.intersects(self.boss_enemy.rect):
                    bullets_to_remove.add(bullet)
                    self.boss_enemy.health -= 1
                    if self.boss_enemy.health <= 0:
                        self.player.score += 1000 # 보스 처치 점수
                        self.boss_enemy = None # 보스 제거
                    break # 총알은 보스에게만 영향을 줌

        # 적 총알과 플레이어 충돌
        for bullet in self.enemy_bullets:
            if bullet.rect.intersects(self.player.rect):
                enemy_bullets_to_remove.add(bullet)
                self.player.lives -= 1
                break # 플레이어는 하나의 총알에만 맞음

        # 적/보스와 플레이어 충돌 (게임 오버)
        for enemy in self.enemies:
            if enemy.rect.intersects(self.player.rect):
                self.game_over = True
                break
        if self.boss_enemy and self.boss_enemy.rect.intersects(self.player.rect):
            self.game_over = True

        # 제거할 객체들을 실제 리스트에서 제거
        self.player_bullets = [b for b in self.player_bullets if b not in bullets_to_remove]
        self.enemies = [e for e in self.enemies if e not in enemies_to_remove]
        self.enemy_bullets = [b for b in self.enemy_bullets if b not in enemy_bullets_to_remove]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 배경
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRect(self.rect())

        # 플레이어
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawRect(self.player.rect)

        # 플레이어 총알
        painter.setBrush(QBrush(QColor(255, 255, 0)))
        for bullet in self.player_bullets:
            painter.drawRect(bullet.rect)

        # 적
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        for enemy in self.enemies:
            painter.drawRect(enemy.rect)

        # 보스
        if self.boss_enemy:
            painter.setBrush(QBrush(QColor(255, 100, 0)))
            painter.drawRect(self.boss_enemy.rect)
            # 보스 체력 바
            health_bar_width = self.boss_enemy.rect.width()
            health_bar_height = 5
            health_bar_x = self.boss_enemy.rect.left()
            health_bar_y = self.boss_enemy.rect.top() - 10
            
            painter.setBrush(QBrush(QColor(100, 100, 100)))
            painter.drawRect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
            
            current_health_width = (self.boss_enemy.health / self.boss_enemy.max_health) * health_bar_width
            painter.setBrush(QBrush(QColor(0, 255, 0)))
            painter.drawRect(health_bar_x, health_bar_y, current_health_width, health_bar_height)

        # 적 총알
        painter.setBrush(QBrush(QColor(0, 255, 255)))
        for bullet in self.enemy_bullets:
            painter.drawRect(bullet.rect)

        # 점수, 생명력, 스테이지 표시
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont('Arial', 16))
        painter.drawText(10, 25, f"Score: {self.player.score}")
        painter.drawText(10, 50, f"Lives: {self.player.lives}")
        painter.drawText(10, 75, f"Stage: {self.current_stage}")

        # 게임 오버 화면
        if self.game_over:
            painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # 반투명 검은색
            painter.drawRect(self.rect())
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont('Arial', 40, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME OVER\nPress 'R' to Restart")
        
        # 게임 클리어 화면
        if self.game_cleared:
            painter.setBrush(QBrush(QColor(0, 0, 0, 150))) # 반투명 검은색
            painter.drawRect(self.rect())
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont('Arial', 40, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "GAME CLEARED!\nPress 'R' to Play Again")

    def keyPressEvent(self, event):
        if self.game_over or self.game_cleared:
            if event.key() == Qt.Key_R:
                self.init_game()
            return
            
        self.keys_pressed.add(event.key())
        if event.key() == Qt.Key_Space:
            # 총알 발사
            bullet_x = self.player.rect.center().x() - 2.5 # 총알 너비의 절반
            bullet_y = self.player.rect.top()
            self.player_bullets.append(Bullet(bullet_x, bullet_y, 5, 10, PLAYER_BULLET_SPEED))

    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())