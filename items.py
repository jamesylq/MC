import pygame

IDs = {
    '-1': {
        'name': 'air',
        'texture': pygame.image.load('MCResources/Air.png'),
        'itemtexture': None
    },
    '0': {
        'name': 'bedrock',
        'texture': pygame.image.load('MCResources/Bedrock.png'),
        'itemtexture': None
    },
    '1': {
        'name': 'grass_block',
        'texture': pygame.image.load('MCResources/Grass.png'),
        'itemtexture': pygame.image.load('MCResources/Grass_item.png')
    },
    '2': {
        'name': 'stone',
        'texture': pygame.image.load('MCResources/Stone.png'),
        'itemtexture': pygame.image.load('MCResources/Stone_item.png')
    },
    '3': {
        'name': 'dirt',
        'texture': pygame.image.load('MCResources/Dirt.png'),
        'itemtexture': pygame.image.load('MCResources/Dirt_item.png')
    },
    '4': {
        'name': 'iron_ore',
        'texture': pygame.image.load('MCResources/Iron_Ore.png'),
        'itemtexture': pygame.image.load('MCResources/Iron_Ore_Item.png')
    }
}
