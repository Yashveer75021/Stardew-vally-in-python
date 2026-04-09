from pygame import Vector2

# game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
TILE_SIZE = 64

#overlay settings 
OVERLAY_POSITION = {
    'tool': (40, SCREEN_HEIGHT - TILE_SIZE - 15),
    'seed': (70, SCREEN_HEIGHT - TILE_SIZE - 5),
}

PLAYER_TOOL_OFFEST = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main' : 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10

}

APPLE_POS = {
    'Small' : [(18,17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large' : [(17, 17), (17, 18), (18, 16), (18, 19), (19, 16), (19, 19)]
}

GROWTH_SPEED = {
    'corn' : 0.5,
    'tomato' : 0.1,
    'potato' : 0.1
}

SALE_PRICE = {
    'wood' : 2,
    'stone' : 3,
    'apple' : 5,
    'corn' : 10,
    'tomato' : 15
}

PURCHASE_PRICE = {
    'wood' : 2,
    'stone' : 3,
    'apple seed' : 1,   
    'corn seed' : 2,
    'tomato seed' : 3
}