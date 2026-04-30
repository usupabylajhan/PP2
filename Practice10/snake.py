import pygame
import random
import sys

pygame.init()
CELL, COLS, ROWS, HUD_H = 20, 30, 25, 50
SCREEN_W, SCREEN_H = CELL * COLS, CELL * ROWS + HUD_H
BASE_FPS, FPS_PER_LEVEL, FOODS_PER_LEVEL = 8, 2, 3

BLACK, WHITE, DKGREEN, GREEN, RED, YELLOW, GRAY, LT_GRAY, GOLD, BLUE = (0,0,0), (255,255,255), (0,140,0), (50,200,50), (220,40,40), (255,215,0), (30,30,30), (60,60,60), (255,200,0), (60,120,220)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake")
clock, font, big = pygame.time.Clock(), pygame.font.SysFont("Arial", 22, True), pygame.font.SysFont("Arial", 44, True)

UP, DOWN, LEFT, RIGHT = (0,-1), (0,1), (-1,0), (1,0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

def random_food(occupied):
    while True:
        c, r = random.randint(1, COLS-2), random.randint(1, ROWS-2)
        if (c, r) not in occupied: return (c, r)

class Snake:
    def __init__(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body, self.direction, self._queued, self._grow = [(cx, cy), (cx-1, cy), (cx-2, cy)], RIGHT, RIGHT, False
    def queue_direction(self, new_dir):
        if new_dir != OPPOSITE.get(self.direction): self._queued = new_dir
    def move(self):
        self.direction = self._queued
        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        self.body.insert(0, new_head)
        if self._grow: self._grow = False
        else: self.body.pop()
    def eat(self): self._grow = True
    def hit_wall(self):
        hx, hy = self.body[0]
        return not (0 <= hx < COLS and 0 <= hy < ROWS)
    def hit_self(self): return self.body[0] in self.body[1:]
    def draw(self, surface):
        for i, (c, r) in enumerate(self.body):
            x, y = c * CELL, r * CELL + HUD_H
            col = DKGREEN if i == 0 else GREEN
            pygame.draw.rect(surface, col, (x+2, y+2, CELL-4, CELL-4), border_radius=4)
            if i == 0:
                pygame.draw.circle(surface, WHITE, (x+5, y+6), 3)
                pygame.draw.circle(surface, WHITE, (x+14, y+6), 3)
                pygame.draw.circle(surface, BLACK, (x+5, y+6), 1)
                pygame.draw.circle(surface, BLACK, (x+14, y+6), 1)
    @property
    def cells(self): return set(self.body)

class Food:
    def __init__(self, occupied): self.pos = random_food(occupied)
    def draw(self, surface):
        c, r = self.pos
        cx, cy = c * CELL + CELL//2, r * CELL + CELL//2 + HUD_H
        pygame.draw.circle(surface, RED, (cx, cy), CELL//2 - 2)
        pygame.draw.circle(surface, (255,120,120), (cx-3, cy-3), 3)

def draw_hud(surface, score, level, foods_this_level):
    pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_W, HUD_H))
    pygame.draw.line(surface, LT_GRAY, (0, HUD_H), (SCREEN_W, HUD_H), 2)
    sc, lv = font.render(f"Score: {score}", True, WHITE), font.render(f"Level {level}", True, GOLD)
    nxt = font.render(f"Next ↑: {FOODS_PER_LEVEL - foods_this_level}", True, GREEN)
    surface.blit(sc, (12, HUD_H//2 - sc.get_height()//2))
    surface.blit(lv, (SCREEN_W//2 - lv.get_width()//2, HUD_H//2 - lv.get_height()//2))
    surface.blit(nxt, (SCREEN_W - nxt.get_width() - 12, HUD_H//2 - nxt.get_height()//2))

def draw_border(surface): pygame.draw.rect(surface, LT_GRAY, (0, HUD_H, SCREEN_W, CELL * ROWS), 2)

def draw_overlay(surface, title, sub=""):
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))
    t = big.render(title, True, WHITE)
    surface.blit(t, (SCREEN_W//2 - t.get_width()//2, SCREEN_H//2 - 70))
    if sub:
        s = font.render(sub, True, YELLOW)
        surface.blit(s, (SCREEN_W//2 - s.get_width()//2, SCREEN_H//2))
    hint = font.render("R – restart   Q – quit", True, (180,180,180))
    surface.blit(hint, (SCREEN_W//2 - hint.get_width()//2, SCREEN_H//2 + 50))

def main():
    snake, food = Snake(), Food(Snake().cells)
    score, level, total_foods_eaten, current_fps, game_over = 0, 1, 0, BASE_FPS, False
    
    while True:
        clock.tick(current_fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: main(); return
                    if event.key == pygame.K_q: pygame.quit(); sys.exit()
                else:
                    if event.key in (pygame.K_UP, pygame.K_w): snake.queue_direction(UP)
                    if event.key in (pygame.K_DOWN, pygame.K_s): snake.queue_direction(DOWN)
                    if event.key in (pygame.K_LEFT, pygame.K_a): snake.queue_direction(LEFT)
                    if event.key in (pygame.K_RIGHT, pygame.K_d): snake.queue_direction(RIGHT)
        
        if not game_over:
            snake.move()
            if snake.hit_wall() or snake.hit_self(): game_over = True
            elif snake.body[0] == food.pos:
                snake.eat()
                total_foods_eaten += 1
                score += 10 * level
                new_level = total_foods_eaten // FOODS_PER_LEVEL + 1
                if new_level > level:
                    level, current_fps = new_level, BASE_FPS + (level) * FPS_PER_LEVEL
                food = Food(snake.cells)
        
        screen.fill(BLACK)
        draw_hud(screen, score, level, total_foods_eaten % FOODS_PER_LEVEL if total_foods_eaten else 0)
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(screen, (20,20,20), (c*CELL, r*CELL+HUD_H, CELL, CELL), 1)
        draw_border(screen)
        food.draw(screen)
        snake.draw(screen)
        if game_over: draw_overlay(screen, "GAME OVER", f"Score: {score}   Level: {level}")
        pygame.display.flip()

if __name__ == "__main__":
    main()