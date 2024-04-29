import esper

from src.ecs.components.tags.c_tag_shield import CTagShield


def system_shield_active(world: esper.World, delta_time: int, shield_info: dict):
    components = world.get_components(CTagShield)

    c_tag_shield: CTagShield

    for entity, (c_tag_shield, ) in components:
        total = delta_time - c_tag_shield.shield_start_at
        if total >= shield_info['max_time_used']:
            world.delete_entity(entity)
