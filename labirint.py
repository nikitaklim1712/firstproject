# Разработай свою игру в этом файле!
from pygame import *
rback = 700,500

back = display.set_mode(rback)
PINK = 254, 204, 255
win = transform.scale(image.load('gg.png'),(700,500))
lose = transform.scale(image.load('game-over.png'),(700,500))

display.set_caption('смешной лабиринтик')
run = True
x_speed = 0
y_speed = 0
bullets = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self,picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        back.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,picture,w,h,x,y,x_speed,y_speed):
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,p.rect.right)
        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.right,self.rect.centery,30,30,10)
        bullets.add(bullet)
class Enemy(GameSprite):
    def __init__(self,picture,x,y,w,h,speed,x1,x2):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
        self.x1 = x1
        self.x2 = x2
    def update(self):
        if self.rect.x <= self.x1:
            self.direction = 'right'
        if self.rect.x >= self.x2 - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Bullet(GameSprite):
    def __init__(self,picture,x,y,w,h,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()
        
          
player = Player('free-icon-ghost-2213748.png',65,65,55,55,x_speed,y_speed)
wall_1 = GameSprite('images.png',150,400,150,250)
wall_2 = GameSprite('images.png',60,200,500,0)
wall_3 = GameSprite('images.png',160,50,400,200)
final = GameSprite('winner.png',65,65,600,400)

enemyg = Enemy('ghost.png',200,400,65,65,5, 200,600)
enemies = sprite.Group()
enemies.add(enemyg)

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)
barriers.add(wall_3)
finish = False

while run:
    if finish != True:
        back.fill((254, 204, 255))
        enemies.draw(back)
        enemies.update()
        barriers.draw(back)
        player.reset()
        player.update()
        bullets.draw(back)
        bullets.update()
        time.delay(50)
        final.reset()
        sprite.groupcollide(bullets,barriers,True,False)
        sprite.groupcollide(bullets,enemies,True,True)
        if sprite.collide_rect(player, final):
            finish = True
            back.blit(win,(0,0))
        if sprite.spritecollide(player, enemies,True):
            finish = True
            back.blit(lose,(0,0))

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_w:
                player.y_speed = -10
            if e.key == K_s:
                player.y_speed = 10
            if e.key == K_a:
                player.x_speed = -10
            if e.key == K_d:
                player.x_speed = 10
        elif e.type == KEYUP:
            if e.key == K_w:
                player.y_speed = 0
            if e.key == K_s:
                player.y_speed = 0
            if e.key == K_a:
                player.x_speed = 0
            if e.key == K_d:
                player.x_speed = 0
    
        
        
    display.update()

