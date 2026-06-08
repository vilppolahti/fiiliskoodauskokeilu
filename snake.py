# Simple Snake Game
# Why pygame? It provides the necessary primitives for 2D games (rendering, input, timing) without excessive complexity
# Why a class-based structure? Encapsulation keeps game state and logic organized, making it easier to extend

import pygame
import random
import sys

class Snake:
    # Why start with 3 segments? A single segment snake would be invisible until it moves, 3 provides immediate visual feedback
    def __init__(self):
        self.positions = [(100, 100), (80, 100), (60, 100)]
        self.direction = (20, 0)  # Why start moving right? Arbitrary but consistent; avoids edge cases of starting stationary
        self.length = 3
        self.score = 0

    # Why check for self-collision? Without this, snake could reverse direction and collide with itself
    def get_head_position(self):
        return self.positions[0]

    # Why update positions by inserting at head and removing from tail? This creates the movement illusion efficiently
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % 800, (head[1] + y) % 800)  # Why modulo? Wrap around screen edges for continuous gameplay
        
        # Why check if new head collides with body? Prevents snake from moving into itself
        if new_head in self.positions[1:]:
            return False  # Game over
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    # Why increment length instead of appending directly? Allows score-based growth without immediate visual change
    def grow(self):
        self.length += 1
        self.score += 10  # Why +10? Standard scoring increment for snake games

    # Why change direction based on input? Direct control mapping to user expectations
    def change_direction(self, new_direction):
        # Why prevent 180-degree turns? Would cause immediate self-collision
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    # Why render as rectangles? Simple primitive that clearly represents each segment
    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(p[0], p[1], 20, 20))

class Food:
    # Why random position? Ensures unpredictability and replayability
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    # Why randomize within grid? Aligns with snake movement grid (multiples of 20)
    def randomize_position(self):
        self.position = (random.randint(0, 39) * 20, random.randint(0, 39) * 20)

    # Why draw as a rectangle? Distinct visual from snake segments, universally recognizable as food
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 20, 20))

def main():
    # Why 800x800? Square aspect ratio works well for grid-based games, large enough to be visible
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    font = pygame.font.SysFont('Arial', 25)  # Why Arial? Widely available default font

    # Why 10 FPS? Balances playability with visibility; snake moves at observable speed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Why key down events? Immediate response to player input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -20))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 20))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-20, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((20, 0))

        # Why update before checking collision? Ensures snake moves before checking if it hit food
        if not snake.update():
            break

        # Why check head position against food? Simple collision detection for grid-aligned objects
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            # Why ensure food doesn't spawn on snake? Prevents impossible situations
            while food.position in snake.positions:
                food.randomize_position()

        screen.fill((0, 0, 0))  # Why black background? High contrast with snake and food colors
        snake.draw(screen)
        food.draw(screen)

        # Why display score? Provides feedback and goal tracking for the player
        score_text = font.render(f'Score: {snake.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main()
