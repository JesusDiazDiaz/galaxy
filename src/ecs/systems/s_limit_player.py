import pygame

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_limit_player(world: esper.World, player_entity: int, screen: pygame.Surface):
    screen_rect = screen.get_rect()

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    if not screen_rect.contains(pl_rect):
        pl_rect.clamp_ip(screen_rect)
        pl_t.pos.xy = pl_rect.topleft
