import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_shield import CTagShield


def system_player_shield(world: esper.World, player_entity: int):
    components = world.get_components(CSurface, CTransform, CTagShield)

    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    pl_size = pl_rect.size

    c_s: CSurface
    c_t: CTransform

    for enemy_entity, (c_s, c_t, _) in components:
        shield_size = c_s.surface.get_size()
        c_t.pos.x = pl_t.pos.x + pl_size[0] // 2 - shield_size[0] // 2
        c_t.pos.y = pl_t.pos.y + pl_size[1] // 2 - shield_size[1] // 2

