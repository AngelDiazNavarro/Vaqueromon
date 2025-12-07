import pygame
from os.path import join 
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720 

COLORS = {
    'black': '#000000',
    'red': '#ee1a0f',
    'gray': 'gray',
    'white': '#ffffff',
}

# Vaqueromon programming-themed monsters
MONSTER_DATA = {
    'Android': {'element': 'plant',  'health': 110},
    'Clippy':  {'element': 'normal', 'health': 80},
    'DMan':    {'element': 'fire',   'health': 90},
    'Duke':    {'element': 'fire',   'health': 120},
    'Go':      {'element': 'water',  'health': 130},
    'HolyC':   {'element': 'plant',  'health': 100},
    'Keith':   {'element': 'normal', 'health': 95},
}

ABILITIES_DATA = {
    'scratch': {'damage': 20,  'element': 'normal', 'animation': 'scratch'},
    'spark':   {'damage': 35,  'element': 'fire',   'animation': 'fire'},
    'nuke':    {'damage': 50,  'element': 'fire',   'animation': 'explosion'},
    'splash':  {'damage': 30,  'element': 'water',  'animation': 'splash'},
    'shards':  {'damage': 50,  'element': 'water',  'animation': 'ice'},
    'spiral':  {'damage': 40,  'element': 'plant',  'animation': 'green'},
}

ELEMENT_DATA = {
    'fire':   {'water': 0.5, 'plant': 2,   'fire': 1,   'normal': 1},
    'water':  {'water': 1,   'plant': 0.5, 'fire': 2,   'normal': 1},
    'plant':  {'water': 2,   'plant': 1,   'fire': 0.5, 'normal': 1},
    'normal': {'water': 1,   'plant': 1,   'fire': 1,   'normal': 1},
}
