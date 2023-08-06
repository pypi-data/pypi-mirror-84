from wargame.abstractgameunit import AbstractGameUnit
from wargame.gameutils import print_bold
from wargame.orchrider import OrcRider


class Knight(AbstractGameUnit):
    def __init__(self, name):
        self.max_health = 40
        super().__init__(name)
        self.unit_type = 'friend'

    def acquire_hut(self, hut):
        print('\033[1m' + f'Foo先生进入了木屋{hut.number}...'+ '\033[0m',end='')
        is_enemy = isinstance(hut.occupant, OrcRider)

        if not is_enemy:
            if isinstance(hut.occupant, Knight):
                print_bold('遇见队友')
            else:
                print_bold('一间空木屋')
            hut.acquire(self)
            self.heal()
        else:
            print_bold('看见敌人')
            self.show_health()
            hut.occupant.show_health()
            continue_attack = 'y'

            while continue_attack == 'y':
                continue_attack = input('····continue to attack？y/n')
                if continue_attack not in 'ynYN':
                    print(f'such input "{continue_attack}" not allowed')
                    continue_attack = 'y'
                    continue

                if continue_attack == 'n':
                    self.run_away()
                    print('')
                    break

                self.attack(hut.occupant)

                if hut.occupant.health_meter <= 0:
                    print('')
                    hut.acquire(self)
                    break
                if self.health_meter <= 0:
                    print('')
                    break

    def __str__(self):
        return self.name

    def info(cls):
        return 'Knight'