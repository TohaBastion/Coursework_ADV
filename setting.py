import pygame
import os

pygame.init()

FILE_DIR = os.path.dirname(__file__)

# Зображення
BACKGROUND = pygame.image.load(os.path.join(FILE_DIR, 'ground_texture898.jpg'))
BLOCK_PLATFORM = '%s/pngegg.png' % FILE_DIR
CAR_IMAGE = '%s/pngwing.com.png' % FILE_DIR
FILE_PATH = '%s/map.txt' % FILE_DIR
MONSTER_IMAGE = '%s/zom.png' % FILE_DIR
BULLET_IMAGE = '%s/fire.png' % FILE_DIR
FLAG_IMAGE = '%s/flag.png' % FILE_DIR
with open(FILE_PATH, 'r') as f:
    level_map = [line.strip("\n") for line in f]

# Параметри екрану
TILE_SIZE = 40
SCREEN_WIDTH = TILE_SIZE * len(level_map[0])
SCREEN_HEIGHT = TILE_SIZE * len(level_map)

# Параметри тексту
font = pygame.font.Font(None, 120)
winner_text = font.render('YOU WIN', True, (0, 0, 255))
lose_text = font.render('YOU LOSE', True, (0, 0, 255))
