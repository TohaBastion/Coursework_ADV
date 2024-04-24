import random
from setting import *


class Wall(pygame.sprite.Sprite):
    """Клас блоків лабіринту"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load(BLOCK_PLATFORM)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class GameSprite(pygame.sprite.Sprite):
    """Абстрактний клас"""
    def __init__(self, image, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.angle = 0


    def update(self):
        pass

    def collide(self):
        pass

    def rotate_to(self, angle):
        rotate = (360 - self.angle + angle)
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, rotate)


class Player(GameSprite):
    """Клас основного гравця"""
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.rotate_to(90)
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.rotate_to(270)
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.rotate_to(0)
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.rotate_to(180)


    def collide(self, blocks):
        for wall in blocks:
            if pygame.sprite.collide_rect(self, wall):
                if isinstance(wall, Wall):
                    if self.angle == 90:
                        self.rect.left = wall.rect.right
                    elif self.angle == 270:
                        self.rect.right = wall.rect.left
                    elif self.angle == 0:
                        self.rect.top = wall.rect.bottom
                    elif self.angle == 180:
                        self.rect.bottom = wall.rect.top


class Monster(pygame.sprite.Sprite):
    """Клас для зомбі"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image = pygame.image.load(MONSTER_IMAGE)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=random.choice([(40, 40), (720, 80)]))
        self.speed = 2
        self.angle = random.choice([0, 180, 90, 270])


    def update(self):
        """Функція руху зомбі"""
        if self.angle == 0:
            self.rect.y -= self.speed
        elif self.angle == 180:
            self.rect.y += self.speed
        elif self.angle == 270:
            self.rect.x += self.speed
        elif self.angle == 90:
            self.rect.x -= self.speed



    def collide(self, blocks):
        """Функція обходу перешкод"""
        for wall in blocks:
            if pygame.sprite.collide_rect(self, wall):
                if isinstance(wall, Wall):
                    if self.angle == 90:
                        self.rect.left = wall.rect.right
                        self.angle = random.choice([0, 180, 270])
                    elif self.angle == 270:
                        self.rect.right = wall.rect.left
                        self.angle = random.choice([0, 180, 90])
                    elif self.angle == 0:
                        self.rect.top = wall.rect.bottom
                        self.angle = random.choice([90, 180, 270])
                    elif self.angle == 180:
                        self.angle = random.choice([0, 90, 270])
                        self.rect.bottom = wall.rect.top

class Flag(pygame.sprite.Sprite):
    """Клас виграшного флагу що треба знищити"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image = pygame.image.load(FLAG_IMAGE)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class Bullet(pygame.sprite.Sprite):
    """Клас снаряду"""
    def __init__(self, start_x, start_y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image = pygame.image.load(BULLET_IMAGE)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.speed = 10
        self.angle = angle

    def update(self):
        """Функція напряму постріла"""
        if self.angle == 0:
            self.rect.y -= self.speed
        elif self.angle == 180:
            self.rect.y += self.speed
        elif self.angle == 270:
            self.rect.x += self.speed
        elif self.angle == 90:
            self.rect.x -= self.speed


    def collide(self, blocks):
        """Функція знищщення куль при потраплянні в стіни"""
        for _ in blocks:
            if pygame.sprite.collide_rect(self, _):
                if isinstance(_, Wall):
                    self.kill()
