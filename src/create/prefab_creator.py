import math
import random

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_hunter_enemy import CTagHunterEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_shield import CTagShield
from src.engine.service_locator import ServiceLocator


def create_square(
        ecs_world: esper.World,
        size: pygame.Vector2,
        pos: pygame.Vector2,
        vel: pygame.Vector2,
        col: pygame.Color
) -> int:
    cuad_entity = ecs_world.create_entity()

    ecs_world.add_component(
        cuad_entity,
        CSurface(size, col)
    )
    ecs_world.add_component(
        cuad_entity,
        CTransform(pos)
    )
    ecs_world.add_component(
        cuad_entity,
        CVelocity(vel)
    )
    return cuad_entity


def create_sprite(ecs_world, post:  pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = ecs_world.create_entity()

    ecs_world.add_component(sprite_entity, CTransform(post))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))

    return sprite_entity


def create_enemy_square(
        ecs_world: esper.World,
        pos: pygame.Vector2,
        enemy: dict,
):
    enemy_surface = ServiceLocator.images_service.get(enemy['image'])

    velocity_range = random.randrange(enemy['velocity_min'], enemy['velocity_max'])
    velocity = pygame.Vector2(
        random.choice([-velocity_range, velocity_range]),
        random.choice([-velocity_range, velocity_range])
    )

    enemy_entity = create_sprite(ecs_world, pos, velocity, enemy_surface)
    ecs_world.add_component(enemy_entity, CTagEnemy())
    ecs_world.add_component(enemy_entity, CTagExplosion())

    ServiceLocator.sounds_service.play(enemy['sound'])


def create_hunter(ecs_world: esper.World, pos: pygame.Vector2, hunter: dict):
    hunter_surface = ServiceLocator.images_service.get(hunter['image'])

    size = hunter_surface.get_size()
    size = (size[0] / hunter['animations']["number_frames"], size[1])

    position = pygame.Vector2(
        pos.x + (size[0] / 2),
        pos.y - (size[1] / 2)
    )
    velocity = pygame.Vector2(0, 0)

    hunter_entity = create_sprite(ecs_world, position, velocity, hunter_surface)
    ecs_world.add_component(hunter_entity, CTagEnemy())
    ecs_world.add_component(hunter_entity, CTagHunterEnemy())
    ecs_world.add_component(hunter_entity, CAnimation(hunter['animations']))
    ecs_world.add_component(
        hunter_entity,
        CHunterState(
            hunter['velocity_chase'],
            hunter['velocity_return'],
            hunter['distance_start_chase'],
            hunter['distance_start_return'],
            pos.copy(),
            hunter['sound_chase']
        )
    )


def create_explosion(ecs_world: esper.World, pos: pygame.Vector2, explosion: dict):
    explosion_surface = ServiceLocator.images_service.get(explosion['image'])
    velocity = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(ecs_world, pos, velocity, explosion_surface)
    ecs_world.add_component(explosion_entity, CAnimation(explosion['animations']))
    ecs_world.add_component(explosion_entity, CTagExplosion())

    ServiceLocator.sounds_service.play(explosion['sound'])


def create_player_square(ecs_world: esper.World, player: dict, player_lvl_info: dict) -> int:
    player_surface = ServiceLocator.images_service.get(player['image'])

    size = player_surface.get_size()
    size = (size[0] / player['animations']["number_frames"], size[1])

    position = pygame.Vector2(
        player_lvl_info['position']['x'] - (size[0] / 2),
        player_lvl_info['position']['y'] - (size[1] / 2)
    )

    velocity = pygame.Vector2(0, 0)

    player_entity = create_sprite(ecs_world, position, velocity, player_surface)
    ecs_world.add_component(player_entity, CTagPlayer())
    ecs_world.add_component(player_entity, CAnimation(player['animations']))
    ecs_world.add_component(player_entity, CPlayerState())

    return player_entity


def create_bullet(
        ecs_world: esper.World,
        player_entity: int,
        bullet_info: dict
):
    bullet_surface = ServiceLocator.images_service.get(bullet_info['image'])
    bullet_size = bullet_surface.get_rect().size

    mouse_pos = pygame.mouse.get_pos()

    pl_t = ecs_world.component_for_entity(player_entity, CTransform)
    pl_pos = pl_t.pos

    bullet_init_pos = pygame.Vector2(
        pl_pos.x + (bullet_size[0] / 2),
        pl_pos.y + (bullet_size[1] / 2)
    )
    velocity = (mouse_pos - bullet_init_pos).normalize() * bullet_info['velocity']

    bullet_entity = create_sprite(ecs_world, bullet_init_pos, velocity, bullet_surface)
    ecs_world.add_component(bullet_entity, CTagBullet())

    ServiceLocator.sounds_service.play(bullet_info['sound'])


def create_enemy_spawner(ecs_world: esper.World, events):
    spawner_entity = ecs_world.create_entity()
    ecs_world.add_component(spawner_entity, CEnemySpawner(events))


