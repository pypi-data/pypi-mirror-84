from wargame.gameuniterror import HealthMeterException
from attackoftheorcs_v1_1 import Knight


if __name__ == '__main__':
    knight = Knight('sir foo')
    knight.health_meter = 10
    knight.show_health()
    try:
        knight.heal(heal_by=100,full_healing=False)
    except HealthMeterException as e:
        print(e)
        print(e.error_msg)
    knight.show_health()
