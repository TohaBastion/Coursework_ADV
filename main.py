"""Основний файл, що містить логіку проведення гри"""
import random
from setting import *
from classes import Player, Wall, Bullet, Monster, Flag

# Ініціалізація Pygame
pygame.init()

background = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombi")


# Завантаження рівня
def load_level(level_map):
    """Функція завантаження рівня"""
    window.blit(background, (0, 0))
    walls = pygame.sprite.Group()
    player = None
    flag = None

    for y, row in enumerate(level_map):
        for x, symbol in enumerate(row):
            if symbol == 'x':
                walls.add(Wall(x, y))
            elif symbol == 'f':
                flag = Flag(x, y)
            elif symbol == 'P':
                player = Player(CAR_IMAGE, x, y, 35, TILE_SIZE, 2)
    return walls, player, flag


# Головний цикл гри та його змінні та групування
walls, player, flag = load_level(level_map)
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
clock = pygame.time.Clock()

running = True
winner = False
lose = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(
                    player.rect.centerx,
                    player.rect.centery,
                    player.angle
                )
                bullets.add(bullet)

    player.update()
    bullets.update()
    zombies.update()
    player.collide(walls)
    for bullet in bullets.sprites():
        bullet.collide(walls)

    if random.random() < 0.02:
        zombi = Monster()
        zombies.add(zombi)

    for zombi in zombies.sprites():
        zombi.collide(walls)

    pygame.sprite.groupcollide(bullets, zombies, True, True)
    if pygame.sprite.spritecollideany(player, zombies):
        player.kill()
        lose = True
        running = False

    # Очистка екрану
    window.blit(background, (0, 0))

    # Малювання об'єктів
    bullets.draw(window)
    walls.draw(window)
    zombies.draw(window)
    window.blit(flag.image, flag.rect)
    window.blit(player.image, player.rect)
    if pygame.sprite.spritecollideany(flag, bullets):
        winner = True
        running = False

    clock.tick(60)
    pygame.display.flip()

# Цикл відповідальний за події при перемоі
cors = (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
        SCREEN_HEIGHT // 2 - winner_text.get_height() // 2)
while winner:
    window.blit(background, (0, 0))
    window.blit(winner_text, cors)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            winner = False
    pygame.display.flip()

# Цикл відповідальний за події при програші
cors1 = (SCREEN_WIDTH // 2 - lose_text.get_width() // 2,
         SCREEN_HEIGHT // 2 - lose_text.get_height() // 2)
while lose:
    window.blit(background, (0, 0))
    window.blit(lose_text, cors1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lose = False
    pygame.display.flip()
