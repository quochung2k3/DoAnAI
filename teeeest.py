import pygame
import time
import algo as algomaze
import home_game

def main():
    pygame.init()

    screen = pygame.display.set_mode((1300, 700))
    pygame.display.set_caption("Mê cung ngẫu nhiên")

    BLACK = (68, 79, 85)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (51,153,255)
    BLUE = (0, 0, 255)

    font = pygame.font.Font(None, 36)
    open_combobox = 0
    algo = ""
    lines = '-'*100

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
    def draw_maze(Surface, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image):
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
        screen.blit(Surface, (50,75))
                    
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
        button_rect_copy.x += 1070
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
        
    def draw_time(surface):
        surface.fill(BLACK)       
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        seconds = int((elapsed_time / 1000) % 60)
        milliseconds = int((elapsed_time % 1000) / 10)  
        time_str = f"Time: {seconds:02d}.{milliseconds:02d}"
        text_surface = font.render(time_str, True, WHITE)
        surface.blit(text_surface, (20,15))
        screen.blit(surface_time, (870,500))
        
    def draw_text_algo(text):
        button_surface.fill(WHITE)
        draw_button(20, 10, 200, 50, text, WHITE, GREEN)
        draw_button(20, 400, 125, 50, "Easy", WHITE, BLACK)
        draw_button(160, 400, 125, 50, "Medium", WHITE, BLACK)
        draw_button(300, 400, 125, 50, "Hard", WHITE, BLACK)
        draw_button(245, 240, 175, 50 ,f"Speed: x{speed}", WHITE, RED)
        button_surface.blit(reset_image,(245, 10))
        button_surface.blit(solve_image,(245, 85))
        button_surface.blit(exit_image,(245, 160))
        screen.blit(button_surface, (850,0))
        
    def draw_header(text_level, text_round):
        draw_level(0, 0, 200, 60, text_level, WHITE, RED)
        draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
        draw_round(80, 0, 200, 60, text_round, WHITE, RED)
        draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
        screen.blit(button_level, (50, 8))
        screen.blit(button_round, (290, 8))

    def draw_solve(surface, path, visited, CELL_SIZE_w, CELL_SIZE_h, speed):
        count = 0
        state = 0 
        if(level == 1):
            text_level = 'Easy'
        elif (level == 2):
            text_level = 'Medium'
        elif (level == 3):
            text_level = 'Hard'
        text = f'Algorithm: {algo}   Level: {text_level}   Round: {current_round}   Speed:x{speed}'
        write_his(lines)
        write_his(text)
        write_his(f'Step: {len(path)-1}')
        write_his(f'State: {len(visited)}')

        start_solve = pygame.time.get_ticks()
        for row, col in visited:
            state += 1
            if(row, col) == start or (row, col) == end:
                draw_state(state)
                continue
            surface.blit(visited_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
            time.sleep(1/(20*speed))
            screen.blit(surface_maze, (50,75))
            pygame.display.update()
            draw_time(surface_time)
            draw_state(state)
        if path:
            print(path)
            for row, col in path:
                count +=1
                if(row, col) == start or (row, col) == end:
                    continue
                surface.blit(return_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                time.sleep(2/(20*speed))
                screen.blit(surface_maze, (50,75))
                pygame.display.update() 
                draw_time(surface_time)
                draw_count(count)

            previous_r, previous_c = start  
            for row, col in path:
                if(row, col) == start:
                    continue
                surface.blit(path_image, (previous_c * CELL_SIZE_w, previous_r * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))           
                surface.blit(start_image, (col * CELL_SIZE_w, row * CELL_SIZE_h, CELL_SIZE_w, CELL_SIZE_h))
                previous_r, previous_c = row, col
                time.sleep(2/(20*speed))
                screen.blit(surface_maze, (50,75))
                draw_time(surface_time)
                pygame.display.update()
        else:
            print("Can't Solve")
        end_solve = pygame.time.get_ticks()
        time_sovle = end_solve - start_solve
        seconds = int((time_sovle / 1000) % 60)
        milliseconds = int((time_sovle % 1000) / 10)  
        time_str = f"Time: {seconds:02d}.{milliseconds:02d}s"
        write_his(time_str)

    def draw_count(count):
        surface_count.fill(BLACK)
        str_count = f"Count: {count}"
        text = font.render(str_count, True, WHITE)
        surface_count.blit(text,(20,17))
        screen.blit(surface_count, (675,8))

    def draw_state(state):
        surface_state.fill(BLACK)
        str_state = f"State: {state}"
        text = font.render(str_state, True, WHITE)
        surface_state.blit(text,(30,15))
        screen.blit(surface_state, (1100,500))

    current_round = 1
    level = 1
    text_round = "Round: " + str(current_round)  
    text_level = "Level: Easy"
    speed = 1 
    end_game = True
    start_time = pygame.time.get_ticks()
    running = True
    show_options = False

    maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file('Level11.txt')
    maze1, start1, end1 = maze, start, end

    surface_maze = pygame.Surface((WIDTH, HEIGHT))
    button_surface = pygame.Surface((440, 470))
    button_surface.fill(WHITE)
    surface_time = pygame.Surface((175,50))
    surface_count = pygame.Surface((150,60))
    surface_state = pygame.Surface((175,50))
    button_level = pygame.Surface((200,60))
    button_round = pygame.Surface((360,60))
    button_next_round = pygame.Surface((200, 60))

    reset_image = load_image('reset.png',175,50)
    solve_image = load_image('solve.png',175,50)
    exit_image = load_image('exit.png',175,50)
    
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

    button_rs = draw_button(245, 10, 175, 50, "Reset", WHITE, RED)
    button_sovle = draw_button(245, 85, 175, 50, "Solve", WHITE, BLUE)
    button_exit = draw_button(245, 160, 175, 50, "Exit", WHITE, GREEN)
    button_algo = draw_button(20, 10, 200, 50, "Algo", WHITE, GREEN)
    button_easy = draw_button(20, 400, 125, 50, "Easy", WHITE, BLACK)
    button_medium = draw_button(160, 400, 125, 50, "Medium", WHITE, BLACK)
    button_hard = draw_button(300, 400, 125, 50, "Hard", WHITE, BLACK)
    button_speed = draw_button(245, 240, 175, 50 ,f"Speed: x{speed}", WHITE, RED)
    #
    path = visited = []
    surface_maze.blit(background1_image,(0,0))
    draw_maze(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)
    # 

    def load_maze(level, return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image):
        screen.fill(WHITE)
        screen.blit(background_image,(0,0))
        maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze_from_file(level)
        surface_maze = pygame.Surface((WIDTH, HEIGHT))
        surface_maze.blit(background1_image,(0,0))
        draw_maze(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)
        return surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT
    
    def write_his(text):
        with open("history.txt", "a") as file:
            file.writelines(text)
            file.writelines('\n')
    


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("history.txt","w") as file:
                    file.writelines("")
                running = False
            if show_options == False:
                draw_text_algo("Algo")
                draw_level(0, 0, 200, 60, text_level, WHITE, RED)
                button_pre = draw_round(0, 0, 80, 60, "Pre", WHITE, GREEN)
                draw_round(80, 0, 200, 60, text_round, WHITE, RED)
                button_next = draw_round(280, 0, 80, 60, "Next", WHITE, GREEN)
                screen.blit(button_level, (50, 8))
                screen.blit(button_round, (290, 8))
                screen.blit(button_surface, (850,0))
                show_options = True
            if end_game == False:
                button_next_round_screen = draw_next_round(0, 0, 200, 60, "Next round", WHITE, GREEN)
                screen.blit(button_next_round, (1070, 610))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        mouse_pos = pygame.mouse.get_pos()
                    if button_next_round_screen.collidepoint(mouse_pos):
                        current_round = current_round + 1
                        text_round = "Round: " + str(current_round)
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        end_game = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouse_pos = pygame.mouse.get_pos()
                    if button_exit.collidepoint(mouse_pos):
                        home_game.home_screen()
                    if button_easy.collidepoint(mouse_pos):
                        text_level = "Level: Easy"
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level11.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end
                        print(len(maze),len(maze[0]))
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        level = 1
                        end_game = True
                    if button_medium.collidepoint(mouse_pos):
                        text_level = "Level: Medium"
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level21.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end
                        print(len(maze),len(maze[0]))
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        level = 2
                        end_game = True
                    if button_hard.collidepoint(mouse_pos):
                        text_level = "Level: Hard"
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level31.txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end
                        current_round = 1
                        text_round = "Round: " + str(current_round)
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        level = 3
                        end_game = True
                    if button_rs.collidepoint(mouse_pos):
                        path = visited = []
                        maze, end , start = maze1, end1 , start1
                        screen.blit(background_image,(0,0))
                        draw_maze(surface_maze, maze, CELL_SIZE_w, CELL_SIZE_h, border_image, wall_image, start_image, end_image)
                        draw_header(text_level, text_round)
                        draw_count(0)
                        draw_state(0)
                        draw_text_algo("Algo")
                        algo = ""
                        end_game = True
                    if button_sovle.collidepoint(mouse_pos):
                        start_time = pygame.time.get_ticks()
                        draw_solve(surface_maze,path,visited,CELL_SIZE_w,CELL_SIZE_h,speed)
                        print(algo)
                        end_game = False
                    if button_pre.collidepoint(mouse_pos):
                        if current_round > 1:
                            current_round = current_round - 1
                        else:
                            print("Đây là round đầu tiên ")
                        text_round = "Round: " + str(current_round)
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end 
                        print("level"+str(level)+str(current_round)+".txt")
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        end_game = True
                    if button_next.collidepoint(mouse_pos):
                        if(current_round < 9 ):
                            current_round = current_round + 1
                        else:
                            print("Đây là round cuối cùng")
                        text_round = "Round: " + str(current_round)  
                        surface_maze, maze, start, end, CELL_SIZE_w, CELL_SIZE_h, WIDTH, HEIGHT = load_maze("level"+str(level)+str(current_round)+".txt",return_image, visited_image, path_image, wall_image, start_image, end_image, border_image, background_image)
                        maze1, start1, end1 = maze, start, end
                        print("level"+str(level)+str(current_round)+".txt")
                        draw_header(text_level, text_round)
                        draw_text_algo("Algo")
                        end_game = True
                    if button_speed.collidepoint(mouse_pos):
                        if speed == 1:
                            speed = 2
                        elif speed == 2:
                            speed = 3
                        elif speed == 3:
                            speed = 1
                        draw_text_algo("Algo")
                    if button_algo.collidepoint(mouse_pos):
                        if open_combobox == 0:
                            button_DFS = draw_button(20, 60, 200, 45, "DFS", WHITE, BLACK)
                            button_BFS = draw_button(20, 105, 200, 45, "BFS", WHITE, BLACK)
                            button_UCS = draw_button(20, 150, 200, 45, "UCS", WHITE, BLACK)
                            button_A = draw_button(20, 195, 200, 45, "A*", WHITE, BLACK)
                            button_GBFS = draw_button(20, 240, 200, 45, "GBFS", WHITE, BLACK)
                            button_greedy = draw_button(20, 285, 200, 45, "Greedy", WHITE, BLACK)
                            button_7 = draw_button(20, 330, 200, 45, "IDS", WHITE, BLACK)
                            screen.blit(button_surface, (850, 0))
                            open_combobox = 1
                        elif open_combobox == 1:
                            open_combobox = 0
                            draw_text_algo("Algo")
                    if open_combobox == 1:
                        if button_DFS.collidepoint(mouse_pos):
                            path, visited = algomaze.dfs_search(maze,start,end)
                            draw_text_algo("DFS")
                            algo = "DFS"
                            open_combobox = 0
                        if button_BFS.collidepoint(mouse_pos):
                            path, visited = algomaze.bfs_search(maze,start,end)                            
                            draw_text_algo("BFS")
                            algo = "BFS"
                            open_combobox = 0
                        if button_UCS.collidepoint(mouse_pos):
                            path, visited = algomaze.ucs_search(maze,start,end)
                            draw_text_algo("UCS")
                            algo = "UCS"
                            open_combobox = 0
                        if button_A.collidepoint(mouse_pos):
                            path, visited = algomaze.a_star_search(maze,start,end)                           
                            draw_text_algo("A*")
                            algo = "A*"
                            open_combobox = 0
                        if button_GBFS.collidepoint(mouse_pos):
                            path, visited = algomaze.gbfs_search(maze,start,end)
                            draw_text_algo("GBFS")
                            algo = "GBFS"
                            open_combobox = 0
                        if button_greedy.collidepoint(mouse_pos):
                            path, visited = algomaze.greedy_search(maze,start,end)
                            draw_text_algo("Greedy")
                            open_combobox = 0
                        if button_7.collidepoint(mouse_pos):
                            path, visited = algomaze.ids_search(maze,start,end,100)
                            draw_text_algo("IDS")
                            open_combobox = 0
        pygame.display.update()
    pygame.quit()
main()