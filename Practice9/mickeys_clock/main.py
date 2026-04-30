import pygame
import os
import sys
from clock import get_angles

pygame.init()
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

base = os.path.join(os.path.dirname(__file__), 'images')

image_surface = pygame.image.load(os.path.join(base, 'clock.png')).convert_alpha()
mickey        = pygame.image.load(os.path.join(base, 'mUmrP.png')).convert_alpha()
hand_l        = pygame.image.load(os.path.join(base, 'hand_left_centered.png')).convert_alpha()
hand_r        = pygame.image.load(os.path.join(base, 'hand_right_centered.png')).convert_alpha()

resized_image = pygame.transform.scale(image_surface, (800, 600))
res_mickey    = pygame.transform.scale(mickey, (350, 350))
hand_l_base   = pygame.transform.scale(hand_l, (151, 300))
hand_r_base   = pygame.transform.scale(hand_r, (151, 300))

CLOCK_CENTER = (300, 180)
HAND_CENTER  = (600, 320)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    minutes_angle, hours_angle = get_angles()

    rotated_minutes = pygame.transform.rotate(hand_l_base, minutes_angle)
    rotated_hours   = pygame.transform.rotate(hand_r_base, hours_angle)

    minutes_rect = rotated_minutes.get_rect(center=HAND_CENTER)
    hours_rect   = rotated_hours.get_rect(center=HAND_CENTER)

    screen.fill((255, 255, 255))

    image_rect = resized_image.get_rect(center=(600, 340))
    screen.blit(resized_image, image_rect)

    mic_rect = res_mickey.get_rect(center=(600 , 320))
    screen.blit(res_mickey, mic_rect)

    screen.blit(rotated_hours, hours_rect)
    screen.blit(rotated_minutes, minutes_rect)

    pygame.display.flip()
    clock.tick(60)