import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface: pygame.surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surface = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.Color):
        text_surface = font.render(text, True, color)
        c_surf = cls.from_surface(text_surface)
        return c_surf

    @staticmethod
    def get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2):
        rect = area.copy()
        rect.topleft = pos_topleft.copy()
        return rect
