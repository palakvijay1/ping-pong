import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        self.paddle_sound = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.wall_sound = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("sounds/score.wav")

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_sound.play() 

    def check_collision(self, player, ai):
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        # Collision with Player Paddle (only check if moving left)
        if ball_rect.colliderect(player_rect) and self.velocity_x < 0:
            self.velocity_x *= -1
            # Reposition to prevent tunneling/sticking
            self.x = player_rect.right 
            self.paddle_sound.play()

        # Collision with AI Paddle (only check if moving right)
        elif ball_rect.colliderect(ai_rect) and self.velocity_x > 0:
            self.velocity_x *= -1
            # Reposition to prevent tunneling/sticking
            self.x = ai_rect.left - self.width
            self.paddle_sound.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
