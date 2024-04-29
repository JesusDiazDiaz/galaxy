import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_hunter_enemy import CTagHunterEnemy


def system_collision_bullet_enemy(world: esper.World, explosion_cfg: dict):
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)

    for bullet_entity, (b_s, b_t, _) in bullet_components:
        bullet_rect = CSurface.get_area_relative(b_s.area, b_t.pos)

        for enemy_entity, (e_s, e_t, _) in enemy_components:
            enemy_rect = CSurface.get_area_relative(e_s.area, e_t.pos)

            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)

                create_explosion(world, e_t.pos, explosion_cfg)
