import pygame

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
tileset_img = None

def load_asset():
    load_assets = {
        'tileset_img': pygame.image.load("assets/spritesheet.png").convert_alpha(),
        'point_img' : pygame.image.load("assets/point.png").convert_alpha(),
        'big_point_img' : pygame.image.load("assets/big_point.png").convert_alpha(),
        'blank_img' : pygame.image.load("assets/blank.png").convert_alpha(),
    }
    return load_assets

    


def slice_tileset(image, xrange, yrange, tile_width, tile_height):
    tiles = []
    for y in range(yrange[0], yrange[1], tile_height):
        for x in range(xrange[0], xrange[1], tile_width):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            tile = image.subsurface(rect)
            tiles.append(tile)
    return tiles


def rotate_tile(tile, angle):
    """Rotate the tile by a specific angle."""
    return pygame.transform.rotate(tile, angle)

def draw_map(screen, map_data, tile_dict, tile_size=16):
    load_assets = load_asset()
    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            tile = tile_dict(cell, load_assets)
            #print(cell, tile)
            if tile:
                if cell in ['7','8']:
                    if map_data[y+1][x] == '1':
                        tile = rotate_tile(tile, 270)
                    elif map_data[y-1][x] == '1':
                        tile = rotate_tile(tile, 90)
                    else:
                        tile = rotate_tile(tile, 180)
                    if cell == '7' or map_data[y+1][x+1] == '+':
                        tile = rotate_tile(tile, 180)
                elif cell == '2':
                     for dx in [-1, 1]:
                        for dy in [-1, 1]:
                            if map_data[y + dy][x + dx] in ['3','X','9']:
                                if (dx,dy) == (-1, 1):
                                    tile = pygame.transform.rotate(tile, 270 )
                                elif (dx,dy) == (-1, -1):
                                    tile =  pygame.transform.rotate(tile, 180)
                                elif (dx,dy) == (1, -1):
                                    tile =  pygame.transform.rotate(tile, 90)
                elif cell in ['0', '4', '6', '9']:
                    for dx in [-1, 1]:
                        for dy in [-1, 1]:
                            if (map_data[y + dy][x + dx] in ['+', 'n', 'P'] and cell != '4') or (map_data[y + dy][x + dx] == 'X' and cell == '4'):
                                if (dx == -dy):
                                    tile = pygame.transform.rotate(tile, 90 * dx)
                                elif (dx == -1):
                                    tile =  pygame.transform.rotate(tile, 180)
                    if (cell in ['6']):
                        tile = pygame.transform.rotate(tile, 180)
                elif cell in ['1','3', '5']:
                    if map_data[y][x+1] in '.+|Ppn-abcde':
                        tile = rotate_tile(tile, 90)
                    elif map_data[y][x-1] in '.+|Ppn-:abcde':
                        tile = rotate_tile(tile, 270)
                    elif map_data[y-1][x] in  '.+|Ppn-abcde':
                        tile = rotate_tile(tile, 180)
                    if (cell in ['3','5']):
                        tile = rotate_tile(tile, 180)
                elif cell == '9':
                    if (map_data[y - 1][x] >='0' and map_data[y - 1][x] <='9') or (map_data[y + 1][x] >='0' and map_data[y + 1][x] <='9'):
                            tile =  pygame.transform.rotate(tile, 90)
                            if (map_data[y][x+1] not in ['.', '+', '|', 'p']):
                                tile = pygame.transform.rotate(tile, 180)
                    else:
                        if (map_data[y+1][x] not in ['.', '+', '|', 'p']):
                                tile = pygame.transform.rotate(tile, 180)
                tile = pygame.transform.scale(tile, (tile_size, tile_size))
                screen.blit(tile, (x * tile_size, y * tile_size))

def redraw_map(screen, map_data, tile_dict, tile_size=16):
    load_assets = load_asset()

    for y, row in enumerate(map_data):
        for x, cell in enumerate(row):
            tile = tile_dict(cell, load_assets)
            #print(cell, tile)
            if tile:
                tile = pygame.transform.scale(tile, (tile_size, tile_size))
                screen.blit(tile, (x * tile_size, y * tile_size))
    

def tile_dict(char, load_assets):
    global tileset_img
    if tileset_img ==None:
        tileset_img = load_assets['tileset_img']
    if char >= '0' and char <= '9':
        tiles = slice_tileset(tileset_img,(176 + 16, 352), (0,  16), 16, 16)  # or 8x8, 32x32 depending on your asset
        return tiles[int(char)]
    if char == '.' or char== ',' or char == '+':
        return load_assets['point_img']
    if char == 'p' or char =='P':
        return load_assets['big_point_img']
    
    return None

def tile_dict_2(char, load_assets):
    
    if char == '.' or char==',' or char == '+':
        return load_assets['point_img']
    if char == 'p' or char =='P':
        return load_assets['big_point_img']
    if char in "-=n|" or (char >= 'a' and char <= 'e'):
        return load_assets['blank_img']
    
    return None

def tile_dict_3(char, load_assets):
    if char in ".,+Pp|n-abcde=":
        return load_assets['blank_img']
    if char != 'X' and char <'0' and char > '9':
        return load_assets['blank_img']
    
    return None

def draw_complex_map(screen, game_map):
    
    draw_map(screen, game_map, tile_dict)

def redraw(screen, game_map):
    redraw_map(screen, game_map, tile_dict_2)

def redraw_demo(screen, game_map):
    redraw_map(screen, game_map, tile_dict_3)

    