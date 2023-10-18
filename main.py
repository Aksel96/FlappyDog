import pygame, sys, time, random
from pygame.locals import *

pygame.init()
width = 500
height = 700
play_surface = pygame.display.set_mode((width, height))
bg_image = pygame.image.load("back.png").convert()
bird_image = pygame.image.load("bird.png").convert_alpha()
top_pipe = pygame.image.load("pipe_top.png").convert_alpha()
bot_pipe = pygame.image.load("pipe_bot.png").convert_alpha()
game_active = True
fps = pygame.time.Clock()


def pipe_random_heigth():
    pipe_h = [random.randint(200, int((height / 2) - 20)), random.randint(int((height / 2) + 20), height - 200)]
    return pipe_h


def display_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Chetos: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topleft=(10, 10))
    play_surface.blit(score_text, score_rect)


def game_over(score=None):
    global game_active
    game_active = False
    while not game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
        # pantalla negra
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 1))
        play_surface.blit(overlay, (0, 0))

        # Mensaje game over
        if score >= 10:
            # Mostrar "Felicidades, has ganado"
            font = pygame.font.Font(None, 36)
            text = font.render("Violetilla logro escapar con los chetos!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 4))
        else:
            # Mostrar el mensaje de "Game Over"
            font = pygame.font.Font(None, 36)
            text = font.render("No puede ser, cacharon a Violeta...", True, (255, 255, 255))
            text_rect = text.get_rect(center=(width // 2, height // 4))

        font = pygame.font.Font(None, 36)
        #text = font.render("GAME OVER", True, (255, 255, 255))
        text_score = font.render(f"Se robo \" {score} \" cheetos!", True, (255, 255, 255))
        text_info = font.render("Presiona \" ENTER \" para reiniciar", True, (255, 255, 255))
        #text_rect = text.get_rect(center=(width // 2, height // 4))
        text_rect_score = text_score.get_rect(center=(width // 2, height // 3))
        text_rect_info = text_info.get_rect(center=(width // 2, height // 2))
        play_surface.blit(text, text_rect)
        play_surface.blit(text_score, text_rect_score)
        play_surface.blit(text_info, text_rect_info)

        pygame.display.flip()


def main():
    global game_active
    game_active = True  # Iniciar el juego
    POS_X = 100
    POS_Y = 350
    acceleration = 0.98
    player_pos = [POS_X, POS_Y]
    gravity = 1
    speed = 0
    jump = -14
    score = 0
    # pipes
    pipe_pos = 700
    pipe_widht = 50
    pipe_heigth = pipe_random_heigth()

    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed = 0  # Ponemos la velocidad en 0 para que el momentum sea mas uniforme
                    speed += jump

        speed += gravity
        speed *= acceleration
        player_pos[1] += speed

        # Move pipes
        if pipe_pos >= -20:
            pipe_pos -= 10
        else:
            pipe_pos = 700
            pipe_heigth = pipe_random_heigth()
            score += 1

        # background

        play_surface.blit(bg_image, [0, 0])

        # Pipe drawing
        play_surface.blit(top_pipe, (pipe_pos, -pipe_heigth[0]))
        play_surface.blit(bot_pipe, (pipe_pos, pipe_heigth[1]))

        # player
        play_surface.blit(bird_image, (int(player_pos[0]), int(player_pos[1])))

        # Collisions
        if player_pos[1] <= (-pipe_heigth[0] + 450) or player_pos[1] >= pipe_heigth[1]:
            if player_pos[0] in list(range(pipe_pos, pipe_pos + pipe_widht)):
                print(f"Gameover score {score}")
                game_over(score)

        # Map Limits
        if player_pos[1] >= height:
            player_pos[1] = height
            speed = 0
        elif player_pos[1] <= 0:
            player_pos[1] = 0
            speed = 0

        display_score(score)
        pygame.display.flip()
        fps.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()
