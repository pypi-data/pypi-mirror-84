from wargame.gameutils import print_bold


class Hut:
    def __init__(self, num, occupant):
        self.occupant = occupant
        self.number = num
        self.is_acquired = False

    def acquire(self, new_occupant):
        self.is_acquired = True
        print_bold('干得漂亮，你获得了这间木屋')
        self.occupant = new_occupant

    def get_occupant_type(self):
        if self.is_acquired:
            occupant_type = 'Acquired'
        elif self.occupant is None:
            occupant_type = 'unoccupied'
        else:
            occupant_type = self.occupant.unit_type
        return occupant_type