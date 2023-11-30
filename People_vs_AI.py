import pygame
import time
import algo as algomaze
import home_game

def main():
    pygame.init()

    screen = pygame.display.set_mode((1500, 800))
    pygame.display.set_caption("Mê cung ngẫu nhiên")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
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
        CELL_SIZE_w = 750//len(maze[0])
        CELL_SIZE_h = 600//len(maze)

        WIDTH = len(maze[0])*CELL_SIZE_w
        HEIGHT = len(maze)*CELL_SIZE_h
        return maze, (start_row,start_col), (end_row,end_col), CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT

    def draw_maze_ai(Surface, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image):
        Surface.blit(background1_image,(0,0))
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == '#':
                    Surface.blit(border_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                elif maze[y][x] == 'x':
                    Surface.blit(start_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                elif maze[y][x] == '1':
                    Surface.blit(wall_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                elif maze[y][x] == 'y':
                    Surface.blit(end_image, (x * CELL_SIZE_w, y * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
        screen.blit(Surface,(750,75))


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
        screen.blit(Surface,(25,75))

    def draw_solve(surface, path, visited, CELL_SIZE_w, CELL_SIZE_h,speed):
        for row, col in visited:
            if(row, col) == start or (row, col) == end:
                continue
            surface.blit(visited_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
            time.sleep(1/(20*speed))
            screen.blit(surface_ai, (750,75))
            pygame.display.update()
            draw_time(surface_time_ai,775,700)
        if path:
            print(path)
            for row, col in path:
                if(row, col) == start or (row, col) == end:
                    continue
                surface.blit(return_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                time.sleep(2/(20*speed))
                screen.blit(surface, (750,75))
                pygame.display.update() 
                draw_time(surface_time_ai,775,700)
            previous_r, previous_c = start  
            for row, col in path:
                if(row, col) == start:
                    continue
                surface.blit(path_image, (previous_c * CELL_SIZE_w, previous_r * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))           
                surface.blit(start_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                previous_r, previous_c = row, col
                time.sleep(2/(20*speed))
                screen.blit(surface, (750,75))
                draw_time(surface_time_ai,775,700)
                pygame.display.update()
        else:
            print("Can't Solve")      

    start_time = pygame.time.get_ticks()
    running = True
    keydown = False

    maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file('Level11.txt')
    maze_people = maze_ai = maze 
    current_position = list(start)

    wall_image = load_image('wall.jpg',CELL_SIZE_w, CELL_SIZE_h)
    start_image = load_image('ghost1.png',CELL_SIZE_w, CELL_SIZE_h)
    path_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    path_image.fill(WHITE) 
    end_image = load_image('door.png',CELL_SIZE_w, CELL_SIZE_h)
    border_image = load_image('wall_zalo.jpg',CELL_SIZE_w, CELL_SIZE_h)
    background_image = load_image('background.jpg', 1800, 900)
    background1_image = load_image('background1.jpg', WIDTH, HEIGHT)
    screen.blit(background_image,(0,0))

    def draw_level(x, y, width, height, text, text_color, button_color):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += 50
        button_rect_copy.y += 8
        pygame.draw.rect(surface_level, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface_level.blit(text_surface, text_rect)
        return button_rect_copy

    def draw_header(text_level, text_round):
        draw_level(0, 0, 200, 60, f"Level: {text_level}", WHITE, RED)
        draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
        draw_round(80, 0, 200, 60, text_round, WHITE, RED)
        draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
        screen.blit(surface_level, (50, 8))
        screen.blit(button_round, (290, 8))

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

    def load_maze(level, return_image, visited_image, wall_image, start_image, end_image, border_image, background_image,current_position):
        screen.fill(WHITE)
        screen.blit(background_image,(0,0))
        maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file(level)
        current_position = list(start)
        surface_people = pygame.Surface((WIDTH, HEIGHT))
        surface_ai = pygame.Surface((WIDTH, HEIGHT))
        surface_ai.blit(background1_image,(0,0))
        surface_people.blit(background1_image,(0,0))
        draw_maze_pp(surface_people, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
        draw_maze_ai(surface_ai, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)
        return surface_people,surface_ai, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position

    path = visited = []
    surface_level = pygame.Surface((200,60))
    button_round = pygame.Surface((360,60))
    surface_people = pygame.Surface((WIDTH, HEIGHT))
    surface_ai = pygame.Surface((WIDTH, HEIGHT))
    surface_time_pp = pygame.Surface((175,50))
    surface_time_ai = pygame.Surface((175,50))
    button_surface = pygame.Surface((800,60))
    button_surface.fill(WHITE)
    screen.blit(button_surface,(750,0))

    return_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    return_image.fill(BLUE)
    visited_image = pygame.Surface((CELL_SIZE_w, CELL_SIZE_h))
    visited_image.fill(GREEN)


    draw_maze_pp(surface_people, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
    draw_maze_ai(surface_ai, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)

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

    def draw_button(surface,x, y, width, height, text, text_color, button_color, x_plus, y_plus):
        button_rect = pygame.Rect(x, y, width, height)
        button_rect_copy = button_rect.copy()
        button_rect_copy.x += x_plus
        button_rect_copy.y += y_plus
        pygame.draw.rect(surface, button_color, button_rect)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)
        return button_rect_copy

    surface_algo = pygame.Surface((150,50))

    def draw_algo(text):
        surface_algo.fill(WHITE)
        draw_button(surface_algo,0,0,150,50,text,WHITE,BLACK,1200,700)
        screen.blit(surface_algo,(1200,700))

    def draw_button_():
        draw_button(button_surface,375,15,150,50,'Solve',WHITE,BLACK,750,0)
        draw_button(button_surface,25,15,150,50,'Reset',WHITE,BLACK,750,0)
        draw_button(button_surface,200,15,150,50,f'Speed: x{speed}',WHITE,BLACK,750,0)
        draw_button(button_surface,550,15,150,50,'Exit',WHITE,BLACK,750,0)
        screen.blit(button_surface,(750,0))


    speed = 1 
    text_level = "Easy"

    button_solve = draw_button(button_surface,375,15,150,50,'Solve',WHITE,BLACK,750,0)
    button_rs = draw_button(button_surface,25,15,150,50,'Reset',WHITE,BLACK,750,0)
    button_speed = draw_button(button_surface,200,15,150,50,f'Speed: x{speed}',WHITE,BLACK,750,0)
    button_exit = draw_button(button_surface,550,15,150,50,'Exit',WHITE,BLACK,750,0)
    button_algo = draw_button(surface_algo,0,0,150,50,'Algo',WHITE,BLACK,1200,700)

    button_level = draw_level(0, 0, 200, 60, f'Level:{text_level}', WHITE, RED)
    button_pre = draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
    button_next = draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
    screen.blit(surface_algo,(1200,700))
    screen.blit(button_surface,(750,0))

    text = "Algo"
    current_round = 1
    level = 1
    text_round = "Round: " + str(current_round)  

    path = visited = []
    draw_header(text_level,text_round)

    while running:
        if keydown == True:
            draw_time(surface_time_pp,25,700)
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
                if 1 <= new_row < len(maze) - 1 and 1 <= new_col < len(maze[0]) - 1 and (maze_people[new_row][new_col] == '0' or maze_people[new_row][new_col] == 'x' or maze_people[new_row][new_col] == 'y'):
                    if [new_row, new_col] != current_position:
                        current_position = [new_row, new_col]
                        if keydown == False:
                            start_time = pygame.time.get_ticks()
                            keydown = True    
                if current_position == list(end):
                    print("Chiến thắng!")
                    keydown = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_pos = pygame.mouse.get_pos()
                    if button_solve.collidepoint(mouse_pos):
                        start_time = pygame.time.get_ticks()
                        draw_solve(surface_ai, path, visited, CELL_SIZE_w, CELL_SIZE_h,speed)
                    if button_exit.collidepoint(mouse_pos):
                        home_game.home_screen()
                    if button_speed.collidepoint(mouse_pos):
                        if speed == 1:
                            speed = 2
                        elif speed == 2:
                            speed = 3
                        elif speed == 3:
                            speed = 1
                        draw_button_()
                    if button_rs.collidepoint(mouse_pos):
                        print('rs')
                        keydown = False
                        path = visited = []
                        current_position = list(start)
                        screen.blit(background_image,(0,0))
                        draw_button_()
                        draw_maze_pp(surface_people, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
                        draw_maze_ai(surface_ai, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)
                        draw_header(text_level, text_round)
                        text = "Algo"
                        draw_algo(text)
                    if button_pre.collidepoint(mouse_pos):
                        if current_round > 1:
                            current_round = current_round - 1
                        else:
                            print("Đây là round đầu tiên ")
                        text_round = "Round: " + str(current_round)
                        surface_people, surface_ai, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, wall_image, start_image, end_image, border_image, background_image, current_position)
                        maze_people = maze_ai = maze 
                        draw_header(text_level, text_round)
                        draw_button_()
                        text = "Algo"
                        draw_algo(text)
                    if button_next.collidepoint(mouse_pos):
                        if(current_round < 9 ):
                            current_round = current_round + 1
                        else:
                            print("Đây là round cuối cùng")
                        text_round = "Round: " + str(current_round)  
                        surface_people, surface_ai, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, wall_image, start_image, end_image, border_image, background_image,current_position)
                        maze_people = maze_ai = maze
                        draw_header(text_level, text_round)
                        draw_button_()
                        text = "Algo"
                        draw_algo(text)
                    if button_level.collidepoint(mouse_pos):
                        if text_level == 'Easy':
                            text_level = 'Medium'
                            level = 2 
                            current_round = 1
                        elif text_level == 'Medium':
                            text_level = 'Hard'
                            level = 3 
                            current_round = 1
                        elif text_level == 'Hard':
                            text_level = 'Easy'
                            level = 1 
                            current_round = 1
                        text_round = "Round: " + str(current_round)
                        surface_people, surface_ai, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT, current_position = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, wall_image, start_image, end_image, border_image, background_image, current_position)
                        maze_people = maze_ai = maze 
                        draw_header(text_level, text_round)
                        draw_button_()
                        text = "Algo"
                        draw_algo(text)
                    if button_algo.collidepoint(mouse_pos):
                        if text == "Algo":
                            path, visited =  algomaze.bfs_search(maze_ai,start,end)   
                            text = 'BFS'
                            draw_algo(text)
                        elif text == "BFS":
                            path, visited = algomaze.dfs_search(maze_ai,start,end)                  
                            text = "DFS"
                            draw_algo(text)
                        elif text == "DFS":
                            path, visited = algomaze.ucs_search(maze_ai,start,end)                 
                            text = "UCS"
                            draw_algo(text)
                        elif text == "UCS":
                            path, visited = algomaze.a_star_search(maze_ai,start,end)                  
                            text = "A*"
                            draw_algo(text)
                        elif text == "A*":
                            path, visited = algomaze.gbfs_search(maze_ai,start,end)                  
                            text = "GBFS"
                            draw_algo(text)
                        elif text == "GBFS":
                            path, visited = algomaze.greedy_search(maze_ai,start,end)                  
                            text = "Greedy"
                            draw_algo(text)
                        elif text == "Greedy":
                            path, visited = algomaze.ids_search(maze_ai,start,end, 100)                  
                            text = "IDS"
                            draw_algo(text)
                        elif text == "IDS":
                            path = visited = []
                            text = 'Algo'
                            draw_algo(text)

        draw_maze_pp(surface_people, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image, current_position)
        pygame.display.update()
    pygame.quit()