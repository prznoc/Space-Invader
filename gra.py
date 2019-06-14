import pygame, random
# Let's import the Car Class
from car import Player

class Pane(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.Font("assets/space_invaders.ttf", 100)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
        self.screen.fill((BLACK))


    def addRect(self, locx, locy, color):
        self.rect = pygame.draw.rect(self.screen, color, (locx, locy , 700, 110), 2)

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

blaster = pygame.mixer.Sound("assets/blaster.wav")
bum = pygame.mixer.Sound("assets/bum.wav")
alarm = pygame.mixer.Sound("assets/alarm.wav")


level = 0
lives = 3

font = pygame.font.Font("assets/space_invaders.ttf", 15)
mfont = pygame.font.Font("assets/space_invaders.ttf", 40)
bfont = pygame.font.Font("assets/space_invaders.ttf", 100)
vbfont = pygame.font.Font("assets/space_invaders.ttf", 150)

SCREENWIDTH = 1920
SCREENHEIGHT = 1080

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
pygame.display.set_caption("Car Racing")

# This will be a list that will contain all the sprites we intend to use in our game.



def menu():
    menuOn = True
    pan = Pane()
    color = GREEN
    color2 = BLACK
    screen.fill(BLACK)
    text = bfont.render("START GAME", True, WHITE)
    text2 = bfont.render("QUIT", True, WHITE)
    text3 = vbfont.render("SPACE INVADERS", True, RED)
    text_rect = text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
    text_rect2 = text2.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 + 200))
    text_rect3 = text3.get_rect(center=(SCREENWIDTH / 2, 100))
    event = pygame.event.get()

    while menuOn:
        screen.fill(BLACK)
        pan.addRect(SCREENWIDTH / 2 - 355, SCREENHEIGHT / 2 - 69, color)
        pan.addRect(SCREENWIDTH / 2 - 355, SCREENHEIGHT / 2 + 131, color2)
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    color = GREEN
                    color2 = BLACK
                if event.key == pygame.K_DOWN:
                    color = BLACK
                    color2 = GREEN
                if event.key == pygame.K_SPACE and color2 == GREEN:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE and color == GREEN:
                    play(0,lives)
                    menuOn = False
        pygame.display.flip()


def lost():
    lostOn = True
    text = bfont.render("YOU LOST", True, RED)
    text_rect = text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
    while lostOn:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lostOn = False
        if lostOn == False:
            menu()
        pygame.display.flip()


def nextlevel(level, lives):
    levelOn = True
    lives = lives
    level = level + 1
    text = mfont.render("To contiune press space", True, WHITE)
    text_rect = text.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
    while levelOn:
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play(level,lives)
                    levelOn = False
        pygame.display.flip()


