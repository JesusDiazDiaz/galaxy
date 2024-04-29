import pygame

import esper

from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_update_shield_counter(
        ecs_world: esper.World,
        entity: int,
        shield_info: dict,
        time_counter: float,
        last_shield_created_at: float,
        counter_ultimate_power_info: dict
):
    font = ServiceLocator.fonts_service.get(
        counter_ultimate_power_info['font'],
        counter_ultimate_power_info['size']
    )
    total_cooldown = shield_info['cooldown'] + shield_info['max_time_used']
    total = total_cooldown + last_shield_created_at
    percentage = _get_percentage(total, time_counter, total_cooldown)

    color_info = counter_ultimate_power_info['color_error'] if percentage < 100 else counter_ultimate_power_info['color']

    new_surface = CSurface.from_text(
        f"{percentage}%",
        font,
        pygame.Color(
            color_info['r'],
            color_info['g'],
            color_info['b']
        )
    )
    ecs_world.remove_component(entity, CSurface)
    ecs_world.add_component(entity, new_surface)


def _get_percentage(total, time_counter: float, total_cooldown: float) -> int:
    if total < time_counter:
        return 100
    current = (total - time_counter)
    percentage = (current * 100) / total_cooldown
    percentage_reusable = 100 - percentage
    return int(percentage_reusable)
