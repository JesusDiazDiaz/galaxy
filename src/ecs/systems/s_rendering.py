import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(word: esper.World, screen: pygame.Surface):
    components = word.get_components(CTransform, CSurface)

    c_transform: CTransform
    c_surface: CSurface

    for entity, (c_transform, c_surface) in components:
        screen.blit(c_surface.surface, c_transform.pos, area=c_surface.area)
