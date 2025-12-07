import sys
import os
import pygame
from os import walk

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', relative_path)

def folder_importer(root_folder, subfolder):
    folder = resource_path(f"{root_folder}/{subfolder}")
    data = {}
    for path, _, files in walk(folder):
        for file in files:
            if file.endswith(('.png', '.jpg')):
                full_path = os.path.join(path, file)
                key = file.split('.')[0]
                data[key] = pygame.image.load(full_path).convert_alpha()
    return data

def tile_importer(size, root_folder, subfolder):
    folder = resource_path(f"{root_folder}/{subfolder}")
    tiles = {}
    for path, _, files in walk(folder):
        for file in files:
            if file.endswith('.png'):
                full_path = os.path.join(path, file)
                sheet = pygame.image.load(full_path).convert_alpha()
                name = file.split('.')[0]
                tiles[name] = []
                w, h = sheet.get_size()
                for y in range(0, h, size):
                    for x in range(0, w, size):
                        tile = sheet.subsurface((x, y, size, size))
                        tiles[name].append(tile)
    return tiles

def audio_importer(folder):
    folder = resource_path(folder)
    audio = {}
    for path, _, files in walk(folder):
        for file in files:
            if file.endswith(('.wav', '.mp3', '.ogg')):
                full_path = os.path.join(path, file)
                key = file.split('.')[0]
                audio[key] = pygame.mixer.Sound(full_path)
    return audio
