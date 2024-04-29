import pygame

import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator


def system_hunter_state(world: esper.World, player_entity: int):
    hunter_components = world.get_components(CTransform, CVelocity, CAnimation, CHunterState)
    player_transform = world.component_for_entity(player_entity, CTransform)

    c_v: CVelocity
    c_a: CAnimation
    c_pst: CHunterState

    for _, (c_t, c_v, c_a, c_hst) in hunter_components:
        if c_hst.state == HunterState.IDLE:
            _do_idle_state(c_t, c_a, c_hst, player_transform.pos)
        elif c_hst.state == HunterState.CHASE:
            _do_chase_state(c_t, c_v, c_a, c_hst, player_transform.pos)
        elif c_hst.state == HunterState.RETURN:
            _do_return_state(c_t, c_v, c_a, c_hst)


def _set_animation(c_a: CAnimation, num_animation):
    if c_a.current_animation != num_animation:
        c_a.current_animation = num_animation
        c_a.current_frame = c_a.animations_list[c_a.current_animation].start
        c_a.current_animation_time = 0


def _do_idle_state(
        c_t: CTransform,
        c_a: CAnimation,
        c_hst: CHunterState,
        player_position: pygame.Vector2
):
    _set_animation(c_a, 1)

    if c_hst.distance_start_chase >= c_t.pos.distance_to(player_position):
        ServiceLocator.sounds_service.play(c_hst.sound_chase)
        c_hst.state = HunterState.CHASE


def _do_chase_state(
        c_t: CTransform,
        c_v: CVelocity,
        c_a: CAnimation,
        c_hst: CHunterState,
        player_position: pygame.Vector2
):
    _set_animation(c_a, 0)

    if c_t.pos.distance_to(c_hst.initial_position) >= float(c_hst.distance_start_return):
        c_hst.state = HunterState.RETURN
    else:
        c_v.vel = (player_position - c_t.pos).normalize() * c_hst.velocity_chase


def _do_return_state(
        c_t: CTransform,
        c_v: CVelocity,
        c_a: CAnimation,
        c_hst: CHunterState
):
    _set_animation(c_a, 0)

    if c_t.pos.distance_to(c_hst.initial_position) < 1.0:
        c_t.pos = c_hst.initial_position.copy()
        c_v.vel = pygame.Vector2(0, 0)
        c_hst.state = HunterState.IDLE
    else:
        c_v.vel = (c_hst.initial_position - c_t.pos).normalize() * c_hst.velocity_return
