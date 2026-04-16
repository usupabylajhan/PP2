import pygame
import sys
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Moving Ball")
clock = pygame.time.Clock()

ball = Ball(600, 400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -ball.step)
            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.step)
            elif event.key == pygame.K_LEFT:
                ball.move(-ball.step, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(ball.step, 0)

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.r)
    pygame.display.flip()
    clock.tick(60)