import random
import textwrap
from wargame.gameutils import print_bold
from wargame.hut import Hut
from wargame.knight import Knight
from wargame.orchrider import OrcRider


class AttackOfTheOrcs:
    def __init__(self):
        self.huts = []
        self.player = None

    def get_occupants(self):
        occupants = []
        for i in self.huts:
            occupants.append(i.get_occupant_type())
        print('木屋占领情况：',str(occupants))

    @staticmethod
    def show_game_mission():
        width = 70
        print_bold('兽人之袭1.0.0')
        msg = (
            "在人类和他们的敌人之间的战争中，兽人就是第一个到来的敌人。"
            "一支巨大的兽人军队正在向人类的聚集地进发。他们几乎摧毁了行进道路上的一切。"
            "人类不同种族的首领们联起手来击败他们最强大的敌人，来共同为他们的伟大时代而战斗。"
            "人们都被召集起来参加了军队。Foo先生，一个保卫南部平原的勇敢骑士，穿过一片未知的茂密森林，开始长途跋涉，"
            "向东部进发。两天两夜，他小心翼翼地穿过茂密的树林。在路上，他发现了一个小的孤立定居点。"
            "因为疲劳的原因，再加上要希望补充粮食储备，他决定绕道而行。"
            "当他走进村庄时，他看见了五个木屋。周围没有发现任何人。犹豫之后，他决定走进其中一间木屋……"
        )
        print(textwrap.fill(msg, width=width))
        print_bold('任务')
        print('1.占领所有木屋\n2.打败敌人')
        print('-'*70)

    def _process_user_choice(self):
        self.get_occupants()
        hut_not_acquired = True
        while hut_not_acquired:
            house = input('请选择一个木屋(1 to 5):')
            try:
                idx = int(house)
            except ValueError as e:
                print('Invalid input:',e)
                continue
            try:
                if idx <= 0:
                    raise IndexError
                if not self.huts[idx-1].is_acquired:
                    hut_not_acquired = False
                else:
                    print("you can not heal in hut already acquired!")
            except IndexError:
                print(f'Invalid number {idx},no such hut!')
                continue
        return idx

    def _occupy_huts(self):
        choice_list = [Knight, OrcRider, None]
        for i in range(5):
            choice = random.choice(choice_list)
            if choice:
                name = 'Knight' if choice == Knight else 'enemy'
                self.huts.append(Hut(i + 1, choice(name + '-' +str(i))))
            else:
                self.huts.append(Hut(i + 1, choice))

    def play(self):
        self.player = Knight('Foo')
        self._occupy_huts()
        acquired_huts_counter = 0

        self.show_game_mission()
        self.player.show_health()

        while acquired_huts_counter < 5:
            idx = self._process_user_choice()
            self.player.acquire_hut(self.huts[idx - 1])

            if self.player.health_meter <= 0:
                print_bold('You lose the game')
                break

            if self.huts[idx - 1].is_acquired:
                acquired_huts_counter += 1
        if acquired_huts_counter == 5:
            print_bold('Congratulations! You win!')


if __name__ == '__main__':
    game = AttackOfTheOrcs()
    game.play()
