import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_shield import CTagShield


def system_collision_shield_enemy(world: esper.World, explosion_cfg: dict):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    shield_components = world.get_components(CSurface, CTransform, CTagShield)

    s_t: CTransform
    c_tag_shield: CTagShield

    for shield_entity, (s_s, s_t, c_tag_shield) in shield_components:

        for enemy_entity, (e_s, e_t, _) in enemy_components:
            if c_tag_shield.distance >= s_t.pos.distance_to(e_t.pos):
                world.delete_entity(enemy_entity)
                create_explosion(world, e_t.pos, explosion_cfg)
