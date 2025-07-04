
import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

from game.player import Player
from game.monster import Monster
from game.resources import load_image

class GameEngine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("GameEngine: Initializing...")
        self.setMinimumSize(1280, 720) # Match game resolution
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.pygame_surface = None
        self.pygame_widget = QLabel() # QLabel to display Pygame surface
        self.layout.addWidget(self.pygame_widget)

        self.game_active = False
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.frame_count = 0 # 프레임 카운터 추가

        self.player = None
        self.monsters = []
        self.background = None
        self.hit_monsters_in_current_attack = set() # 현재 공격에서 이미 타격된 몬스터를 추적

        self.init_pygame()
        print("GameEngine: Initialization complete.")

    def init_pygame(self):
        try:
            print("GameEngine: Initializing Pygame...")
            # Pygame is initialized in a headless mode for embedding
            pygame.init()
            pygame.display.set_mode((1, 1), pygame.HIDDEN) # Create a dummy display
            self.screen = pygame.Surface((1280, 720), pygame.SRCALPHA) # Main drawing surface with alpha
            print("GameEngine: Pygame display surface created.")

            # Load game resources
            print("GameEngine: Loading resources...")
            self.background = load_image("background_placeholder.png") # Placeholder
            if self.background:
                self.background = pygame.transform.scale(self.background, (1280, 720))
                print("GameEngine: Background loaded.")
            else:
                print("GameEngine: Failed to load background image.")

            self.player = Player(100, 500) # Initial player position
            print("GameEngine: Player created.")
            self.monsters.append(Monster(800, 500, player=self.player)) # Initial monster position, pass player
            print("GameEngine: Monster created.")
            print("GameEngine: Pygame initialization complete.")
        except Exception as e:
            print(f"GameEngine: Error during Pygame initialization: {e}")
            # Optionally, re-raise or handle more gracefully
            raise

    def get_pygame_widget(self):
        return self.pygame_widget

    def start_game_loop(self):
        print("GameEngine: Starting game loop...")
        self.game_active = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000 // self.fps) # Update at 60 FPS
        print("GameEngine: Game loop timer started.")

    def stop_game_loop(self):
        print("GameEngine: Stopping game loop...")
        self.game_active = False
        if self.timer.isActive():
            self.timer.stop()
        print("GameEngine: Game loop stopped.")

    def game_loop(self):
        # print("GameEngine: Entering game_loop.") # 디버깅용
        if not self.game_active:
            return

        try:
            # Update game state
            self.player.update()
            for monster in self.monsters:
                monster.update()

            # Simple collision detection (placeholder)
            # Player attack collision with monsters
            if self.player.is_attacking:
                player_attack_rect = self.player.get_attack_rect()
                if player_attack_rect:
                    # 새로운 공격이 시작되었으면 hit_monsters_in_current_attack 초기화
                    if self.player.attack_just_started:
                        self.hit_monsters_in_current_attack.clear()
                        self.player.attack_just_started = False

                    monsters_to_remove = []
                    for monster in self.monsters:
                        if monster not in self.hit_monsters_in_current_attack and player_attack_rect.colliderect(monster.rect):
                            # Monster takes damage
                            if monster.take_damage(self.player.attack_power): # Assuming player has attack_power
                                monsters_to_remove.append(monster)
                            self.hit_monsters_in_current_attack.add(monster) # 몬스터를 타격된 목록에 추가
                    for monster in monsters_to_remove:
                        self.monsters.remove(monster)

            # Monster collision with player (for future, e.g., player takes damage)
            for monster in self.monsters:
                if self.player.rect.colliderect(monster.rect):
                    # Handle collision (e.g., player takes damage)
                    pass

            # Drawing
            self.screen.fill((255, 255, 255)) # Clear screen with white
            # if self.background:
            #     self.screen.blit(self.background, (0, 0)) # 배경 이미지 그리는 부분 주석 처리

            self.player.draw(self.screen)
            # Draw player HP
            font = pygame.font.Font(None, 36) # 폰트 설정
            player_hp_text = font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, (0, 0, 0)) # 검정색 텍스트
            self.screen.blit(player_hp_text, (10, 10)) # 화면 좌측 상단에 표시

            for monster in self.monsters:
                monster.draw(self.screen)
                # Draw monster HP
                font = pygame.font.Font(None, 24) # 폰트 설정
                hp_text = font.render(f"HP: {monster.hp}", True, (255, 0, 0)) # 빨간색 텍스트
                self.screen.blit(hp_text, (monster.rect.x, monster.rect.y - 20)) # 몬스터 위에 표시

            # Convert Pygame surface to QImage and display in QLabel
            self.update_pygame_display()

            self.clock.tick(self.fps)
            self.frame_count += 1 # 프레임 카운터 증가
        except Exception as e:
            print(f"GameEngine: Error during game loop: {e}")
            self.stop_game_loop() # Stop the loop to prevent further errors
            # Optionally, show an error message to the user
            raise # Re-raise the exception to see the full traceback

    def handle_key_event(self, event):
        # Pass the event to the player
        self.player.handle_event(event)

    def update_pygame_display(self):
        # Get Pygame surface data
        raw_data = self.screen.get_buffer().raw
        # Calculate bytes per line (stride) for ARGB32 format
        bytes_per_line = self.screen.get_width() * 4
        # Create QImage from Pygame surface data with explicit stride
        qimage = QImage(raw_data, self.screen.get_width(), self.screen.get_height(), bytes_per_line, QImage.Format_ARGB32)
        # Convert QImage to QPixmap and set to QLabel
        self.pygame_widget.setPixmap(QPixmap.fromImage(qimage))

    def __del__(self):
        print("GameEngine: Deleting GameEngine instance. Quitting Pygame.")
        pygame.quit()
