import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_limit_bullet(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CSurface, CTransform, CTagBullet)

    c_s: CSurface
    c_t: CTransform

    for bullet_entity, (c_s, c_t, _) in components:
        bullet_rect = c_s.surface.get_rect(topleft=c_t.pos)

        if not screen_rect.contains(bullet_rect):
            world.delete_entity(bullet_entity)
