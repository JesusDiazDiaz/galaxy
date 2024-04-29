import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_remove_explosion(world: esper.World):
    c_a: CAnimation

    for entity, (c_a, _) in world.get_components(CAnimation, CTagExplosion):
        if c_a.current_frame >= c_a.animations_list[c_a.current_animation].end:
            world.delete_entity(entity)
