import pygame
import os
import sys


def load_image(file_name, transparent_color=None):
    full_path = os.path.join('data', file_name)
    try:
        img = pygame.image.load(full_path)
    except pygame.error as e:
        print(f"Ошибка загрузки изображения: {file_name}")
        raise SystemExit(e)
    img = img.convert_alpha()
    if transparent_color is not None:
        if transparent_color == -1:
            transparent_color = img.get_at((0, 0))
        img.set_colorkey(transparent_color)
    return img


pygame.init()
screen_size = width, height = 500, 500
screen = pygame.display.set_mode(screen_size)

tiles = pygame.sprite.Group()
players = pygame.sprite.Group()

tile_images = {
    'wall': load_image('box.png'),
    'grass': load_image('grass.png')
}

player_img = load_image('mar.png')

tile_size = 50


def quit_game():
    pygame.quit()
    sys.exit()


def load_level(file_name):
    file_path = os.path.join('data', file_name)
    if not os.path.exists(file_path):
        print(f"Ошибка: файл уровня '{file_name}' не найден.")
        quit_game()

    with open(file_path, 'r') as level_file:
        level_data = [line.strip() for line in level_file]
    max_width = max(map(len, level_data))
    return [list(line.ljust(max_width, '.')) for line in level_data]


def generate_level(level_data):
    new_player = None
    for y in range(len(level_data)):
        for x in range(len(level_data[y])):
            tile = level_data[y][x]
            if tile == '.':
                Tile('grass', x, y)
            elif tile == '#':
                Tile('wall', x, y)
            elif tile == '@':
                Tile('grass', x, y)
                new_player = Player(x, y)
                level_data[y][x] = '.'
    return new_player


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, x, y):
        super().__init__(tiles)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size, y * tile_size)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(players)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * tile_size + 15, y * tile_size + 5)
        self.position = (x, y)

    def move(self, direction):
        x, y = self.position
        if direction == 'up' and y > 0 and level_map[y - 1][x] == '.':
            self.position = (x, y - 1)
        elif direction == 'down' and y < len(level_map) - 1 and level_map[y + 1][x] == '.':
            self.position = (x, y + 1)
        elif direction == 'left' and x > 0 and level_map[y][x - 1] == '.':
            self.position = (x - 1, y)
        elif direction == 'right' and x < len(level_map[y]) - 1 and level_map[y][x + 1] == '.':
            self.position = (x + 1, y)
        self.rect.topleft = (self.position[0] * tile_size + 15, self.position[1] * tile_size + 5)


def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    hero.move('up')
                elif event.key == pygame.K_DOWN:
                    hero.move('down')
                elif event.key == pygame.K_LEFT:
                    hero.move('left')
                elif event.key == pygame.K_RIGHT:
                    hero.move('right')

        screen.fill(pygame.Color('white'))
        tiles.draw(screen)
        players.draw(screen)
        pygame.display.flip()


def show_intro_screen():
    intro_text = ["Добро пожаловать в игру!", '', "Используйте стрелки для перемещения."]
    background = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 30)
    y_position = 50
    for line in intro_text:
        rendered_text = font.render(line, True, pygame.Color('black'))
        text_rect = rendered_text.get_rect()
        y_position += 10
        text_rect.top = y_position
        text_rect.x = 10
        y_position += text_rect.height
        screen.blit(rendered_text, text_rect)

    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                waiting_for_input = False


if __name__ == '__main__':
    pygame.display.set_caption('Platformer Game')
    show_intro_screen()
    level_filename = input("Введите имя файла уровня (например, 'levelex.txt'): ")
    level_map = load_level(level_filename)
    hero = generate_level(level_map)
    game_loop()
    pygame.quit()
