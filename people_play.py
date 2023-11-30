import pygame
import home_game

def main():
    pygame.init()

    screen = pygame.display.set_mode((1050, 700))
    pygame.display.set_caption("Mê cung ngẫu nhiên")

    BLACK = (68, 79, 85)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (51,153,255)
    BLUE = (0, 0, 255)

    font = pygame.font.Font(None, 36)

    def load_image(filename,CELL_SIZE_w,CELL_SIZE_h):
        image = pygame.image.load(filename)
        return_image = pygame.transform.scale(image, (CELL_SIZE_w,CELL_SIZE_h))
        return return_image
 
    def load_maze_from_file(filename):
        with open(filename, 'r') as file:
            maze = []
            for line in file:
                maze.append(list(line.strip()))
            for y in range(len(maze)):
                for x in range(len(maze[y])):
                    if maze[y][x] == 'x':
                        start_col = x
                        start_row = y
                    elif maze[y][x] == 'y':
                        end_col = x
                        end_row = y
        CELL_SIZE_w = 800//len(maze[0])
        CELL_SIZE_h = 600//len(maze)

        WIDTH = len(maze[0])*CELL_SIZE_w
        HEIGHT = len(maze)*CELL_SIZE_h
        return maze, (start_row,start_col), (end_row,end_col), CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT

    # Vẽ mê cung trong Pygame
    def draw_maze_pp(Surface, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position):
        Surface.blit(background1_image,(0,0))
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == '#':
                    Surface.blit(border_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                elif maze[y][x] == '1':
                    Surface.blit(wall_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                elif maze[y][x] == 'y':
                    Surface.blit(end_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                if [y, x] == current_position:
                    Surface.blit(start_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
        screen.blit(Surface,(50,75))
                    
    def draw_button(x, y, width, height, text, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += 850
        pygame.draw.rect(button_surface, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        button_surface.blit(text_surface, text_rect)
        return button_rect_copy
    
    def draw_level(x, y, width, height, text, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += 0
        pygame.draw.rect(button_level, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        button_level.blit(text_surface, text_rect)
        return button_rect_copy
    
    def draw_round(x, y, width, height, text, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += 290
        button_rect_copy.y += 8
        pygame.draw.rect(button_round, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        button_round.blit(text_surface, text_rect)
        return button_rect_copy
    
    def draw_next_round(x, y, width, height, text, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += 850
        button_rect_copy.y += 610
        pygame.draw.rect(button_next_round, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        button_next_round.blit(text_surface, text_rect)
        return button_rect_copy

    def draw_option_buttons(x, y, option_texts):
        option_buttons = []
        button_height = 50
        for i, text in enumerate(option_texts):
            button = draw_button(x, y + i * button_height, 150, 50, text, WHITE, BLACK)
            option_buttons.append(button)
        return option_buttons
        
    def draw_time(surface,x,y):
        surface.fill(BLACK)       
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = int((elapsed_time / 1000) % 60)
        milliseconds = int((elapsed_time % 1000) / 10)  
        time_str = f"Time: {seconds:02d}.{milliseconds:02d}"
        text_surface = font.render(time_str, True, WHITE)
        surface.blit(text_surface, (20,15))
        screen.blit(surface, (x,y))
        

    def draw_header(text_level, text_round):
        draw_level(0, 0, 200, 60, text_level, WHITE, RED)
        draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
        draw_round(80, 0, 200, 60, text_round, WHITE, RED)
        draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
        screen.blit(button_level, (50, 8))
        screen.blit(button_round, (290, 8))

    
    def draw_count(count):
        surface_count.fill(BLACK)
        str_count = f"Count: {count}"
        text = font.render(str_count, True, WHITE)
        surface_count.blit(text,(20,17))
        screen.blit(surface_count, (675,8))


    current_round = 1
    level = 1
    text_round = "Round: " + str(current_round)  
    text_level = "Level: Easy"
    count = 0

    end_game = False
    start_time = pygame.time.get_ticks()
    running = True
    keydown = False

    maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file('Level11.txt')
    maze1, start1, end1 = maze, start, end
    current_position = list(start)

    surface_maze = pygame.Surface((WIDTH, HEIGHT))
    button_surface = pygame.Surface((200, 400))
    button_surface.fill(WHITE)
    surface_time = pygame.Surface((175,50))
    surface_count = pygame.Surface((150,60))
    button_level = pygame.Surface((200,60))
    button_round = pygame.Surface((360,60))
    button_next_round = pygame.Surface((150, 60))
    
    return_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    return_image.fill(BLUE)
    visited_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    visited_image.fill(GREEN)
    path_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    path_image.fill(WHITE) 
    wall_image = load_image('wall.jpg',CELL_SIZE_w, CELL_SIZE_h)
    start_image = load_image('ghost1.png',CELL_SIZE_w, CELL_SIZE_h)
    end_image = load_image('door.png',CELL_SIZE_w, CELL_SIZE_h)
    border_image = load_image('wall_zalo.jpg',CELL_SIZE_w, CELL_SIZE_h)
    background_image = load_image('background.jpg', 1400, 700)
    background1_image = load_image('background1.jpg', WIDTH, HEIGHT)
    screen.blit(background_image,(0,0))

    button_rs = draw_button(0, 75, 150, 50, "Reset", WHITE, RED)
    button_exit = draw_button(0, 10, 150, 50, "Exit", WHITE, GREEN)
    button_easy = draw_button(15, 150, 125, 50, "Easy", WHITE, BLACK)
    button_medium = draw_button(15, 225, 125, 50, "Medium", WHITE, BLACK)
    button_hard = draw_button(15, 300, 125, 50, "Hard", WHITE, BLACK)
    button_pre = draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
    button_next = draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
    screen.blit(button_surface,(850,0))

    def draw_button_():
        draw_button(0, 75, 150, 50, "Reset", WHITE, RED)
        draw_button(0, 10, 150, 50, "Exit", WHITE, GREEN)
        draw_button(15, 150, 125, 50, "Easy", WHITE, BLACK)
        draw_button(15, 225, 125, 50, "Medium", WHITE, BLACK)
        draw_button(15, 300, 125, 50, "Hard", WHITE, BLACK)
        screen.blit(button_surface,(850,0))
    #
    surface_maze.blit(background1_image,(0,0))
    draw_maze_pp(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
    # 

    def load_maze(level, return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position):
        screen.fill(WHITE)
        screen.blit(background_image,(0,0))
        maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file(level)
        current_position = list(start)
        surface_maze = pygame.Surface((WIDTH, HEIGHT))
        surface_maze.blit(background1_image,(0,0))
        draw_maze_pp(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
        return surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position
    
    draw_header(text_level,text_round)
    draw_count(count)
    while running:
        if keydown == True:
            draw_time(surface_time,850,400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                new_row, new_col = current_position
                if event.key == pygame.K_LEFT:
                    new_col -= 1 
                elif event.key == pygame.K_RIGHT:
                    new_col += 1
                elif event.key == pygame.K_UP:
                    new_row -= 1 
                elif event.key == pygame.K_DOWN:
                    new_row += 1
                if 1 <= new_row < len(maze) - 1 and 1 <= new_col < len(maze[0]) - 1 and (maze[new_row][new_col] == '0' or maze[new_row][new_col] == 'x' or maze[new_row][new_col] == 'y'):
                    if [new_row, new_col] != current_position:
                        current_position = [new_row, new_col]
                        count += 1
                        draw_count(count)
                        if keydown == False:
                            start_time = pygame.time.get_ticks()
                            keydown = True                        
                if current_position == list(end):
                    print("Chiến thắng!")
                    keydown = False
                    end_game = True
            if end_game == True :
                button_next_round_screen = draw_next_round(0, 0, 150, 60, "Next round", WHITE, GREEN)
                screen.blit(button_next_round, (860, 610))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                    if button_next_round_screen.collidepoint(mouse_pos):
                        current_round = current_round + 1
                        text_round = "Round: " + str(current_round)
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position)
                        maze1, start1, end1 = maze, start, end
                        count = 0 
                        draw_count(count)
                        draw_header(text_level, text_round)
                        draw_button_()
                        end_game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_pos = pygame.mouse.get_pos()
                    if button_exit.collidepoint(mouse_pos):
                        home_game.home_screen()
                    if button_easy.collidepoint(mouse_pos):
                        text_level = "Level: Easy"
                        screen.blit(background_image,(0,0))
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level11.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position)
                        maze1, start1, end1 = maze, start, end
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        draw_header(text_level, text_round)
                        count = 0 
                        draw_count(count)
                        draw_header(text_level, text_round)
                        draw_button_()
                        level = 1
                        end_game = False
                    if button_medium.collidepoint(mouse_pos):
                        text_level = "Level: Medium"
                        screen.blit(background_image,(0,0))
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level21.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image,current_position)
                        maze1, start1, end1 = maze, start, end
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        count = 0 
                        draw_count(count)
                        draw_header(text_level, text_round)
                        draw_button_()
                        level = 2
                        end_game = False
                    if button_hard.collidepoint(mouse_pos):
                        text_level = "Level: Hard"
                        screen.blit(background_image,(0,0))
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level31.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position)
                        maze1, start1, end1 = maze, start, end
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        draw_header(text_level, text_round)
                        draw_button_()
                        draw_count(count)
                        level = 3
                        end_game = False
                    if button_rs.collidepoint(mouse_pos):
                        maze, end , start = maze1, end1 , start1
                        current_position = list(start)
                        screen.blit(background_image,(0,0))
                        draw_maze_pp(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image,current_position)
                        draw_header(text_level, text_round)
                        count = 0 
                        draw_count(count)
                        draw_button_()
                        end_game = False
                    if button_pre.collidepoint(mouse_pos):
                        if current_round > 1:
                            current_round = current_round - 1
                        else:
                            print("Đây là round đầu tiên ")
                        text_round = "Round: " + str(current_round)
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position )
                        maze1, start1, end1 = maze, start, end 
                        count = 0 
                        draw_count(count)
                        draw_header(text_level, text_round)
                        draw_button_()
                        end_game = False
                    if button_next.collidepoint(mouse_pos):
                        if(current_round < 9 ):
                            current_round = current_round + 1
                        else:
                            print("Đây là round cuối cùng")
                        text_round = "Round: " + str(current_round)  
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position  = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image, current_position )
                        maze1, start1, end1 = maze, start, end
                        draw_header(text_level, text_round)
                        count = 0 
                        draw_count(count)
                        draw_button_()
                        end_game = False
        draw_maze_pp(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)            
        pygame.display.update()
    pygame.quit()