import asyncio
import json
import pygame

import esper
from src.create.prefab_creator import create_player_square, create_enemy_spawner, create_input_player, \
    create_bullet, create_pause_caption, create_how_to_play_caption, create_ultimate_power_caption, create_player_shield
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_shield_enemy import system_collision_shield_enemy
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_limit_bullet import system_limit_bullet
from src.ecs.systems.s_limit_player import system_limit_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_shield import system_player_shield
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_remove_explosion import system_remove_explosion
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_shield_active import system_shield_active
from src.ecs.systems.s_update_shield_counter import system_update_shield_counter
from src.ecs.systems.system_enemy_spawner import system_enemy_spawner


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()

        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg['size']['w'], self.window_cfg['size']['h']),
        )
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.is_paused = False
        self.frame_rate = self.window_cfg['framerate']
        self.delta_time = 0
        self.time_counter = 0

        self.last_shield_created_at = -999999999.9

        self.shots = 0
        self.num_bullets = 0

        self.ecs_world = esper.World()

    def _load_config_files(self):
        with open("assets/week3/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)

        with open("assets/week3/cfg/level_01.json", encoding="utf-8") as level_file:
            self.level_cfg = json.load(level_file)

        with open("assets/week4/cfg/enemies.json", encoding="utf-8") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)

        with open("assets/week3/cfg/player.json", encoding="utf-8") as player_file:
            self.player_cfg = json.load(player_file)

        with open("assets/week4/cfg/bullet.json", encoding="utf-8") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)

        with open("assets/week4/cfg/explosion.json", encoding="utf-8") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)

        with open("assets/cfg/interfaces.json", encoding="utf-8") as interfaces_file:
            self.interfaces_cfg = json.load(interfaces_file)

        with open("assets/cfg/shield.json", encoding="utf-8") as shield_file:
            self.shield_cfg = json.load(shield_file)

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            if not self.is_paused:
                self._update()
            self._draw()

            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        create_how_to_play_caption(self.ecs_world, self.screen, self.interfaces_cfg['how_to_play_caption'])
        self.shield_counter_entity = create_ultimate_power_caption(
            self.ecs_world,
            self.screen,
            self.interfaces_cfg['ultimate_power_caption'],
            self.interfaces_cfg['counter_ultimate_power_caption']
        )
        self._player_entity = create_player_square(self.ecs_world, self.player_cfg, self.level_cfg['player_spawn'])
        self._player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)

        create_enemy_spawner(self.ecs_world, self.level_cfg['enemy_spawn_events'])
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.frame_rate)
        self.delta_time = self.clock.get_time() / 1000.0

        self.time_counter += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)

            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_enemy_spawner(self.ecs_world, self.time_counter, self.enemies_cfg)
        system_movement(self.ecs_world, self.delta_time)
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world, self._player_entity)
        system_screen_bounce(self.ecs_world, self.screen)

        system_limit_bullet(self.ecs_world, self.screen)
        system_limit_player(self.ecs_world, self._player_entity, self.screen)
        system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.level_cfg, self.explosion_cfg)
        system_player_shield(self.ecs_world, self._player_entity)
        system_shield_active(self.ecs_world, self.time_counter, self.shield_cfg)
        system_collision_shield_enemy(self.ecs_world, self.explosion_cfg)
        system_update_shield_counter(
            self.ecs_world,
            self.shield_counter_entity,
            self.shield_cfg,
            self.time_counter,
            self.last_shield_created_at,
            self.interfaces_cfg['counter_ultimate_power_caption']
        )
        system_animation(self.ecs_world, self.delta_time)
        system_remove_explosion(self.ecs_world)

        self.num_bullets = len(self.ecs_world.get_component(CTagBullet))
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(
            (
                self.window_cfg['bg_color']['r'],
                self.window_cfg['bg_color']['g'],
                self.window_cfg['bg_color']['b']
            )
        )

        system_rendering(self.ecs_world, self.screen)

        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()

    def _do_action(self, c_input: CInputCommand):
        print(f"Doing action: {c_input.name} {str(c_input.phase)}")

        if c_input.name == "PLAYER_PAUSE":
            if c_input.phase == CommandPhase.START:
                if self.is_paused:
                    self.ecs_world.delete_entity(self.pause_entity)
                else:
                    self.pause_entity = create_pause_caption(
                        self.ecs_world,
                        self.screen,
                        self.interfaces_cfg['pause_caption']
                    )
                self.is_paused = not self.is_paused

        if self.is_paused:
            return

        if c_input.name == "PLAYER_ULTIMATE_POWER":
            if c_input.phase == CommandPhase.START:
                total_cooldown = self.shield_cfg['cooldown'] + self.shield_cfg['max_time_used']
                total = total_cooldown + self.last_shield_created_at

                if total <= self.time_counter:
                    create_player_shield(
                        self.ecs_world,
                        self._player_entity,
                        self.shield_cfg,
                        self.time_counter
                    )
                    self.last_shield_created_at = self.time_counter

        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x -= self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x += self.player_cfg['input_velocity']

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.x += self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.x -= self.player_cfg['input_velocity']

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y -= self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y += self.player_cfg['input_velocity']

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_c_v.vel.y += self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self._player_c_v.vel.y -= self.player_cfg['input_velocity']

        if c_input.name == "PLAYER_FIRE":
            if c_input.phase == CommandPhase.START:
                if self.num_bullets < self.level_cfg['player_spawn']['max_bullets']:
                    print("PEW PEW PEW")
                    create_bullet(self.ecs_world, self._player_entity, self.bullet_cfg)
                else:
                    print("No more bullets")


