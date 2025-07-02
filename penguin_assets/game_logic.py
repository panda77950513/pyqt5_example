# game_logic.py

from PyQt5.QtCore import QPoint, QRectF
from .game_map import EMPTY, WALL, BLOCK, MAP_WIDTH, MAP_HEIGHT, ROUND_DATA
import random

class Player:
    def __init__(self, start_pos):
        self.x, self.y = start_pos[1], start_pos[0]
        self.lives = 3
        self.score = 0
        self.is_moving = False
        self.move_target = None
        self.move_progress = 0 # 0 to TILE_SIZE

    def update_movement(self):
        if self.is_moving:
            self.move_progress += 8 # 이동 속도 증가 (원작 느낌에 가깝게)
            if self.move_progress >= 40: # TILE_SIZE
                self.x, self.y = self.move_target
                self.is_moving = False
                self.move_progress = 0

    def get_pixel_pos(self):
        if self.is_moving:
            if self.move_target[0] > self.x: # Moving Right
                return self.x * 40 + self.move_progress, self.y * 40
            elif self.move_target[0] < self.x: # Moving Left
                return self.x * 40 - self.move_progress, self.y * 40
            elif self.move_target[1] > self.y: # Moving Down
                return self.x * 40, self.y * 40 + self.move_progress
            elif self.move_target[1] < self.y: # Moving Up
                return self.x * 40, self.y * 40 - self.move_progress
        return self.x * 40, self.y * 40

class IceBlock:
    def __init__(self, pos):
        self.x, self.y = pos[1], pos[0]
        self.is_sliding = False
        self.slide_direction = None # (dx, dy)
        self.slide_target = None
        self.slide_progress = 0

    def update_sliding(self):
        if self.is_sliding:
            self.slide_progress += 16 # 슬라이딩 속도 증가 (플레이어보다 빠르게)
            if self.slide_progress >= 40: # TILE_SIZE
                self.x, self.y = self.slide_target
                self.is_sliding = False
                self.slide_progress = 0
                self.slide_direction = None

    def get_pixel_pos(self):
        if self.is_sliding:
            if self.slide_direction[0] > 0: # Sliding Right
                return self.x * 40 + self.slide_progress, self.y * 40
            elif self.slide_direction[0] < 0: # Sliding Left
                return self.x * 40 - self.slide_progress, self.y * 40
            elif self.slide_direction[1] > 0: # Sliding Down
                return self.x * 40, self.y * 40 + self.slide_progress
            elif self.slide_direction[1] < 0: # Sliding Up
                return self.x * 40, self.y * 40 - self.slide_progress
        return self.x * 40, self.y * 40

class Enemy:
    def __init__(self, start_pos):
        self.x, self.y = start_pos[1], start_pos[0]
        self.is_moving = False
        self.move_target = None
        self.move_progress = 0
        self.speed = 2 # 적 이동 속도 (조정됨)

    def update_movement(self):
        if self.is_moving:
            self.move_progress += self.speed
            if self.move_progress >= 40:
                self.x, self.y = self.move_target
                self.is_moving = False
                self.move_progress = 0

    def get_pixel_pos(self):
        if self.is_moving:
            if self.move_target[0] > self.x: # Moving Right
                return self.x * 40 + self.move_progress, self.y * 40
            elif self.move_target[0] < self.x: # Moving Left
                return self.x * 40 - self.move_progress, self.y * 40
            elif self.move_target[1] > self.y: # Moving Down
                return self.x * 40, self.y * 40 + self.move_progress
            elif self.move_target[1] < self.y: # Moving Up
                return self.x * 40, self.y * 40 - self.move_progress
        return self.x * 40, self.y * 40

    def choose_direction(self, game_map, player_pos):
        # 간단한 AI: 플레이어 방향으로 이동 시도
        possible_moves = []
        current_pos = (self.y, self.x)

        # 상하좌우
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions) # 무작위성 추가

        for dy, dx in directions:
            new_y, new_x = self.y + dy, self.x + dx
            if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                # 벽이나 블록이 없는 빈 공간으로만 이동
                if game_map[new_y][new_x] == EMPTY:
                    possible_moves.append((new_y, new_x))
        
        if possible_moves:
            # 플레이어에게 가까워지는 방향 우선
            best_move = None
            min_dist = float('inf')
            for move_y, move_x in possible_moves:
                dist = abs(move_y - player_pos[1]) + abs(move_x - player_pos[0])
                if dist < min_dist:
                    min_dist = dist
                    best_move = (move_y, move_x)
            
            if best_move: # 플레이어에게 가까워지는 방향으로 이동
                self.move_target = (best_move[1], best_move[0])
                self.is_moving = True
                return

        # 갈 곳이 없으면 제자리
        self.is_moving = False