def play(level, lives):
    yyy = 1  # do szybkostrzelnosci
    zzz = 50
    cont = 0  # kontrolowanie ruchu wrogów
    strzal = 60
    bon = 0
    bon2 = 0
    ai = True
    hearts = lives
    color1 = BLACK
    color2 = BLACK
    licz1 = 0
    licz2 = 0
    wrog = 0

    image1 = pygame.image.load("assets/shooter.png").convert_alpha()
    image2 = pygame.image.load("assets/a1_1.png").convert_alpha()
    image3 = pygame.image.load("assets/heromissile.png").convert_alpha()
    image4 = pygame.image.load("assets/enemymissile.png").convert_alpha()
    image5 = pygame.image.load("assets/gift.png").convert_alpha()
    image6 = pygame.image.load("assets/brick.png").convert_alpha()

    playerCar = Player(30, 60, 70, image1)
    playerCar.rect.x = SCREENWIDTH / 2
    playerCar.rect.y = SCREENHEIGHT - 100

    enemies = [Player(40, 20, 30, image2) for i in range(20)]
    x = 0
    for car in enemies:
        if x < 10:
            car.rect.x = 60 + x * 100
            car.rect.y = 60
        else:
            car.rect.x = 60 + (x - 10) * 100
            car.rect.y = 160
        x = x + 1

    barrier = [Player(10,10,10, image6)for i in range (120)]
    x = 0
    y = 0
    z = 0
    for brick in barrier:
        brick.rect.x = 80 + 480*z + 32*x
        brick.rect.y = playerCar.rect.y - 200 - y*10
        x = x+1
        if x==10 and y != 2:
            x = 0
            y = y+1
        if y == 2 and x == 10 :
            x = 0
            y = 0
            z = z+1

    missiles = []
    enemymissiles = []

    # Add the car to the list of objects
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(playerCar)
    for car in enemies:
        all_sprites_list.add(car)
    for brick in barrier:
        all_sprites_list.add(brick)

    bullets = pygame.sprite.Group()
    ebullets = pygame.sprite.Group()

    gifts = pygame.sprite.Group()
    prezenty = []

    # Allowing the user to close the window...
    carryOn = True
    clock = pygame.time.Clock()

    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if playerCar.rect.x > 0:
                playerCar.moveLeft(5)
        if keys[pygame.K_RIGHT]:
            if playerCar.rect.x < SCREENWIDTH:
                playerCar.moveRight(5)

        if keys[pygame.K_ESCAPE]:
            carryOn = False


        # szczelanie
        if keys[pygame.K_SPACE]:
            if yyy == 0:
                blaster.play()
                missiles.append(Player(30, 30, 30, image3))
                missiles[-1].rect.y = SCREENHEIGHT - 120
                missiles[-1].rect.x = playerCar.rect.x + 15
                all_sprites_list.add(missiles[-1])
                bullets.add(missiles[-1])
                yyy = yyy + 1
                zzz = 0

        # wrogie szczelanie
        for car in enemies:
            los = random.randrange(1800)
            szansa = level * 2
            if keys[pygame.K_LEFT] and playerCar.rect.x > car.rect.x and ai == True:
                szansa = szansa + level
            if keys[pygame.K_RIGHT] and playerCar.rect.x < car.rect.x and ai == True:
                szansa = szansa + level
            if los <= szansa:
                blaster.play()
                enemymissiles.append(Player(30, 30, 30, image4))
                enemymissiles[-1].rect.y = car.rect.y
                enemymissiles[-1].rect.x = car.rect.x + 15
                all_sprites_list.add(enemymissiles[-1])
                ebullets.add(enemymissiles[-1])

        # Game Logic
        for car in enemies:
            if cont == 0:
                car.moveAlienr(2+level)
            else:
                car.moveAlienl(2+level)
        for car in enemies:
            if car.rect.x > SCREENWIDTH - 60:
                for enemy in enemies:
                    enemy.rect.y += 64
                cont = 1
                break
            if car.rect.x < 0:
                for enemy in enemies:
                    enemy.rect.y += 64
                cont = 0

        for bullet in bullets:
            bullet.moveMissile(10)

        for bullet in ebullets:
            bullet.moveMissile(-10 - (level*3))

        car_collision_list = pygame.sprite.spritecollide(playerCar, enemies, False)
        for car in car_collision_list:
            lost()
            carryOn = False
        all_sprites_list.update()

        for bullet in bullets:
            for enemy in enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    bum.play()
                    bullets.remove(bullet)
                    missiles.remove(bullet)
                    enemies.remove(enemy)
                    all_sprites_list.remove(bullet)
                    all_sprites_list.remove(enemy)
                    los = random.randrange(20)
                    wrog = wrog +1
                    if los <= 5:
                        prezenty.append(Player(30, 30, 30, image5))
                        prezenty[-1].rect.x = enemy.rect.x
                        prezenty[-1].rect.y = enemy.rect.y
                        all_sprites_list.add(prezenty[-1])
                        gifts.add(prezenty[-1])


        for gift in gifts:
            gift.moveMissile(-4)
            if pygame.sprite.collide_rect(gift, playerCar):
                gifts.remove(gift)
                all_sprites_list.remove(gift)
                prezenty.remove(gift)
                bonus = random.randrange(100)
                if bonus < 5:
                    hearts = hearts +1
                if bonus >= 5 and bonus < 30:
                    bon = 0
                    strzal = 30
                    color1 = WHITE
                    licz1 = 10
                if bonus >= 30:
                    bon2 = 0
                    ai = False
                    color2 = WHITE
                    licz2 = 10


        bon += 1
        if bon == 600:
            strzal = 60
            color1 = BLACK
            bon = 0
        if bon%60 == 0:
            licz1 = licz1 - 1

        bon2 += 1
        if bon2 == 600:
            ai = True
            color2 = BLACK
            bon2 = 0
        if bon%60 == 0:
            licz2 = licz2 - 1

        for brick in barrier:
            for bullet in bullets:
                if pygame.sprite.collide_rect(brick, bullet):
                    bullets.remove(bullet)
                    missiles.remove(bullet)
                    barrier.remove(brick)
                    all_sprites_list.remove(brick)
                    all_sprites_list.remove(bullet)

        for brick in barrier:
            for bullet in ebullets:
                if pygame.sprite.collide_rect(brick, bullet):
                    ebullets.remove(bullet)
                    enemymissiles.remove(bullet)
                    barrier.remove(brick)
                    all_sprites_list.remove(brick)
                    all_sprites_list.remove(bullet)

        for bullet in bullets:
            if bullet.rect.y < 0:
                bullets.remove(bullet)
                all_sprites_list.remove(bullet)
                missiles.remove(bullet)

        for bullet in ebullets:
            if pygame.sprite.collide_rect(bullet, playerCar):
                alarm.play()
                bullet.remove(ebullets)
                all_sprites_list.remove(bullet)
                enemymissiles.remove(bullet)
                hearts = hearts - 1
                if hearts == 0:
                    lost()
                    carryOn = False


        for bullet in ebullets:
            if bullet.rect.y > SCREENHEIGHT:
                ebullets.remove(bullet)
                all_sprites_list.remove(bullet)
                enemymissiles.remove(bullet)


        # Drawing on Screen
        screen.fill(BLACK)

        # Now let's draw all the sprites in one go. (For now we only have 1 sprite!)
        all_sprites_list.draw(screen)
        screen.blit(font.render("lives :"+str(hearts), True, WHITE), (SCREENWIDTH - 135, 60))
        screen.blit(font.render("level: " + str(level+1), True, WHITE), (40, 60))
        screen.blit(font.render("extra gun :" + str(licz1), True, color1), (SCREENWIDTH - 135, 90))
        screen.blit(font.render("stealth :" + str(licz2), True, color2), (SCREENWIDTH - 135, 120))

        # Refresh Screen
        pygame.display.flip()

        if wrog == 20:
            carryOn = False
            nextlevel(level, hearts)

        zzz = zzz + 1
        if zzz >= strzal:
            zzz = 0
            yyy = 0


        # Number of frames per secong e.g. 60
        clock.tick(60)

        if carryOn == False:
            menu()

    pygame.quit()

print (menu())
