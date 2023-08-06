from wargame.abstractgameunit import AbstractGameUnit


class OrcRider(AbstractGameUnit):
    def __init__(self, name):
        self.max_health = 30
        super().__init__(name)
        self.unit_type = 'enemy'

    def __str__(self):
        return self.name

    def info(cls):
        return 'enemy'