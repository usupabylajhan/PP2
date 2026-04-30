import pygame
import random
import sys

pygame.init()
SCREEN_W, SCREEN_H = 400, 600
FPS = 60
ROAD_LEFT, ROAD_RIGHT = 60, 340
LANE_W = (ROAD_RIGHT - ROAD_LEFT) // 3

WHITE, BLACK, GRAY, YELLOW, GOLD, RED, BLUE, LT_BLU = (255,255,255), (0,0,0), (90,90,90), (255,215,0), (200,160,0), (210,30,30), (30,90,210), (160,210,255)
GRASS, GREEN = (45,120,45), (0,180,0)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer")
clock, font, big, small = pygame.time.Clock(), pygame.font.SysFont("Arial", 22, True), pygame.font.SysFont("Arial", 48, True), pygame.font.SysFont("Arial", 14, True)

def random_lane_x(w): return ROAD_LEFT + random.randint(0, 2) * LANE_W + (LANE_W - w) // 2

class Road:
    LINE_H, LINE_GAP, SEGMENT = 55, 35, 90
    def __init__(self): self.offset, self.speed = 0, 5
    def update(self): self.offset = (self.offset + self.speed) % self.SEGMENT
    def draw(self, surface):
        surface.fill(GRASS)
        pygame.draw.rect(surface, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))
        pygame.draw.rect(surface, WHITE, (ROAD_LEFT - 4, 0, 4, SCREEN_H))
        pygame.draw.rect(surface, WHITE, (ROAD_RIGHT, 0, 4, SCREEN_H))
        for lane in range(1, 3):
            x = ROAD_LEFT + LANE_W * lane - 2
            y = self.offset - self.SEGMENT
            while y < SCREEN_H:
                pygame.draw.rect(surface, WHITE, (x, y, 4, self.LINE_H))
                y += self.SEGMENT

class PlayerCar:
    W, H = 38, 68
    def __init__(self): self.x, self.y, self.spd = SCREEN_W//2 - self.W//2, SCREEN_H - 110, 5
    def draw(self, surface):
        x, y, w, h = self.x, self.y, self.W, self.H
        pygame.draw.rect(surface, BLUE, (x, y, w, h), border_radius=6)
        pygame.draw.rect(surface, LT_BLU, (x+5, y+8, w-10, 18))
        pygame.draw.rect(surface, LT_BLU, (x+5, y+h-22, w-10, 12))
        for wx, wy in [(x-6, y+6), (x+w-2, y+6), (x-6, y+h-22), (x+w-2, y+h-22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 14), border_radius=2)
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT: self.x -= self.spd
        if keys[pygame.K_RIGHT] and self.x + self.W < ROAD_RIGHT: self.x += self.spd
        if keys[pygame.K_UP] and self.y > 0: self.y -= self.spd
        if keys[pygame.K_DOWN] and self.y + self.H < SCREEN_H: self.y += self.spd
    def rect(self): return pygame.Rect(self.x + 4, self.y + 4, self.W - 8, self.H - 8)

class EnemyCar:
    W, H = 38, 68
    def __init__(self, speed):
        self.x, self.y, self.spd = random_lane_x(self.W), -self.H - random.randint(0, 60), speed
        self.col = random.choice([(200,40,40), (180,90,0), (140,0,140)])
    def draw(self, surface):
        x, y, w, h = self.x, self.y, self.W, self.H
        pygame.draw.rect(surface, self.col, (x, y, w, h), border_radius=6)
        pygame.draw.rect(surface, LT_BLU, (x+5, y+h-22, w-10, 12))
        for wx, wy in [(x-6, y+6), (x+w-2, y+6), (x-6, y+h-22), (x+w-2, y+h-22)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 8, 14), border_radius=2)
    def update(self): self.y += self.spd
    def off_screen(self): return self.y > SCREEN_H
    def rect(self): return pygame.Rect(self.x + 4, self.y + 4, self.W - 8, self.H - 8)

class Coin:
    R = 11
    def __init__(self, speed): self.x, self.y, self.spd = random.randint(ROAD_LEFT + self.R + 2, ROAD_RIGHT - self.R - 2), -self.R, speed
    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.R)
        pygame.draw.circle(surface, GOLD, (self.x, self.y), self.R, 2)
        lbl = small.render("$", True, GOLD)
        surface.blit(lbl, (self.x - lbl.get_width()//2, self.y - lbl.get_height()//2))
    def update(self): self.y += self.spd
    def off_screen(self): return self.y - self.R > SCREEN_H
    def rect(self): return pygame.Rect(self.x - self.R, self.y - self.R, self.R*2, self.R*2)

def draw_hud(surface, score, coins):
    s = font.render(f"Score: {score}", True, WHITE)
    c = font.render(f"Coins: {coins}", True, YELLOW)
    surface.blit(s, (10, 8))
    surface.blit(c, (SCREEN_W - c.get_width() - 10, 8))

def draw_game_over(surface, score, coins):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    lines = [(big, "GAME OVER", RED), (font, f"Score : {score}", WHITE), (font, f"Coins : {coins}", YELLOW), (font, "R – restart   Q – quit", WHITE)]
    y = 190
    for f_, text, col in lines:
        surf = f_.render(text, True, col)
        surface.blit(surf, (SCREEN_W//2 - surf.get_width()//2, y))
        y += surf.get_height() + 14

def main():
    road, player = Road(), PlayerCar()
    enemies, coins = [], []
    score, coin_count, base_speed, game_over = 0, 0, 4, False
    enemy_timer, enemy_interval, coin_timer, coin_interval = 0, 80, 0, random.randint(100, 180)
    
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r: main(); return
                if event.key == pygame.K_q: pygame.quit(); sys.exit()
        
        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)
            road.update()
            speed = base_speed + score // 5
            road.speed = 5 + score // 8
            
            enemy_timer += 1
            if enemy_timer >= enemy_interval:
                enemies.append(EnemyCar(speed))
                enemy_timer, enemy_interval = 0, random.randint(55, 110)
            
            coin_timer += 1
            if coin_timer >= coin_interval:
                coins.append(Coin(speed))
                coin_timer, coin_interval = 0, random.randint(90, 200)
            
            for en in enemies[:]:
                en.update()
                if en.off_screen(): enemies.remove(en); score += 1
                elif en.rect().colliderect(player.rect()): game_over = True
            
            for co in coins[:]:
                co.update()
                if co.off_screen(): coins.remove(co)
                elif co.rect().colliderect(player.rect()): coins.remove(co); coin_count += 1
        
        road.draw(screen)
        for en in enemies: en.draw(screen)
        for co in coins: co.draw(screen)
        player.draw(screen)
        draw_hud(screen, score, coin_count)
        if game_over: draw_game_over(screen, score, coin_count)
        pygame.display.flip()

if __name__ == "__main__":
    main()