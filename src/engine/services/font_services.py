import pygame


class FontsService:
    def __init__(self):
        self.fonts = {}

    def get(self, path: str, size: int):
        key = (path, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(path, size)

        return self.fonts[key]
