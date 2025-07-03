
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

        # Health
        self.max_hp = 50
        self.hp = self.max_hp

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
        # Player tracking logic
        if self.player:
            if self.player.rect.x < self.rect.x:
                self.direction = -1 # Move left towards player
                self.facing_right = False
            elif self.player.rect.x > self.rect.x:
                self.direction = 1 # Move right towards player
                self.facing_right = True
            else:
                self.direction = 0 # Stop if aligned horizontally

        # Simple horizontal movement
        self.rect.x += self.speed * self.direction

        # Determine current animation state
        if self.direction != 0: # Walking
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

    def draw(self, screen):
        if self.facing_right:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
