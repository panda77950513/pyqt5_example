# game_logic.py

from PyQt5.QtCore import QPointF
from .constants import *
import math

class Entity:
    def __init__(self, x, y, radius, color):
        self.pos = QPointF(x, y)
        self.radius = radius
        self.color = color
        self.velocity = QPointF(0, 0)

    def update(self):
        self.pos += self.velocity

    def apply_friction(self, friction):
        if self.velocity.x() != 0 or self.velocity.y() != 0:
            speed = math.sqrt(self.velocity.x()**2 + self.velocity.y()**2)
            if speed > friction:
                self.velocity -= self.velocity / speed * friction
            else:
                self.velocity = QPointF(0, 0)

class Player(Entity):
    def __init__(self, x, y, team_color, team_side, role='midfielder'):
        super().__init__(x, y, PLAYER_RADIUS, team_color)
        self.team_side = team_side # 'left' or 'right'
        self.role = role # 'midfielder', 'forward', 'defender'
        self.has_ball = False
        self.is_controlled = False # Only one player is controlled by user at a time

    def move(self, dx, dy):
        self.velocity += QPointF(dx * PLAYER_ACCELERATION, dy * PLAYER_ACCELERATION)
        speed = math.sqrt(self.velocity.x()**2 + self.velocity.y()**2)
        if speed > PLAYER_SPEED:
            self.velocity = self.velocity / speed * PLAYER_SPEED

    def update(self):
        super().update()
        self.apply_friction(PLAYER_FRICTION)

    def update_ai(self, game_state):
        # Simple AI: move towards the ball
        ball_pos = game_state.ball.pos
        
        # Determine target based on role and ball position
        target_x, target_y = self.pos.x(), self.pos.y() # Default: stay put

        # If ball is closer to this player than any opponent, try to get it
        dist_to_ball = game_state.distance(self.pos, ball_pos)
        closest_opponent_dist = float('inf')
        for opponent in game_state.get_opponent_team(self.team_side).players:
            closest_opponent_dist = min(closest_opponent_dist, game_state.distance(opponent.pos, ball_pos))

        if dist_to_ball < closest_opponent_dist + 50: # Ball is relatively closer
            target_x, target_y = ball_pos.x(), ball_pos.y()
        else:
            # Return to general position based on role
            if self.team_side == 'left':
                if self.role == 'defender': target_x = FIELD_X + FIELD_WIDTH * 0.2
                elif self.role == 'midfielder': target_x = FIELD_X + FIELD_WIDTH * 0.4
                elif self.role == 'forward': target_x = FIELD_X + FIELD_WIDTH * 0.6
            else: # right team
                if self.role == 'defender': target_x = FIELD_X + FIELD_WIDTH * 0.8
                elif self.role == 'midfielder': target_x = FIELD_X + FIELD_WIDTH * 0.6
                elif self.role == 'forward': target_x = FIELD_X + FIELD_WIDTH * 0.4
            target_y = FIELD_Y + FIELD_HEIGHT / 2 # Center vertically for simplicity

        # Move towards target
        dx = target_x - self.pos.x()
        dy = target_y - self.pos.y()
        
        # Normalize direction and apply speed
        dist_to_target = math.sqrt(dx**2 + dy**2)
        if dist_to_target > 10: # Only move if far enough from target
            self.move(dx / dist_to_target, dy / dist_to_target)
        else:
            self.velocity = QPointF(0,0) # Stop if close enough

class Ball(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_RADIUS, COLOR_BALL)

    def update(self):
        super().update()
        self.apply_friction(BALL_FRICTION)

class Team:
    def __init__(self, color, side):
        self.color = color
        self.players = []
        self.score = 0
        self.side = side # 'left' or 'right'

    def add_player(self, player):
        self.players.append(player)

