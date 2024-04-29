import random

import pygame

import esper
from src.create.prefab_creator import create_enemy_square, create_hunter
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_enemy_spawner(world: esper.World, time_counter: float, enemies: dict):
    for entity, c_enemy_spawner in world.get_component(CEnemySpawner):
        for i, event in enumerate(c_enemy_spawner.enemy_spawn_events):
            if event['time'] <= time_counter and not c_enemy_spawner.event_triggered[i]:
                position = pygame.Vector2(event['position']['x'], event['position']['y'])
                enemy = enemies[event['enemy_type']]

                c_enemy_spawner.event_triggered[i] = True

                if event['enemy_type'] == 'Hunter':
                    create_hunter(world, position, enemy)
                else:
                    create_enemy_square(world, position, enemy)
