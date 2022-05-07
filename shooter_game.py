from pygame import *
from random import (
    randint,
    random,
)


font.init()
lost = 0
score = 0



class GameSprite(sprite.Sprite):
    def __init__(self ,player_image , x_pos, y_pos, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(
            image.load(player_image),
            (width, height)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -self.height:
            self.kill()

class AsteroidBullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 500:
            self.kill()


class Player(GameSprite):
    def __init__(self, player_image, x_pos, y_pos, width, height, speed):
        super().__init__(player_image, x_pos, y_pos, width, height, speed)
        self.bullets = sprite.Group()

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        elif keys[K_d] and self.rect.x < 630:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + self.height / 2 - 5, self.rect.y, 10, 20, 20)
        self.bullets.add(bullet)


class Enemy(GameSprite):
    def __init__(self, player_image, x_pos, y_pos, width, height, speed):
        super(). __init__(player_image, x_pos, y_pos, width, height, speed)
        self.bullet = None

    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 502:
            self.rect.y = -70
            self.rect.x = randint(0, 635)
            lost += 1
        n = randint(0, 250)
        if not self.bullet:
            if self.rect.y >= n:
                self.bullet = AsteroidBullet('asteroid.png', self.rect.centerx - 5, self.rect.bottom, 20, 20, 5)
                


class FontClass():
    def __init__(self, text, x_pos, y_pos, text_color = (255, 255, 255), fsize = 30):
        self.font = font.SysFont('Arial', fsize)
        self.image = self.font.render(text, True, text_color)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.text_color = text_color

    def update_score(self, score):
        self.image = self.font.render(self.text + str(score), True, self.text_color)

    def reset(self):
        window.blit(self.image, (self.x_pos, self.y_pos))
        


score_font = FontClass('Счет: ' + str(score), 5, 10)
missed_font = FontClass('Пропущено: ' + str(lost), 5, 30)


enemys = sprite.Group()
for i in range(5):
    enemys.add(
        Enemy('ufo_PNG.png', randint(0, 635), -70, 65, 65, randint(1,3))
    )
hero = Player('clipart2808871.png', 317.5, 420, 65, 65, 5)
window = display.set_mode((700, 500))
background = transform.scale(
    image.load('galaxy.jpg'),
    (700, 500)
)
fps = 60
clock = time.Clock()
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.3)
game = True
lose = FontClass('Проигрыш!', 250, 235, (255, 0, 0), 60)
win = FontClass('Победа!', 270, 235, (255, 0, 0), 60)
fire_sound = mixer.Sound('fire.ogg')
finish = False
boom = None
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key ==K_SPACE:
                hero.fire()
                if not finish:
                    fire_sound.play()
    if not finish:
        groupcollides = sprite.groupcollide(enemys, hero.bullets, True, True)
        spritecollide = sprite.spritecollide(hero, enemys, False)
        window.blit(background, (0, 0))
        if groupcollides:
                score += 1 
                enemys.add(
                Enemy('ufo_PNG.png', randint(0, 635), -70, 65, 65, randint(1,3))
            )
                collide = list(groupcollides.keys())[0]
                boom = GameSprite('boom.png.png', collide.rect.x, collide.rect.y, 65, 65, 0)
                boom.reset()  
        hero.reset()  
        hero.update()
        enemys.draw(window)
        enemys.update()
        hero.bullets.update()
        hero.bullets.draw(window)
        score_font.update_score(score)
        score_font.reset()
        missed_font.update_score(lost)
        missed_font.reset()
        if boom:
            boom.reset()
        if spritecollide or lost > 3:
            finish = True
            boom = GameSprite('boom.png.png', hero.rect.centerx - 82.5, hero.rect.top - 82.5, 165, 165, 0)
            boom.reset()
            mixer.music.stop()
            lose.reset()
        if score >= 9:
            finish = True
            mixer.music.stop()
            win.reset()
        for ene in enemys:
            if ene.bullet:
                ene.bullet.update()
                ene.bullet.reset()
                if sprite.collide_rect(ene.bullet, hero):
                    finish = True
                    boom = GameSprite('boom.png.png', hero.rect.centerx - 82.5, hero.rect.top - 82.5, 165, 165, 0)
                    mixer.music.stop()
                    boom.reset()
                    lose.reset()
        display.update()
        clock.tick(fps)