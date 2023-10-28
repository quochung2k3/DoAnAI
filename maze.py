import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH + 400, HEIGHT))
pygame.display.set_caption("Mê cung ngẫu nhiên")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

CELL_SIZE = 25
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

def create_random_maze():
    maze = [[1] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

    def is_valid(cell):
        row, col = cell
        return 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH

    def recursive_backtracking(row, col):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if is_valid((r, c)) and maze[r][c] == 1:
                maze[r][c] = 0
                maze[row + dr // 2][col + dc // 2] = 0
                recursive_backtracking(r, c)

    start_row = random.randint(0, GRID_HEIGHT // 2) * 2
    start_col = random.randint(0, GRID_WIDTH // 2) * 2
    if is_valid((start_row, start_col)):
        maze[start_row][start_col] = 0
        recursive_backtracking(start_row, start_col)

    end_row = random.randint(0, GRID_HEIGHT - 1)
    end_col = random.randint(0, GRID_WIDTH - 1)
    if is_valid((end_row, end_col)):
        maze[end_row][end_col] = 0

    return maze, (start_row, start_col), (end_row, end_col)


maze, start, end = create_random_maze()

current_position = list(start)

def draw_maze(maze, current_position, end):
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (current_position[1] * CELL_SIZE, current_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_border():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 1)
    
def draw_button():
    pygame.draw.rect(screen, BLACK, (620, 0, 100, 70))
    font = pygame.font.Font(None, 48)
    text = font.render("Reset", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (100, 535)
    screen.blit(text, text_rect)

game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_row, new_col = current_position
            if event.key == pygame.K_LEFT:
                new_col -= 1
            elif event.key == pygame.K_RIGHT:
                new_col += 1
            elif event.key == pygame.K_UP:
                new_row -= 1
            elif event.key == pygame.K_DOWN:
                new_row += 1

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                current_position = (new_row, new_col)
            
        if current_position == end:
            game_over = True
            print("Chiến thắng!")
            maze, start, end = create_random_maze()
            current_position = list(start)
            game_over = False
    
    screen.fill(WHITE)
    draw_maze(maze, current_position, end)
    draw_border()
    draw_button()
    pygame.display.flip()
pygame.quit()