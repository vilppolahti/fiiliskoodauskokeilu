# Simple Tetris Game
# Why pygame? Consistent with snake.py for library uniformity across the repository
# Why class-based? Modular design allows clear separation of concerns (board, pieces, rendering)

import pygame
import random

# Why define shapes as lists of coordinates? Compact representation of tetromino patterns
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Why define colors? Visual distinction between different piece types
COLORS = [
    (0, 255, 255),  # I - Cyan
    (255, 255, 0),  # O - Yellow
    (128, 0, 128),  # T - Purple
    (255, 165, 0),  # L - Orange
    (0, 0, 255),    # J - Blue
    (0, 255, 0),    # S - Green
    (255, 0, 0)     # Z - Red
]

class Tetris:
    # Why 10x20 grid? Standard tetris dimensions that provide balanced gameplay
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.game_over = False
        self.new_piece()

    # Why random piece selection? Ensures variety and prevents predictability
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[shape_idx]
        self.current_color = COLORS[shape_idx]
        self.current_x = self.width // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        # Why check for immediate game over? Piece might spawn in invalid position
        if self.check_collision():
            self.game_over = True

    # Why check collision? Prevents pieces from moving through walls or other pieces
    def check_collision(self, offset_x=0, offset_y=0):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_x + x + offset_x
                    new_y = self.current_y + y + offset_y
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height or 
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return True
        return False

    # Why rotate piece? Core tetris mechanic that allows strategic placement
    def rotate_piece(self):
        # Why transpose and reverse? Standard 90-degree rotation for 2D arrays
        rotated = [[self.current_piece[y][x] for y in range(len(self.current_piece)-1, -1, -1)] 
                  for x in range(len(self.current_piece[0]))]
        old_piece = self.current_piece
        self.current_piece = rotated
        
        # Why revert if rotation causes collision? Maintains game validity
        if self.check_collision():
            self.current_piece = old_piece

    # Why merge piece into board? Finalizes piece placement when it can't move further
    def merge_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell and self.current_y + y >= 0:
                    self.board[self.current_y + y][self.current_x + x] = self.current_color

    # Why clear lines? Primary scoring mechanism and gameplay objective
    def clear_lines(self):
        lines_cleared = 0
        for y in range(self.height):
            if all(self.board[y]):
                lines_cleared += 1
                # Why move all lines above down? Creates space for new pieces
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2-1][:]
                self.board[0] = [0 for _ in range(self.width)]
        
        # Why score based on lines cleared? Reward for efficient piece placement
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    # Why update by moving piece down? Gravity simulation for falling pieces
    def update(self):
        if self.game_over:
            return
        
        if not self.check_collision(0, 1):
            self.current_y += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.new_piece()

    # Why move left/right? Allows horizontal positioning of pieces
    def move(self, dx):
        if not self.check_collision(dx, 0):
            self.current_x += dx

    # Why hard drop? Allows instant placement for strategic plays
    def hard_drop(self):
        while not self.check_collision(0, 1):
            self.current_y += 1
        self.update()

    # Why render as grid? Visual representation of the game state
    def draw(self, surface):
        cell_size = 30
        
        # Draw board
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x]:
                    pygame.draw.rect(surface, self.board[y][x], 
                                    pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
                    pygame.draw.rect(surface, (255, 255, 255), 
                                    pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size), 1)

        # Draw current piece
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell and self.current_y + y >= 0:
                    pygame.draw.rect(surface, self.current_color,
                                    pygame.Rect((self.current_x + x) * cell_size, 
                                               (self.current_y + y) * cell_size, 
                                               cell_size, cell_size))
                    pygame.draw.rect(surface, (255, 255, 255),
                                    pygame.Rect((self.current_x + x) * cell_size,
                                               (self.current_y + y) * cell_size,
                                               cell_size, cell_size), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 600))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 25)

    game = Tetris()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move(1)
                elif event.key == pygame.K_DOWN:
                    game.update()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()

        screen.fill((0, 0, 0))
        game.draw(screen)
        
        score_text = font.render(f'Score: {game.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(5)

    font_large = pygame.font.SysFont('Arial', 40)
    game_over_text = font_large.render('GAME OVER', True, (255, 0, 0))
    screen.blit(game_over_text, (50, 300))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == '__main__':
    main()
