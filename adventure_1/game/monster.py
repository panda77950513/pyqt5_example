
import pygame
from game.resources import load_image, load_animation_frames

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, player=None):
        super().__init__()
        self.player = player # 플레이어 객체 참조
        # Load animation frames
        self.idle_frames = load_animation_frames(["monster_idle_1.png", "monster_idle_2.png"], 64, 64)
        self.walk_frames = load_animation_frames(["monster_walk_1.png", "monster_walk_2.png", "monster_walk_3.png", "monster_walk_4.png"], 64, 64)

        # Fallback to placeholder if frames are not loaded
        if not self.idle_frames: self.idle_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.idle_frames[0].fill((255,0,0))
        if not self.walk_frames: self.walk_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.walk_frames[0].fill((200,0,0))

        self.image = self.idle_frames[0] # Initial image is idle
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 2
        self.direction = 1 # 1 for right, -1 for left
        self.stop_distance = 50 # 플레이어에게 이 거리만큼 가까워지면 멈춤

        # Health
        self.max_hp = 50
        self.hp = self.max_hp

        # Attack
        self.attack_power = 5
        self.attack_cooldown = 60 # 프레임 단위 (1초에 60프레임이면 1초 쿨다운)
        self.attack_timer = 0

        # Animation variables
        self.current_frame_index = 0
        self.animation_speed = 0.1 # Adjust for faster/slower animation
        self.animation_timer = 0
        self.facing_right = True # Direction monster is facing
        self.state = "idle" # Current animation state: "idle", "walking"

    def take_damage(self, amount):
        self.hp -= amount
        print(f"Monster took {amount} damage. HP: {self.hp}")
        if self.hp <= 0:
            print("Monster defeated!")
            return True # Monster is defeated
        return False # Monster is still alive

    def update(self):
        # Update attack timer
        if self.attack_timer > 0:
            self.attack_timer -= 1

        # Player tracking logic
        current_speed = self.speed # 현재 프레임에서 사용할 속도
        if self.player:
            distance_x = self.player.rect.centerx - self.rect.centerx
            # 플레이어와의 거리가 stop_distance 이내이면 멈춤
            if abs(distance_x) < self.stop_distance:
                current_speed = 0
                self.direction = 0 # 정지 상태
                # Attack logic
                if self.attack_timer == 0: # 쿨다운이 지났으면 공격
                    self.attack(self.player)
                    self.attack_timer = self.attack_cooldown
            elif distance_x < 0:
                self.direction = -1 # Move left towards player
                self.facing_right = False
            elif distance_x > 0:
                self.direction = 1 # Move right towards player
                self.facing_right = True

        # Simple horizontal movement
        self.rect.x += current_speed * self.direction

        # Determine current animation state
        if current_speed != 0: # Walking
            current_frames = self.walk_frames
            if self.state != "walking": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "walking"
        else: # Idle (if speed is 0)
            current_frames = self.idle_frames
            if self.state != "idle": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "idle"

        # Update animation frame
        self.animation_timer += self.animation_speed
        if self.animation_timer >= len(current_frames):
            self.animation_timer = 0

        self.current_frame_index = int(self.animation_timer)
        self.image = current_frames[self.current_frame_index]

    def attack(self, target):
        # 몬스터가 플레이어를 공격하는 로직
        print(f"Monster attacks Player! Dealing {self.attack_power} damage.")
        target.take_damage(self.attack_power)

    def draw(self, screen):
        if self.facing_right:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
