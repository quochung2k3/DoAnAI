import pygame
import sys
import AI_solve
def main():
    pygame.init()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Scrolling Text Example")

    font = pygame.font.Font(None, 36)

    def draw_text(surface, text, x, y, max_lines, current_line):
        lines = text.split('\n')

        # Hiển thị chỉ một số dòng tối đa (max_lines)
        visible_lines = lines[current_line:current_line + max_lines]

        for i, line in enumerate(visible_lines):
            text_surface = font.render(line, True, (0, 0, 0))
            surface.blit(text_surface, (x, y + i * font.get_height()))

    long_text = ""
    with open("history.txt", "r") as file:
        long_text = file.read()
    max_lines_displayed = 24
    current_line = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                AI_solve.main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Lăn lên
                    if current_line > 0:
                        current_line -= 1
                elif event.button == 5:  # Lăn xuống
                    if current_line < len(long_text.split('\n')) - max_lines_displayed:
                        current_line += 1

        # Vẽ văn bản lên màn hình
        screen.fill((255, 255, 255))
        draw_text(screen, long_text, 10, 10, max_lines_displayed, current_line)
        pygame.display.flip()

        clock.tick(30)