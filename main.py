import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.5
FLAP_STRENGTH = -5
PIPE_WIDTH = 80
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill((255, 0, 0))  # Placeholder for bird image

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= 5

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

    def get_rects(self):
        return (pygame.Rect(self.x, 0, PIPE_WIDTH, self.height),
                pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

# Game loop
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:  # Restart game
                    main()

        if not game_over:
            bird.update()

            # Update pipes
            if pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())
            for pipe in pipes:
                pipe.update()

            # Check for collisions
            if bird.y > SCREEN_HEIGHT or bird.y < 0:  # Check for ground and ceiling
                game_over = True

            for pipe in pipes:
                pipe_rects = pipe.get_rects()
                if bird.get_rect().colliderect(pipe_rects[0]) or bird.get_rect().colliderect(pipe_rects[1]):
                    game_over = True
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1  # Increment score when passing a pipe

            # Draw everything
            screen.fill(WHITE)
            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))

        else:
            # Game over screen
            font = pygame.font.Font(None, 72)
            game_over_text = font.render('Game Over! Press R to Restart', True, (255, 255, 0))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
