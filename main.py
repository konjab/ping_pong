from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

back = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

game = True
finish = False
clock = time.Clock()
FPS = 60

racket1 = Player('racket.png', 0, 200, 100, 100, 5)
racket2 = Player('racket.png', 520, 200, 100, 100, 5)
ball = GameSprite('tenis_ball.png', 200, 200, 50, 50, 70)

font.init()
font = font.Font(None, 35)

speed_x = 5
speed_y = 5

score1 = 0
score2 = 0
max_score = 3
ball_moving = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.fill(back)
        score_text = font.render(f"{score1} : {score2}", True, (0, 0, 0))
        window.blit(score_text, (win_width // 2 - 30, 20))

        racket1.update_l()
        racket2.update_r()

        if ball_moving:
            ball.rect.x += speed_x
            ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            score2 += 1
            if score2 == max_score:
                finish = True
                end_text = font.render(f"PLAYER 2 WINS!  {score1} : {score2}", True, (0, 180, 0))
                window.blit(end_text, (160, 200))
            else:
                ball.rect.x, ball.rect.y = racket1.rect.right + 5, racket1.rect.y + 25
                speed_x = 5
                speed_y = 5
                ball_moving = False

        if ball.rect.x > win_width:
            score1 += 1
            if score1 == max_score:
                finish = True
                end_text = font.render(f"PLAYER 1 WINS!  {score1} : {score2}", True, (0, 180, 0))
                window.blit(end_text, (160, 200))
            else:
                ball.rect.x, ball.rect.y = racket2.rect.left - 55, racket2.rect.y + 25
                speed_x = -5
                speed_y = 5
                ball_moving = False

        keys = key.get_pressed()
        if not ball_moving:
            if score1 < max_score and score2 < max_score:
                if ball.rect.x < win_width // 2 and keys[K_d]:
                    ball_moving = True
                if ball.rect.x > win_width // 2 and keys[K_LEFT]:
                    ball_moving = True

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
