import pygame
import os

# Base path for assets
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

def load_image(filename):
    path = os.path.join(IMAGES_DIR, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        print(f"Resources: Successfully loaded image: {filename}")
        return image
    except pygame.error as e:
        print(f"Resources: Error loading image {filename} from {path}: {e}")
        return None

def load_animation_frames(sprite_sheet_filename, frame_width, frame_height):
    frames = []
    sheet = load_image(sprite_sheet_filename)
    if sheet:
        for i in range(sheet.get_width() // frame_width):
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
    else:
        print(f"Resources: Could not load sprite sheet: {sprite_sheet_filename}")
    return frames

def load_sound(filename):
    path = os.path.join(SOUNDS_DIR, filename)
    try:
        sound = pygame.mixer.Sound(path)
        print(f"Resources: Successfully loaded sound: {filename}")
        return sound
    except pygame.error as e:
        print(f"Resources: Error loading sound {filename} from {path}: {e}")
        return None