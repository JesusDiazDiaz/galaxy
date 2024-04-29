from enum import Enum

import pygame


class CHunterState:
    def __init__(
            self,
            velocity_chase: int,
            velocity_return: int,
            distance_start_chase: int,
            distance_start_return: int,
            initial_position: pygame.Vector2,
            sound_chase: str
    ) -> None:
        self.state = HunterState.IDLE

        self.velocity_chase = velocity_chase
        self.velocity_return = velocity_return
        self.distance_start_chase = distance_start_chase
        self.distance_start_return = distance_start_return
        self.initial_position = initial_position
        self.sound_chase = sound_chase


class HunterState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2
