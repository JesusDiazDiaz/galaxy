
class CEnemySpawner:
    def __init__(self, enemy_spawn_events):
        self.enemy_spawn_events = enemy_spawn_events
        self.event_triggered = [False] * len(enemy_spawn_events)

        print(f"CEnemySpawner created ${self.enemy_spawn_events} ${self.event_triggered}")
