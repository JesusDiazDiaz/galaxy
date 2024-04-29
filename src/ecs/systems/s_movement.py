import pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(word: esper.World, delta_time: float):
    components = word.get_components(CTransform, CVelocity)

    c_transform: CTransform
    c_velocity: CVelocity

    for entity, (c_transform, c_velocity) in components:
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
