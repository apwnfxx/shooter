#Создай собственный Шутер!

from pygame import *
from random import randint


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

lose = 0
score = 0
max_lose = 3
max_score = 10
life = 4


font.init()
font1 = font.SysFont('Arial', 36)
fire_sound = mixer.Sound('fire.ogg')
font2 = font.SysFont('Arial', 80)

win = font2.render('YOU WIN!', True, (100, 0, 0))
lost = font2.render('YOU LOSE!',  True, (100,0,0))



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < width - 80:
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 10:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('la.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0
            lose += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()




width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (width, height))
hero = Player('i.png', 350, height - 80, 10)
monsters = sprite.Group()
for i in range(1,3):
    monster = Enemy('kf.png', randint(80,width-80), -20, randint(1,3))
    monsters.add(monster)

bullets =  sprite.Group()

asteroids = sprite.Group()
for i in range(1,3):
    asteroid =  Enemy('asteroid.png', randint(80, width -80), -40, randint(1,5))
    asteroids.add(asteroid)




game = True
finish = False

FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                hero.fire()

   


    if not finish:
    
        window.blit(background, (0,0))
        text_lose = font1.render('Пропущено: '+str(lose),True,(255,0,0))
        text_win = font1.render('Счет:'+ str(score), True, (255,0,0))
        window.blit(text_win,(10,10))
        window.blit(text_lose, (10, 50))
        hero.update()
        hero.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)


        collides = sprite.groupcollide(monsters, bullets, True, True)
        collides1 = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('kf.png', randint(80,width-80), -20, randint(1,3))
            monsters.add(monster)
                
        if sprite.spritecollide(hero, monsters, False) or sprite.spritecollide(hero, asteroids, False):
            sprite.spritecollide(hero,monsters, True)
            sprite.spritecollide(hero, asteroids, True)
            life -= 1

        if life == 0 or lose >= max_lose:
        
            finish = True
            window.blit(lost,(210,250))

        if score >= max_score:
            finish = True
            window.blit(win,(210,250))

        if life > 2:
            life_color =  (0,170,0)
        if life  <= 2 and life > 1:
            life_color = (250,100,0)
        if life == 1:
            life_color = (170,0,0)

        text_life = font1.render(str(life), True, life_color)
        window.blit(text_life,(650,10))
        display.update()
    else:
        finish = False
        lose = 0
        score = 0
        max_lose = 3
        max_score = 10
        life = 4

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        clock.tick(3000)
        for i in range(1,3):
            monster = Enemy('kf.png', randint(80,width-80), -20, randint(1,3))
            monsters.add(monster)
        for i in range(1,3):
            asteroid =  Enemy('asteroid.png', randint(80, width -80), -40, randint(1,5))
            asteroids.add(asteroid)



        


    clock.tick(FPS)