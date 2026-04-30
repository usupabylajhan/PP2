import pygame
import sys
import math

SCREEN_W, SCREEN_H, TOOLBAR_W = 900, 650, 160
CANVAS_X, CANVAS_W, CANVAS_H = TOOLBAR_W, SCREEN_W - TOOLBAR_W, SCREEN_H
WHITE, BLACK, BG_TOOLBAR, BG_CANVAS, HIGHLIGHT, TEXT_COLOUR, GRID_COLOUR = (255,255,255), (0,0,0), (40,42,54), (255,255,255), (80,140,255), (220,220,220), (230,230,230)

PALETTE = [(0,0,0), (220,40,40), (30,120,255), (50,200,80), (255,220,0), (255,140,0), (180,60,200), (0,200,200), (255,105,180), (139,90,43), (128,128,128), (255,255,255)]
BRUSH_SIZES = [2, 4, 8, 16]

TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE, TOOL_RTRIANGLE, TOOL_EQTRIANGLE, TOOL_RHOMBUS, TOOL_FILL, TOOL_ERASER = "pencil", "line", "rect", "square", "circle", "right_tri", "eq_tri", "rhombus", "fill", "eraser"
TOOL_LABELS = {TOOL_PENCIL:"✏ Pencil", TOOL_LINE:"╱ Line", TOOL_RECT:"▭ Rectangle", TOOL_SQUARE:"■ Square", TOOL_CIRCLE:"○ Circle", TOOL_RTRIANGLE:"◺ R-Triangle", TOOL_EQTRIANGLE:"△ Eq-Triangle", TOOL_RHOMBUS:"◇ Rhombus", TOOL_FILL:"🪣 Fill", TOOL_ERASER:"⬜ Eraser"}
TOOL_ORDER = [TOOL_PENCIL, TOOL_LINE, TOOL_RECT, TOOL_SQUARE, TOOL_CIRCLE, TOOL_RTRIANGLE, TOOL_EQTRIANGLE, TOOL_RHOMBUS, TOOL_FILL, TOOL_ERASER]

def points_for_right_triangle(x1, y1, x2, y2): return [(x1, y1), (x1, y2), (x2, y2)]
def points_for_equilateral_triangle(x1, y1, x2, y2):
    bx1, bx2, by = min(x1, x2), max(x1, x2), max(y1, y2)
    cx, side = (bx1 + bx2) / 2, bx2 - bx1
    return [(cx, by - side * math.sqrt(3) / 2), (bx1, by), (bx2, by)]
def points_for_rhombus(x1, y1, x2, y2):
    lx, rx, ty, by = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
    cx, cy = (lx + rx) / 2, (ty + by) / 2
    return [(cx, ty), (rx, cy), (cx, by), (lx, cy)]

def flood_fill(surface, pos, fill_colour):
    target = surface.get_at(pos)[:3]
    if target == fill_colour: return
    w, h, stack, visited = surface.get_size(), [pos], set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or x >= w[0] or y < 0 or y >= w[1]: continue
        if surface.get_at((x, y))[:3] != target: continue
        surface.set_at((x, y), fill_colour)
        visited.add((x, y))
        stack += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