def create_input_player(ecs_world: esper.World):
    input_left = ecs_world.create_entity()
    input_right = ecs_world.create_entity()
    input_up = ecs_world.create_entity()
    input_down = ecs_world.create_entity()
    input_fire = ecs_world.create_entity()
    input_pause = ecs_world.create_entity()
    input_ultimate_power = ecs_world.create_entity()

    ecs_world.add_component(input_pause, CInputCommand("PLAYER_PAUSE", pygame.K_p))
    ecs_world.add_component(input_left, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    ecs_world.add_component(input_right, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    ecs_world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    ecs_world.add_component(input_down, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    ecs_world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))
    ecs_world.add_component(input_ultimate_power, CInputCommand("PLAYER_ULTIMATE_POWER", pygame.BUTTON_RIGHT))


def create_pause_caption(ecs_world: esper.World, screen, pause_caption: dict) -> int:
    font = ServiceLocator.fonts_service.get(pause_caption['font'], pause_caption['size'])
    pause_entity = ecs_world.create_entity()

    color = pygame.Color(
        pause_caption['color']['r'],
        pause_caption['color']['g'],
        pause_caption['color']['b']
    )

    component_surface = CSurface.from_text(
        pause_caption['text'],
        font,
        color
    )

    text_size = component_surface.surface.get_size()
    position = pygame.Vector2(
        (screen.get_width() // 2) - (text_size[0] / 2),
        (screen.get_height() // 2) - (text_size[1] / 2)
    )

    ecs_world.add_component(pause_entity, CTransform(position))
    ecs_world.add_component(
        pause_entity,
        component_surface
    )

    return pause_entity


def create_how_to_play_caption(ecs_world: esper.World, screen: pygame.Surface, how_to_play_caption: dict):
    font = ServiceLocator.fonts_service.get(how_to_play_caption['font'], how_to_play_caption['size'])
    how_to_play_entity = ecs_world.create_entity()

    color = pygame.Color(
        how_to_play_caption['color']['r'],
        how_to_play_caption['color']['g'],
        how_to_play_caption['color']['b']
    )

    component_surface = CSurface.from_text(
        how_to_play_caption['text'],
        font,
        color
    )

    screen_rect = screen.get_rect()
    position = pygame.Vector2(
        screen_rect.x + 10,
        screen_rect.y + 10
    )

    ecs_world.add_component(how_to_play_entity, CTransform(position))
    ecs_world.add_component(
        how_to_play_entity,
        component_surface
    )


def create_ultimate_power_caption(
        ecs_world: esper.World,
        screen: pygame.Surface,
        ultimate_power_caption: dict,
        counter_ultimate_power_caption: dict
) -> int:
    ultimate_power_font = ServiceLocator.fonts_service.get(
        ultimate_power_caption['font'],
        ultimate_power_caption['size']
    )
    counter_ultimate_power_font = ServiceLocator.fonts_service.get(
        counter_ultimate_power_caption['font'],
        counter_ultimate_power_caption['size']
    )

    ultimate_power_entity = ecs_world.create_entity()
    counter_ultimate_power_entity = ecs_world.create_entity()

    ultimate_power_component_surface = CSurface.from_text(
        ultimate_power_caption['text'],
        ultimate_power_font,
        pygame.Color(
            ultimate_power_caption['color']['r'],
            ultimate_power_caption['color']['g'],
            ultimate_power_caption['color']['b']
        )
    )

    counter_ultimate_power_component_surface = CSurface.from_text(
        counter_ultimate_power_caption['text'],
        counter_ultimate_power_font,
        pygame.Color(
            counter_ultimate_power_caption['color']['r'],
            counter_ultimate_power_caption['color']['g'],
            counter_ultimate_power_caption['color']['b']
        )
    )

    screen_rect = screen.get_rect()
    ultimate_power_position = pygame.Vector2(
        screen_rect.x + 10,
        screen_rect.height - ultimate_power_component_surface.surface.get_height() - counter_ultimate_power_component_surface.surface.get_height() - 10,
    )
    counter_ultimate_power_position = pygame.Vector2(
        screen_rect.x + 10,
        screen_rect.height - counter_ultimate_power_component_surface.surface.get_height() - 10
    )

    ecs_world.add_component(ultimate_power_entity, CTransform(ultimate_power_position))
    ecs_world.add_component(
        ultimate_power_entity,
        ultimate_power_component_surface
    )

    ecs_world.add_component(counter_ultimate_power_entity, CTransform(counter_ultimate_power_position))
    ecs_world.add_component(
        counter_ultimate_power_entity,
        counter_ultimate_power_component_surface
    )

    return counter_ultimate_power_entity


def create_player_shield(ecs_world: esper.World, player_entity: int, shield: dict, delta_time: int):
    shield_surface = ServiceLocator.images_service.get(shield['image'])
    shield_size = shield_surface.get_rect().size

    pl_t = ecs_world.component_for_entity(player_entity, CTransform)
    pl_s = ecs_world.component_for_entity(player_entity, CSurface)

    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)
    pl_size = pl_rect.size
    pl_pos = pl_t.pos

    shield_init_pos = pygame.Vector2(
        pl_pos.x + pl_size[0] // 2 - shield_size[0] // 2,
        pl_pos.y + pl_size[1] // 2 - shield_size[1] // 2
    )
    velocity = pygame.Vector2(0, 0)

    shield_entity = create_sprite(ecs_world, shield_init_pos, velocity, shield_surface)
    ecs_world.add_component(shield_entity, CTagShield(delta_time, shield['distance']))