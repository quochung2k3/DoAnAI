import pygame.mixer
import pygame
import sys
import AI_solve
import people_play
import People_vs_AI

def home_screen():
    pygame.init()
    #Nhac nen
    pygame.mixer.init()
    background_music = pygame.mixer.Sound(r'sound\nhacnen.mp3')
    background_music.play(-1)  # Đối số -1 đảm bảo rằng âm nhạc sẽ phát lặp đi lặp lại vô hạn.
    # Tiêu đề và biểu tượng game
    pygame.display.set_caption('Maze')
    
    # Nền
    bg = pygame.image.load(r'assets\nen1.png')
    #bg = pygame.transform.scale2x(bg)
    
    # Kích thước cửa sổ game
    screen_width = 1040
    screen_height = 780
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Nút "Start" và kích thước mới
    st = pygame.image.load(r'assets\Logo1.png')
    new_st_width = 350
    new_st_height = 200
    st = pygame.transform.scale(st, (new_st_width, new_st_height))
    # Nút "Người chơi" và kích thước mới
    nc = pygame.image.load(r'assets\nguoichoi1.png')
    new_nc_width = 350
    new_nc_height = 200
    nc = pygame.transform.scale(nc, (new_nc_width, new_nc_height))
    # Nút "Máy chơi" và kích thước mới
    mc = pygame.image.load(r'assets\maychoi.png')
    new_mc_width = 350
    new_mc_height = 200
    mc = pygame.transform.scale(mc, (new_mc_width, new_mc_height))
    # Nút "Người vs máy" và kích thước mới
    nmc = pygame.image.load(r'assets\nguoivsmay.png')
    new_nmc_width = 350
    new_nmc_height = 200
    nmc = pygame.transform.scale(nmc, (new_nmc_width, new_nmc_height))
    # Nút "Exit" và kích thước mới
    ex = pygame.image.load(r'assets\thoat.png')
    new_ex_width = 350
    new_ex_height = 200
    ex = pygame.transform.scale(ex, (new_ex_width, new_ex_height))

    class Button():
        def __init__(self, x, y, image):
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.topleft = (x, y)
        def draw(self):
            screen.blit(self.image, (self.rect.x, self.rect.y))
    
    #create button instances
    start_button = Button(358, 130, st)
    nguoi_button = Button(358, 280, nc)
    may_button = Button(358, 380, mc)
    nguoivsmay_button = Button(358, 480, nmc)
    exit_button = Button(358, 580, ex)
    exit_button_clicked = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x >= 385 and mouse_x <= 680:
                    if mouse_y >= 345 and mouse_y <= 400:
                        people_play.main()
                    elif mouse_y >= 445 and mouse_y <= 500:
                        AI_solve.main()
                    elif mouse_y >= 545 and mouse_y <= 600:
                        People_vs_AI.main()
                    elif mouse_y >= 645 and mouse_y <= 700:
                        exit_button_clicked = True
        screen.blit(bg, (0, 0))
        if exit_button_clicked:
            pygame.quit()
            sys.exit()
        start_button.draw()
        exit_button.draw()
        may_button.draw()
        nguoi_button.draw()
        nguoivsmay_button.draw()
        pygame.display.update()
    pygame.quit()