class Game:
    def __init__(self):
        self.ball = Ball(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        self.red_team = Team(COLOR_RED_TEAM, 'left')
        self.blue_team = Team(COLOR_BLUE_TEAM, 'right')

        # 플레이어 초기화 (역할 부여)
        # Red Team
        self.red_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.2, FIELD_Y + FIELD_HEIGHT / 2, COLOR_RED_TEAM, 'left', role='midfielder'))
        self.red_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.1, FIELD_Y + FIELD_HEIGHT * 0.25, COLOR_RED_TEAM, 'left', role='defender'))
        self.red_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.1, FIELD_Y + FIELD_HEIGHT * 0.75, COLOR_RED_TEAM, 'left', role='defender'))
        
        # Blue Team
        self.blue_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.8, FIELD_Y + FIELD_HEIGHT / 2, COLOR_BLUE_TEAM, 'right', role='midfielder'))
        self.blue_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.9, FIELD_Y + FIELD_HEIGHT * 0.25, COLOR_BLUE_TEAM, 'right', role='defender'))
        self.blue_team.add_player(Player(FIELD_X + FIELD_WIDTH * 0.9, FIELD_Y + FIELD_HEIGHT * 0.75, COLOR_BLUE_TEAM, 'right', role='defender'))

        self.controlled_player = None # Initially no player controlled
        self.set_controlled_player()

        self.score_red = 0
        self.score_blue = 0
        self.game_time = GAME_DURATION

    def update(self, keys_pressed):
        self.set_controlled_player() # Update controlled player each frame

        # Update controlled player based on user input
        dx, dy = 0, 0
        if keys_pressed.get('left'): dx -= 1
        if keys_pressed.get('right'): dx += 1
        if keys_pressed.get('up'): dy -= 1
        if keys_pressed.get('down'): dy += 1
        if self.controlled_player:
            self.controlled_player.move(dx, dy)

        # Update all players (AI for non-controlled players)
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                if not player.is_controlled:
                    player.update_ai(self)
                player.update()
                self.confine_to_field(player)

        # Update ball
        self.ball.update()
        self.confine_to_field(self.ball)

        # Player-ball collision and possession
        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                dist = self.distance(player.pos, self.ball.pos)
                if dist < player.radius + self.ball.radius:
                    # Player has ball possession
                    player.has_ball = True
                    self.ball.pos = player.pos + (self.ball.pos - player.pos) / dist * (player.radius + self.ball.radius + 1) # Keep ball slightly in front
                    self.ball.velocity = player.velocity # Ball moves with player

                    # Simple kick/pass
                    if player.is_controlled and keys_pressed.get('space'):
                        kick_direction = QPointF(0,0)
                        if keys_pressed.get('left'): kick_direction.setX(-1)
                        if keys_pressed.get('right'): kick_direction.setX(1)
                        if keys_pressed.get('up'): kick_direction.setY(-1)
                        if keys_pressed.get('down'): kick_direction.setY(1)

                        if kick_direction.isNull(): # If no direction, kick forward
                            kick_direction = QPointF(1, 0) if player.team_side == 'right' else QPointF(-1, 0)

                        kick_direction_norm = kick_direction / math.sqrt(kick_direction.x()**2 + kick_direction.y()**2)
                        self.ball.velocity = kick_direction_norm * BALL_SPEED
                        player.has_ball = False # Lose possession after kick
                    break # Only one player can have the ball at a time
                else:
                    player.has_ball = False

        # Goal detection
        if (self.ball.pos.x() < FIELD_X + GOAL_WIDTH / 2 and 
           FIELD_Y + FIELD_HEIGHT / 2 - GOAL_HEIGHT / 2 < self.ball.pos.y() < FIELD_Y + FIELD_HEIGHT / 2 + GOAL_HEIGHT / 2):
            self.score_blue += 1
            self.reset_ball_and_players()
        elif (self.ball.pos.x() > FIELD_X + FIELD_WIDTH - GOAL_WIDTH / 2 and 
             FIELD_Y + FIELD_HEIGHT / 2 - GOAL_HEIGHT / 2 < self.ball.pos.y() < FIELD_Y + FIELD_HEIGHT / 2 + GOAL_HEIGHT / 2):
            self.score_red += 1
            self.reset_ball_and_players()

    def confine_to_field(self, entity):
        # Confine to field boundaries
        if entity.pos.x() - entity.radius < FIELD_X:
            entity.pos.setX(FIELD_X + entity.radius)
            entity.velocity.setX(-entity.velocity.x() * 0.8) # Bounce
        elif entity.pos.x() + entity.radius > FIELD_X + FIELD_WIDTH:
            entity.pos.setX(FIELD_X + FIELD_WIDTH - entity.radius)
            entity.velocity.setX(-entity.velocity.x() * 0.8)

        if entity.pos.y() - entity.radius < FIELD_Y:
            entity.pos.setY(FIELD_Y + entity.radius)
            entity.velocity.setY(-entity.velocity.y() * 0.8)
        elif entity.pos.y() + entity.radius > FIELD_Y + FIELD_HEIGHT:
            entity.pos.setY(FIELD_Y + FIELD_HEIGHT - entity.radius)
            entity.velocity.setY(-entity.velocity.y() * 0.8)

    def distance(self, p1, p2):
        return math.sqrt((p1.x() - p2.x())**2 + (p1.y() - p2.y())**2)

    def set_controlled_player(self):
        closest_player = None
        min_dist = float('inf')

        for player in self.red_team.players:
            dist = self.distance(player.pos, self.ball.pos)
            if dist < min_dist:
                min_dist = dist
                closest_player = player
        
        # Set the closest player as controlled and others as not controlled
        for player in self.red_team.players:
            player.is_controlled = (player == closest_player)
        self.controlled_player = closest_player

    def get_opponent_team(self, current_team_side):
        if current_team_side == 'left':
            return self.blue_team
        else:
            return self.red_team

    def reset_ball_and_players(self):
        self.ball.pos = QPointF(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.ball.velocity = QPointF(0, 0)
        
        # Reset player positions based on their roles and team side
        # Red Team (left side)
        self.red_team.players[0].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.2, FIELD_Y + FIELD_HEIGHT / 2) # Midfielder
        self.red_team.players[1].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.1, FIELD_Y + FIELD_HEIGHT * 0.25) # Defender
        self.red_team.players[2].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.1, FIELD_Y + FIELD_HEIGHT * 0.75) # Defender
        
        # Blue Team (right side)
        self.blue_team.players[0].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.8, FIELD_Y + FIELD_HEIGHT / 2) # Midfielder
        self.blue_team.players[1].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.9, FIELD_Y + FIELD_HEIGHT * 0.25) # Defender
        self.blue_team.players[2].pos = QPointF(FIELD_X + FIELD_WIDTH * 0.9, FIELD_Y + FIELD_HEIGHT * 0.75) # Defender

        for team in [self.red_team, self.blue_team]:
            for player in team.players:
                player.velocity = QPointF(0, 0)
                player.has_ball = False