class Toolbar:
    BTN_H, BTN_PAD, SEC_GAP = 34, 4, 10
    def __init__(self, font, small_font):
        self.font, self.small_font = font, small_font
        self.tool_rects, y = {}, 10
        for tool in TOOL_ORDER:
            self.tool_rects[tool] = pygame.Rect(6, y, TOOLBAR_W - 12, self.BTN_H)
            y += self.BTN_H + self.BTN_PAD
        self.tool_section_bottom = y + self.SEC_GAP
        self.palette_rects, px, py = [], 8, self.tool_section_bottom + 24
        for i, col in enumerate(PALETTE):
            self.palette_rects.append((pygame.Rect(px + (i%4)*(32), py + (i//4)*(32), 28, 28), col))
        self.palette_bottom = py + ((len(PALETTE)//4 + 1)*32) + self.SEC_GAP
        self.size_rects, sx, sy = [], 10, self.palette_bottom + 24
        for i, sz in enumerate(BRUSH_SIZES):
            self.size_rects.append((pygame.Rect(sx + i*34, sy, 30, 30), sz))
        self.clear_rect = pygame.Rect(10, sy + 44, TOOLBAR_W - 20, 32)
    def draw(self, surface, active_tool, active_colour, active_size):
        pygame.draw.rect(surface, BG_TOOLBAR, (0, 0, TOOLBAR_W, SCREEN_H))
        pygame.draw.line(surface, HIGHLIGHT, (TOOLBAR_W-1, 0), (TOOLBAR_W-1, SCREEN_H), 2)
        title = self.small_font.render("TOOLS", True, TEXT_COLOUR)
        surface.blit(title, (TOOLBAR_W//2 - title.get_width()//2, 2))
        for tool, rect in self.tool_rects.items():
            pygame.draw.rect(surface, HIGHLIGHT if tool == active_tool else (60,63,78), rect, border_radius=5)
            txt = self.small_font.render(TOOL_LABELS[tool], True, WHITE)
            surface.blit(txt, txt.get_rect(center=rect.center))
        ph = self.small_font.render("COLOUR", True, TEXT_COLOUR)
        surface.blit(ph, (TOOLBAR_W//2 - ph.get_width()//2, self.tool_section_bottom + 6))
        for rect, col in self.palette_rects:
            pygame.draw.rect(surface, col, rect, border_radius=4)
            pygame.draw.rect(surface, WHITE if col == active_colour else (100,100,100), rect, 3 if col == active_colour else 1, border_radius=4)
        sh = self.small_font.render("SIZE", True, TEXT_COLOUR)
        surface.blit(sh, (TOOLBAR_W//2 - sh.get_width()//2, self.palette_bottom + 6))
        for rect, sz in self.size_rects:
            pygame.draw.rect(surface, HIGHLIGHT if sz == active_size else (60,63,78), rect, border_radius=4)
            pygame.draw.circle(surface, WHITE, rect.center, min(sz//2, 10))
        pygame.draw.rect(surface, (180,50,50), self.clear_rect, border_radius=6)
        ct = self.small_font.render("🗑 Clear", True, WHITE)
        surface.blit(ct, ct.get_rect(center=self.clear_rect.center))
    def handle_click(self, pos, active_tool, active_colour, active_size):
        new_tool, new_colour, new_size, clear = active_tool, active_colour, active_size, False
        for tool, rect in self.tool_rects.items():
            if rect.collidepoint(pos): new_tool = tool
        for rect, col in self.palette_rects:
            if rect.collidepoint(pos): new_colour = col
        for rect, sz in self.size_rects:
            if rect.collidepoint(pos): new_size = sz
        if self.clear_rect.collidepoint(pos): clear = True
        return new_tool, new_colour, new_size, clear

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Paint – Practice 11")
        self.clock, self.font, self.small_font = pygame.time.Clock(), pygame.font.SysFont("arial", 18, True), pygame.font.SysFont("arial", 13)
        self.canvas = pygame.Surface((CANVAS_W, CANVAS_H))
        self.canvas.fill(BG_CANVAS)
        self.toolbar = Toolbar(self.font, self.small_font)
        self.active_tool, self.active_colour, self.active_size = TOOL_PENCIL, BLACK, 4
        self.drawing, self.start_pos, self.last_pos, self.running = False, None, None, True
    def to_canvas(self, pos): return (pos[0] - CANVAS_X, pos[1])
    def on_canvas(self, pos): return pos[0] >= CANVAS_X
    def run(self):
        while self.running:
            self.clock.tick(60)
            self._handle_events()
            self._draw()
        pygame.quit()
        sys.exit()
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q): self.running = False
                if event.key == pygame.K_DELETE: self.canvas.fill(BG_CANVAS)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if not self.on_canvas(pos):
                    self.active_tool, self.active_colour, self.active_size, clear = self.toolbar.handle_click(pos, self.active_tool, self.active_colour, self.active_size)
                    if clear: self.canvas.fill(BG_CANVAS)
                else:
                    cp = self.to_canvas(pos)
                    self.drawing, self.start_pos, self.last_pos = True, cp, cp
                    if self.active_tool == TOOL_FILL: flood_fill(self.canvas, cp, self.active_colour); self.drawing = False
                    elif self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                        colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                        pygame.draw.circle(self.canvas, colour, cp, self.active_size // 2)
            elif event.type == pygame.MOUSEMOTION and self.drawing and self.on_canvas(event.pos):
                cp = self.to_canvas(event.pos)
                if self.active_tool in (TOOL_PENCIL, TOOL_ERASER):
                    colour = WHITE if self.active_tool == TOOL_ERASER else self.active_colour
                    pygame.draw.line(self.canvas, colour, self.last_pos, cp, self.active_size)
                    self.last_pos = cp
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.drawing and self.on_canvas(event.pos):
                self._commit_shape(self.start_pos, self.to_canvas(event.pos))
                self.drawing, self.start_pos = False, None
    def _commit_shape(self, p1, p2):
        x1, y1, x2, y2 = *p1, *p2
        col, w, tool = self.active_colour, self.active_size, self.active_tool
        if tool == TOOL_LINE: pygame.draw.line(self.canvas, col, p1, p2, w)
        elif tool == TOOL_RECT: rx, ry = min(x1,x2), min(y1,y2); pygame.draw.rect(self.canvas, col, (rx, ry, abs(x2-x1), abs(y2-y1)), w)
        elif tool == TOOL_SQUARE: side = min(abs(x2-x1), abs(y2-y1)); sx = x1 if x2 >= x1 else x1-side; sy = y1 if y2 >= y1 else y1-side; pygame.draw.rect(self.canvas, col, (sx, sy, side, side), w)
        elif tool == TOOL_CIRCLE: cx, cy = (x1+x2)//2, (y1+y2)//2; pygame.draw.circle(self.canvas, col, (cx, cy), max(1, int(math.hypot(x2-x1, y2-y1)/2)), w)
        elif tool == TOOL_RTRIANGLE: pygame.draw.polygon(self.canvas, col, [(int(p[0]), int(p[1])) for p in points_for_right_triangle(x1,y1,x2,y2)], w)
        elif tool == TOOL_EQTRIANGLE: pygame.draw.polygon(self.canvas, col, [(int(p[0]), int(p[1])) for p in points_for_equilateral_triangle(x1,y1,x2,y2)], w)
        elif tool == TOOL_RHOMBUS: pygame.draw.polygon(self.canvas, col, [(int(p[0]), int(p[1])) for p in points_for_rhombus(x1,y1,x2,y2)], w)
    def _draw_preview(self, surface, p1, p2):
        def sc(pt): return (pt[0] + CANVAS_X, pt[1])
        x1, y1, x2, y2 = *p1, *p2
        col, w, tool = self.active_colour, self.active_size, self.active_tool
        if tool == TOOL_LINE: pygame.draw.line(surface, col, sc(p1), sc(p2), w)
        elif tool == TOOL_RECT: rx, ry = min(x1,x2)+CANVAS_X, min(y1,y2); pygame.draw.rect(surface, col, (rx, ry, abs(x2-x1), abs(y2-y1)), w)
        elif tool == TOOL_SQUARE: side = min(abs(x2-x1), abs(y2-y1)); sx = (x1 if x2>=x1 else x1-side)+CANVAS_X; sy = y1 if y2>=y1 else y1-side; pygame.draw.rect(surface, col, (sx, sy, side, side), w)
        elif tool == TOOL_CIRCLE: cx, cy = (x1+x2)//2 + CANVAS_X, (y1+y2)//2; pygame.draw.circle(surface, col, (cx, cy), max(1, int(math.hypot(x2-x1, y2-y1)/2)), w)
        elif tool == TOOL_RTRIANGLE: pygame.draw.polygon(surface, col, [(int(px)+CANVAS_X, int(py)) for px,py in points_for_right_triangle(x1,y1,x2,y2)], w)
        elif tool == TOOL_EQTRIANGLE: pygame.draw.polygon(surface, col, [(int(px)+CANVAS_X, int(py)) for px,py in points_for_equilateral_triangle(x1,y1,x2,y2)], w)
        elif tool == TOOL_RHOMBUS: pygame.draw.polygon(surface, col, [(int(px)+CANVAS_X, int(py)) for px,py in points_for_rhombus(x1,y1,x2,y2)], w)
    def _draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.canvas, (CANVAS_X, 0))
        if self.drawing and self.start_pos and self.active_tool not in (TOOL_PENCIL, TOOL_ERASER, TOOL_FILL):
            self._draw_preview(self.screen, self.start_pos, self.to_canvas(pygame.mouse.get_pos()))
        self.toolbar.draw(self.screen, self.active_tool, self.active_colour, self.active_size)
        mx, my = pygame.mouse.get_pos()
        cx, cy = self.to_canvas((mx, my))
        status = self.small_font.render(f"{TOOL_LABELS.get(self.active_tool, '')} ({cx},{cy}) sz:{self.active_size}", True, TEXT_COLOUR)
        pygame.draw.rect(self.screen, (25,25,35), (0, SCREEN_H-18, TOOLBAR_W, 18))
        self.screen.blit(status, (4, SCREEN_H-16))
        pygame.display.flip()

if __name__ == "__main__":
    app = PaintApp()
    app.run()