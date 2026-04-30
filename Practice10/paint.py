import pygame, sys, math

pygame.init()

W,H,T = 900,650,70
CT,CH = T,H-T

BLACK,WHITE = (0,0,0),(255,255,255)
LT,MG,DK = (230,230,230),(160,160,160),(80,80,80)

PALETTE = [
(0,0,0),(255,255,255),(220,30,30),(30,180,30),(30,80,220),
(255,220,0),(255,130,0),(140,0,200),(0,200,200),(255,0,180),
(120,80,40),(100,100,100),(255,160,180),(0,100,60)
]

PENCIL,RECT,CIRCLE,ERASER = "pencil","rectangle","circle","eraser"
TOOLS = [PENCIL,RECT,CIRCLE,ERASER]
ICONS = ["✏ Pencil","▭ Rect","◯ Circle","⌫ Eraser"]

screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",15,True)
small = pygame.font.SysFont("Arial",13)

class App:
    def __init__(s):
        s.canvas = pygame.Surface((W,CH)); s.canvas.fill(WHITE)
        s.color, s.tool = BLACK, PENCIL
        s.bs, s.es = 5, 20
        s.drawing, s.start, s.prev, s.snap = False, None, None, None

    def handle(s,e):
        if e.type==pygame.MOUSEBUTTONDOWN and e.button==1: s.press(e.pos)
        elif e.type==pygame.MOUSEMOTION and s.drawing: s.drag(e.pos)
        elif e.type==pygame.MOUSEBUTTONUP and e.button==1: s.release(e.pos)

    def press(s,pos):
        x,y = pos
        if y<T:
            s.toolbar(x,y); return
        cp=(x,y-CT)
        s.drawing, s.start, s.prev = True, cp, cp
        if s.tool==PENCIL:
            pygame.draw.circle(s.canvas,s.color,cp,s.bs)
        elif s.tool==ERASER:
            pygame.draw.circle(s.canvas,WHITE,cp,s.es)
        else:
            s.snap=s.canvas.copy()

    def drag(s,pos):
        x = max(0,min(W-1,pos[0]))
        y = max(CT,min(H-1,pos[1]))
        cp=(x,y-CT)

        if s.tool==PENCIL:
            pygame.draw.line(s.canvas,s.color,s.prev,cp,s.bs*2)
            pygame.draw.circle(s.canvas,s.color,cp,s.bs)
            s.prev=cp
        elif s.tool==ERASER:
            pygame.draw.circle(s.canvas,WHITE,cp,s.es)
            s.prev=cp
        else:
            s.canvas.blit(s.snap,(0,0))
            s.shape(s.start,cp,s.canvas)

    def release(s,pos):
        if not s.drawing: return
        x = max(0,min(W-1,pos[0]))
        y = max(CT,min(H-1,pos[1]))
        cp=(x,y-CT)

        if s.tool in (RECT,CIRCLE):
            s.canvas.blit(s.snap,(0,0))
            s.shape(s.start,cp,s.canvas)

        s.drawing, s.start, s.prev, s.snap = False, None, None, None

    def shape(s,p1,p2,surf):
        x1,y1=p1; x2,y2=p2
        if s.tool==RECT:
            pygame.draw.rect(surf,s.color,
                (min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1)),2)
        else:
            cx,cy=(x1+x2)//2,(y1+y2)//2
            r=int(math.hypot(x2-x1,y2-y1)/2)
            if r>0:
                pygame.draw.circle(surf,s.color,(cx,cy),r,2)

    def toolbar(s,x,y):
        for i,c in enumerate(PALETTE):
            sx=10+i*38
            if sx<=x<=sx+32 and 6<=y<=34:
                s.color=c; return

        for i,t in enumerate(TOOLS):
            tx=10+i*100
            if tx<=x<=tx+92 and 38<=y<=62:
                s.tool=t; return

        if 628<=x<=650:
            if 6<=y<=28: s.bs=max(1,s.bs-1)
            if 36<=y<=58: s.es=max(5,s.es-2)

        if 654<=x<=676:
            if 6<=y<=28: s.bs=min(40,s.bs+1)
            if 36<=y<=58: s.es=min(60,s.es+2)

        if W-90<=x<=W-10 and 20<=y<=50:
            s.canvas.fill(WHITE)

    def draw(s,screen):
        screen.blit(s.canvas,(0,CT))
        mx,my=pygame.mouse.get_pos()

        if s.tool==ERASER:
            pygame.draw.circle(screen,MG,(mx,my),s.es,2)

        pygame.draw.rect(screen,LT,(0,0,W,T))
        pygame.draw.line(screen,MG,(0,T),(W,T),2)

        for i,c in enumerate(PALETTE):
            sx=10+i*38
            pygame.draw.rect(screen,c,(sx,6,32,28))
            pygame.draw.rect(screen,BLACK if c==s.color else DK,
                             (sx,6,32,28),3 if c==s.color else 1)

        for i,(t,ic) in enumerate(zip(TOOLS,ICONS)):
            tx=10+i*100
            col=(90,140,240) if t==s.tool else (190,190,190)
            pygame.draw.rect(screen,col,(tx,38,92,26),border_radius=4)
            txt=font.render(ic,1,WHITE if t==s.tool else BLACK)
            screen.blit(txt,(tx+46-txt.get_width()//2,44))

        s.size(screen,550,6,"Brush",s.bs)
        s.size(screen,550,36,"Ersr",s.es)

        pygame.draw.rect(screen,s.color,(W-100,8,42,42))
        pygame.draw.rect(screen,BLACK,(W-100,8,42,42),2)

        pygame.draw.rect(screen,(210,60,60),(W-90,20,74,28),border_radius=5)
        t=font.render("Clear",1,WHITE)
        screen.blit(t,(W-90+37-t.get_width()//2,25))

    def size(s,screen,x,y,l,v):
        screen.blit(small.render(f"{l}: {v}",1,DK),(x,y+2))
        pygame.draw.rect(screen,MG,(x+78,y,22,22),border_radius=3)
        screen.blit(font.render("−",1,BLACK),(x+83,y+2))
        pygame.draw.rect(screen,MG,(x+104,y,22,22),border_radius=3)
        screen.blit(font.render("+",1,BLACK),(x+108,y+2))

def main():
    app=App()
    while True:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit(); sys.exit()
            app.handle(e)

        screen.fill(WHITE)
        app.draw(screen)
        pygame.display.flip()

main()