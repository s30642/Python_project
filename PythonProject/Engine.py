import pygame
import sys

#configuration ------------------------
CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5

#colors ------------------------------
BLACK = (0, 0, 0)
GRAY = (80, 80, 80)
DULLGRAY = (60, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


#logic --------------------------------
def create_grid():
    return [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(screen, grid, chosen_color, active):
    if active: screen.fill(BLACK)
    else: screen.fill(DULLGRAY)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x]:
                pygame.draw.rect(screen, chosen_color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

def count_neighbors(grid, x, y):
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                count += grid[ny][nx]
    return count

def next_generation(grid):
    new_grid = create_grid()
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, x, y)
            if grid[y][x]:
                new_grid[y][x] = neighbors in [2, 3]
            else:
                new_grid[y][x] = neighbors == 3
    return new_grid

def draw_menu(screen, font):
    screen.fill(WHITE)
    title_text = font.render("Conway's Game of Life", True, BLACK)
    play_text = font.render("Play", True, WHITE)
    button_start = pygame.Rect((SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 150), (120, 40))


    img = pygame.image.load("Images/INSTRUCTIONS.jpg")
    img = pygame.transform.scale(img, (SCREEN_WIDTH // 1.2, SCREEN_HEIGHT // 3))
    screen.blit(img, (SCREEN_WIDTH // 2 -img.get_width() // 2, SCREEN_HEIGHT // 2-img.get_height() // 2 + 200))

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

    pygame.draw.rect(screen, BLACK, button_start)
    screen.blit(play_text, (button_start.centerx - play_text.get_width() // 2, button_start.centery - play_text.get_height() // 2 ))

    button_yellow = pygame.Rect((SCREEN_WIDTH // 2 - 25 - 150, SCREEN_HEIGHT // 2), (50, 50))
    pygame.draw.rect(screen, YELLOW, button_yellow)

    button_red = pygame.Rect((SCREEN_WIDTH // 2 - 25 - 50, SCREEN_HEIGHT // 2), (50, 50))
    pygame.draw.rect(screen, RED, button_red)

    button_blue = pygame.Rect((SCREEN_WIDTH // 2 - 25 + 50, SCREEN_HEIGHT // 2), (50, 50))
    pygame.draw.rect(screen, BLUE, button_blue)

    button_green = pygame.Rect((SCREEN_WIDTH // 2 - 25 + 150, SCREEN_HEIGHT // 2), (50, 50))
    pygame.draw.rect(screen, GREEN, button_green)

    return button_start, button_yellow, button_red, button_blue, button_green


#main loop ---------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    grid = create_grid()
    simulation_running = False
    game_started = False
    CHOSEN_COLOR = YELLOW
    while True:
        if not game_started:
            play_button, yellow_button, red_button, blue_button, green_button = draw_menu(screen, font)
            if CHOSEN_COLOR == YELLOW: highlight_pos = -150
            if CHOSEN_COLOR == RED: highlight_pos = -50
            if CHOSEN_COLOR == BLUE: highlight_pos = 50
            if CHOSEN_COLOR == GREEN: highlight_pos = 150
            highlight = pygame.Rect((SCREEN_WIDTH // 2 - 10 + highlight_pos, SCREEN_HEIGHT // 2 + 15), (20, 20))
            pygame.draw.rect(screen, BLACK, highlight)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        game_started = True
                    if yellow_button.collidepoint(event.pos):
                        CHOSEN_COLOR = YELLOW
                    if red_button.collidepoint(event.pos):
                        CHOSEN_COLOR = RED
                    if blue_button.collidepoint(event.pos):
                        CHOSEN_COLOR = BLUE
                    if green_button.collidepoint(event.pos):
                        CHOSEN_COLOR = GREEN

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        simulation_running = not simulation_running
                    elif event.key == pygame.K_c:
                        grid = create_grid()
                        simulation_running = False
                    if event.key == pygame.K_x:
                        grid = next_generation(grid)
                elif pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    grid[y // CELL_SIZE][x // CELL_SIZE] = not grid[y // CELL_SIZE][x // CELL_SIZE]

            if simulation_running:
                grid = next_generation(grid)

            draw_grid(screen, grid, CHOSEN_COLOR, simulation_running)
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    main()
