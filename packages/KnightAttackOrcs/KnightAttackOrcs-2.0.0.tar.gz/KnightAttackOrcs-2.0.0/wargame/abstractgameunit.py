from abc import ABCMeta, abstractclassmethod
import random
from wargame.gameutils import print_bold
from wargame.gameuniterror import HealthMeterException


class AbstractGameUnit(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name
        self.health_meter = self.max_health
        self.enemy = None

    @abstractclassmethod
    def info(cls):
        pass

    def attack(self, enemy):
        hit_list = [self] * 4 + [enemy] * 6
        injured_unit = random.choice(hit_list)
        injury = random.randint(10, 15)
        injured_unit.health_meter = max(injured_unit.health_meter - injury, 0)
        print('Attack!\t',end='')
        self.show_health(bold=False)
        enemy.show_health(bold=False)

    def heal(self,heal_by=2,full_healing=True):
        if self.health_meter == self.max_health:
            return
        if full_healing:
            self.health_meter = self.max_health
        else:
            self.health_meter+=heal_by
        if self.health_meter > self.max_health:
            raise HealthMeterException("health_meter > max_hp!")
        print_bold('you are healed\t',end='')
        self.show_health()
        print('')

    def run_away(self):
        print_bold('逃跑成功\t', end='')
        self.show_health()

    def show_health(self, bold=True):
        if bold:
            print_bold(f'{self.name} Health：{self.health_meter}\t',end='')
        else:
            print(f'{self.name} Health：{self.health_meter}\t',end='')