class GameState:
    def __init__(self, round_data):
        self.current_map = [row[:] for row in round_data['map']]
        self.player = Player(round_data['player_start'])
        self.ice_blocks = []
        for block_pos in round_data['blocks']:
            self.ice_blocks.append(IceBlock(block_pos))
            self.current_map[block_pos[0]][block_pos[1]] = BLOCK

        self.enemies = []
        for enemy_pos in round_data['enemy_starts']:
            self.enemies.append(Enemy(enemy_pos))

        self.game_over = False
        self.round_cleared = False

    def get_tile_at(self, x, y):
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.current_map[y][x]
        return WALL # 맵 밖은 벽으로 간주

    def get_block_at(self, x, y):
        for block in self.ice_blocks:
            if block.x == x and block.y == y:
                return block
        return None

    def get_enemy_at(self, x, y):
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None

    def move_player(self, dx, dy):
        if self.player.is_moving: return

        new_x, new_y = self.player.x + dx, self.player.y + dy
        target_tile = self.get_tile_at(new_x, new_y)

        if target_tile == EMPTY:
            self.player.move_target = (new_x, new_y)
            self.player.is_moving = True
        elif target_tile == BLOCK:
            block = self.get_block_at(new_x, new_y)
            if block and not block.is_sliding:
                # 블록을 밀 수 있는지 확인
                block_target_x, block_target_y = new_x + dx, new_y + dy
                block_target_tile = self.get_tile_at(block_target_x, block_target_y)
                if block_target_tile == EMPTY: # Only push if the space *behind* the block is empty
                    # 블록 이동
                    self.current_map[block.y][block.x] = EMPTY
                    block.slide_target = (block_target_x, block_target_y)
                    block.slide_direction = (dx, dy)
                    block.is_sliding = True
                    self.current_map[block_target_y][block_target_x] = BLOCK

                    # 플레이어 이동
                    self.player.move_target = (new_x, new_y)
                    self.player.is_moving = True

    def update_game_state(self):
        self.player.update_movement()
        for block in self.ice_blocks:
            block.update_sliding()
        for enemy in self.enemies:
            enemy.update_movement()
            if not enemy.is_moving:
                enemy.choose_direction(self.current_map, (self.player.x, self.player.y))

        # 적과 플레이어 충돌
        if not self.player.is_moving and self.get_enemy_at(self.player.x, self.player.y):
            self.player.lives -= 1
            # 플레이어 위치 초기화 또는 게임 오버 처리
            if self.player.lives <= 0:
                self.game_over = True
            else:
                # 임시로 플레이어 시작 위치로 되돌림
                self.player.x, self.player.y = ROUND_DATA[1]['player_start'][1], ROUND_DATA[1]['player_start'][0]

        # 블록과 적 충돌 (적 처치)
        enemies_to_remove = []
        for block in self.ice_blocks:
            if block.is_sliding:
                for enemy in self.enemies:
                    if block.x == enemy.x and block.y == enemy.y and not enemy.is_moving:
                        enemies_to_remove.append(enemy)
                        self.player.score += 100 # 적 처치 점수
        
        for enemy in enemies_to_remove:
            if enemy in self.enemies: # 중복 제거 방지
                self.enemies.remove(enemy)

        # 라운드 클리어 조건
        if not self.enemies and not self.game_over:
            self.round_cleared = True
