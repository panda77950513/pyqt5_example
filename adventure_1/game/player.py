import pygame
from game.resources import load_image, load_animation_frames

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load animation frames
        self.run_frames = load_animation_frames("Samurai/Walk.png", 32, 64)
        self.idle_frames = load_animation_frames("Samurai/Idle.png", 32, 64)
        self.jump_frames = load_animation_frames("Samurai/Jump.png", 32, 64)
        self.attack_frames = load_animation_frames("Samurai/Attack_1.png", 32, 64) # Attack_1.png를 예시로 사용

        # Fallback to placeholder if frames are not loaded
        if not self.run_frames: self.run_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.run_frames[0].fill((0,255,0))
        if not self.idle_frames: self.idle_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.idle_frames[0].fill((0,200,0))
        if not self.jump_frames: self.jump_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.jump_frames[0].fill((0,150,0))
        if not self.attack_frames: self.attack_frames = [pygame.Surface((64,64), pygame.SRCALPHA)]; self.attack_frames[0].fill((255,100,0))

        self.image = self.idle_frames[0] # Initial image is idle
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False

        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_duration = 10 # frames
        self.attack_power = 10 # 플레이어 공격력 추가

        # Health
        self.max_hp = 100
        self.hp = self.max_hp

        # Animation variables
        self.current_frame_index = 0
        self.animation_speed = 0.1 # Adjust for faster/slower animation
        self.animation_timer = 0
        self.facing_right = True # Direction player is facing
        self.state = "idle" # Current animation state: "idle", "running", "jumping", "attacking"
        self.attack_just_started = False # 새로운 공격이 시작되었는지 여부

    def take_damage(self, amount):
        self.hp -= amount
        print(f"Player took {amount} damage. HP: {self.hp}")
        if self.hp <= 0:
            print("Player defeated!")
            return True # Player is defeated
        return False # Player is still alive

    def handle_event(self, event):
        # print(f"Player: Handling event - Type: {event.type}, Key: {event.key}")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("Player: Moving left")
                self.vel_x = -self.speed
                self.facing_right = False
            elif event.key == pygame.K_RIGHT:
                # print("Player: Moving right")
                self.vel_x = self.speed
                self.facing_right = True
            elif event.key == pygame.K_SPACE:
                if self.on_ground:
                    # print("Player: Jumping")
                    self.vel_y = self.jump_power
                    self.on_ground = False
                    self.state = "jumping"
            elif event.key == pygame.K_z: # Basic attack
                if not self.is_attacking and self.attack_cooldown == 0:
                    # print("Player: Attacking")
                    self.is_attacking = True
                    self.attack_just_started = True # 공격 시작 플래그 설정
                    self.attack_cooldown = 30 # Cooldown frames
                    self.state = "attacking"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.vel_x < 0:
                # print("Player: Stopping left")
                self.vel_x = 0
            elif event.key == pygame.K_RIGHT and self.vel_x > 0:
                # print("Player: Stopping right")
                self.vel_x = 0





    def update(self):
        # Apply gravity
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Simple ground collision (for testing, will be replaced by map collision)
        if self.rect.bottom >= 600: # Assuming ground at y=600
            self.rect.bottom = 600
            self.vel_y = 0
            if not self.on_ground: # Only set to idle if just landed
                self.on_ground = True
                if not self.is_attacking: # Don't change state if attacking
                    self.state = "idle"

        # Attack logic
        if self.is_attacking:
            self.attack_duration -= 1
            if self.attack_duration <= 0:
                self.is_attacking = False
                self.attack_duration = 10
                if self.on_ground: # After attack, if on ground, go to idle/running
                    self.state = "idle" if self.vel_x == 0 else "running"
                else: # If in air, stay jumping
                    self.state = "jumping"
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Determine current animation state
        if self.is_attacking:
            current_frames = self.attack_frames
            if self.state != "attacking": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "attacking"
        elif not self.on_ground: # Jumping/Falling
            current_frames = self.jump_frames
            if self.state != "jumping": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "jumping"
        elif self.vel_x != 0: # Running
            current_frames = self.run_frames
            if self.state != "running": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "running"
        else: # Idle
            current_frames = self.idle_frames
            if self.state != "idle": # Reset animation if state just changed
                self.current_frame_index = 0
                self.animation_timer = 0
                self.state = "idle"

        # Update animation frame
        self.animation_timer += self.animation_speed
        if self.animation_timer >= len(current_frames):
            self.animation_timer = 0
            if self.state == "attacking": # Attack animation plays once
                self.is_attacking = False # End attack state after animation
                self.state = "idle" if self.on_ground else "jumping"

        self.current_frame_index = int(self.animation_timer)
        self.image = current_frames[self.current_frame_index]

    def get_attack_rect(self):
        if self.is_attacking:
            attack_width = 50 # 공격 범위 너비
            attack_height = 30 # 공격 범위 높이
            if self.facing_right:
                # 플레이어 오른쪽에 공격 범위 설정
                return pygame.Rect(self.rect.right, self.rect.centery - attack_height // 2, attack_width, attack_height)
            else:
                # 플레이어 왼쪽에 공격 범위 설정
                return pygame.Rect(self.rect.left - attack_width, self.rect.centery - attack_height // 2, attack_width, attack_height)
        return None # 공격 중이 아니면 None 반환

    def draw(self, screen):
        if self.facing_right:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

        # 디버깅용: 공격 판정 범위 시각화 (나중에 제거)
        # if self.is_attacking:
        #     attack_rect = self.get_attack_rect()
        #     if attack_rect:
        #         pygame.draw.rect(screen, (255, 255, 0), attack_rect, 2) # 노란색 테두리

        if self.is_attacking:
            # Draw a simple attack indicator (placeholder) - now handled by animation
            pass