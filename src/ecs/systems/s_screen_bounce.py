import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_screen_bounce(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)

    c_transform: CTransform
    c_velocity: CVelocity
    c_surface: CSurface

    for entity, (c_transform, c_velocity, c_surface, c_enemy) in components:
        cuad_rect = CSurface.get_area_relative(c_surface.area, c_transform.pos)

        if cuad_rect.left < 0 or cuad_rect.right > screen_rect.width:
            c_velocity.vel.x *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_transform.pos.x = cuad_rect.x

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_velocity.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_transform.pos.y = cuad_rect.y
