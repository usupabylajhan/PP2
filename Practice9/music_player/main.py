import pygame
import sys
from player import Player

pygame.init()
screen = pygame.display.set_mode((500, 200))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("monospace", 22)
small = pygame.font.SysFont("monospace", 16)
clock = pygame.time.Clock()

player = Player("music")

def draw(player):
    screen.fill((20, 20, 30))

    title = font.render(f"Track: {player.current_name()}", True, (200, 220, 255))
    status = font.render(f"Status: {'Playing' if player.playing else 'Stopped'}", True, (100, 255, 150) if player.playing else (255, 100, 100))
    pos = font.render(f"Position: {player.get_pos()}s", True, (180, 180, 180))
    tracks = small.render(f"Tracks: {len(player.tracks)}  |  [{player.index + 1}/{max(len(player.tracks), 1)}]", True, (120, 120, 160))
    controls = small.render("P=Play  S=Stop  N=Next  B=Prev  Q=Quit", True, (100, 100, 130))

    screen.blit(title, (20, 20))
    screen.blit(status, (20, 55))
    screen.blit(pos, (20, 90))
    screen.blit(tracks, (20, 130))
    screen.blit(controls, (20, 165))
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    draw(player)
    clock.tick(30)