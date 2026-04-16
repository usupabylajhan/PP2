class Ball:
    def __init__(self, screen_w, screen_h):
        self.r = 25
        self.x = screen_w // 2
        self.y = screen_h // 2
        self.step = 20
        self.screen_w = screen_w
        self.screen_h = screen_h
 
    def move(self, dx, dy):
        nx = self.x + dx
        ny = self.y + dy
        if self.r <= nx <= self.screen_w - self.r:
            self.x = nx
        if self.r <= ny <= self.screen_h - self.r:
            self.y = ny