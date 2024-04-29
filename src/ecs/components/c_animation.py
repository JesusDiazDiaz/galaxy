from typing import List


class CAnimation:
    def __init__(self, animations: dict):
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = [
            AnimationData(
                anim["name"],
                anim["start"],
                anim["end"],
                anim["framerate"],
            ) for anim in animations["list"]
        ]
        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float):
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate
