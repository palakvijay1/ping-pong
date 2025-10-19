import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 50)
        
        # Load score sound (for Task 4, assuming 'sounds/score.wav' exists)
        try:
            self.score_sound = pygame.mixer.Sound("sounds/score.wav")
        except:
            self.score_sound = None

        self.player_score = 0
        self.ai_score = 0
        self.max_score = 5 # Default best of 5
        self.game_over = False
        self.winner_text = ""
        
        # Replay options mapping requested key to max score
        self.replay_options = {
            pygame.K_3: 3,  # Best of 3
            pygame.K_5: 5,  # Best of 5
            pygame.K_7: 7,  # Best of 7
            pygame.K_ESCAPE: "Exit"
        }

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Only allow paddle movement if the game is NOT over
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        # 1. Always check for game over at the start of update
        self.check_game_over()
        
        # 2. If game is over, skip all movement/scoring logic
        if self.game_over:
            return

        # Regular game logic
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Scoring and Reset
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            if self.score_sound: self.score_sound.play()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            if self.score_sound: self.score_sound.play()

        self.ai.auto_track(self.ball, self.height)

    def check_game_over(self):
        # Only update the state, DO NOT draw or quit here.
        if self.player_score >= self.max_score or self.ai_score >= self.max_score:
            self.game_over = True
            if self.player_score >= self.max_score:
                self.winner_text = "AI WINS!" if self.ai_score > self.player_score else "PLAYER WINS!"
            else:
                self.winner_text = "AI WINS!"

    def handle_replay_input(self, event):
        """Processes a single event for replay choice."""
        if not self.game_over:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in self.replay_options:
                choice = self.replay_options[event.key]
                if choice == "Exit":
                    pygame.quit()
                    exit()
                else:
                    self.restart_game(choice)

    def restart_game(self, best_of):
        """Reset scores and start a new game with chosen max score."""
        self.player_score = 0
        self.ai_score = 0
        self.max_score = best_of
        self.ball.reset()
        self.game_over = False
        self.winner_text = ""

    def render(self, screen):
        # Draw game elements only if NOT game over
        if not self.game_over:
            # Draw game objects
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

            # Draw score
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width // 4, 20))
            screen.blit(ai_text, (self.width * 3 // 4, 20))
        
        # Draw game over screen
        else:
            screen.fill((0, 0, 0)) # Clear the screen
            
            # Winner Text
            winner_display = self.big_font.render(self.winner_text, True, (255, 0, 0))
            screen.blit(winner_display, (self.width // 2 - winner_display.get_width() // 2, self.height // 2 - 100))
            
            # Final Score
            score_text = self.font.render(f"Final Score: {self.player_score} - {self.ai_score}", True, WHITE)
            screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, self.height // 2 - 40))
            
            # Display Replay Options
            y_offset = self.height // 2 + 20
            
            options_map = {
                pygame.K_3: "Best of 3",
                pygame.K_5: "Best of 5",
                pygame.K_7: "Best of 7",
                pygame.K_ESCAPE: "Quit"
            }
            
            for key, option in options_map.items():
                text = f"Press {pygame.key.name(key).upper()} for {option}"
                option_text = self.font.render(text, True, WHITE)
                screen.blit(option_text, (self.width // 2 - option_text.get_width() // 2, y_offset))
                y_offset += 40