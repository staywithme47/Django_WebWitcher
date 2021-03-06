import random
from . witcher_unit import *
from . base_units import *
from . enemy_units import *


class Game:
    def __init__(self, witcher: Witcher, enemies: list, history: list = []):
        self.witcher = witcher
        self.enemies = enemies
        self.turn = 0
        self.history = history

    def enemies_is_alive(self) -> bool:
        return len(self.enemies) > 0

    def get_damage_to_enemies(self, inf: list, action, message) -> PlayerAction:
        result: tuple = self.witcher.next_move(self.history, self.turn, inf, action, message)
        if result[0] is None:
            return result[0]

        for enemy in self.enemies:
            enemy.block = False

        for enemy in self.enemies:
            enemy.next_action(result[0], result[1], self.turn, self.witcher, self.history, self.enemies, message)

        return result[0]

    def get_damage_to_witcher(self, result: PlayerAction, message) -> None:
        attacker = None
        accuracy = self.enemies[0].accuracy

        if result == PlayerAction.axiy:
            attacker = random.choice(self.enemies)
            attacker_position = self.enemies.index(attacker)

            if len(self.enemies) > 1:
                defender = random.choice(self.enemies[:attacker_position] + self.enemies[attacker_position+1:])

                if random.random() > accuracy:
                    message['log'].append('\nХод {0}. Противник номер {1} промахнулся по противнику номер {2} под действием Аксия'
                                                   .format(self.turn, self.enemies.index(attacker),
                                                                                      self.enemies.index(defender)))
                    self.history.append('Ход {0}. Противник номер {1} промахнулся по противнику номер {2} под действием Аксия'
                                                                            .format(self.turn, self.enemies.index(attacker),
                                                                                              self.enemies.index(defender)))

                else:
                    k = 1.0

                    if isinstance(defender, Ghost) and defender.in_astral:
                        k = 0.2
                        message['log'].append('Призрак ушел в астрал под Аксием')

                    if random.random() < attacker.crit:
                        k *= 2
                        message['log'].append('Аттакер кританул')

                    damage = attacker.attack_power * k
                    defender.hp -= damage
                    message['log'].append('\nХод {0}. Противник номер {1} попал по противнику номер {2} по действием знака Аксий и нанес '
                      '{3} урона'.format(self.turn, self.enemies.index(attacker), self.enemies.index(defender), damage))
                    self.history.append('Ход {0}. Противник номер {1} попал по противнику номер {2} по действием знака Аксий и нанес '
                      '{3} урона'.format(self.turn, self.enemies.index(attacker), self.enemies.index(defender), damage))

        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            if enemy == attacker:
                message['log'].append('\nПротивник номер {0} находится под действием аксия'.format(i))
                self.history.append('Противник номер {0} находится под действием аксия'.format(i))
                continue

            enemy.deal_damage_to_witcher(result, self.witcher, self.turn, self.history, message)

    def fight(self, action, message):
        inf: list = []
        inf = list(map(lambda enemy: enemy.get_fullname(), self.enemies))
        result = self.get_damage_to_enemies(inf, action, message)
        if result is None:
            return False, False

        for enemy in self.enemies:
            if enemy.hp <= 0:
                Unit.update_amount_of_alive(False)

        self.enemies: list = list(filter(lambda x: x.hp > 0, self.enemies))
        if not self.enemies_is_alive():
            win_witcher = True
            return True, win_witcher
        self.get_damage_to_witcher(result, message)

        if self.witcher.hp <= 0:
            Unit.update_amount_of_alive(False)
            win_witcher = False
            return True, win_witcher

        self.turn += 1
        return False, False
        # if self.witcher.hp <= 0:
        #     self.history.append('Поражение. Ведьмак мертв')
        #     self.store_history()
        #
        #     return 'Ведьмак мертв, ты проиграл'
        # else:
        #     self.history.append('Победа. Все враги повержены')
        #     self.store_history()
        #
        #     return 'Все враги мертвы, Ведьмак победил'

    def store_history(self) -> None:
        with open('game_log.txt', 'w', encoding='utf-8') as f:
            for el in self.history:
                f.write(el + '\n')

    def find_turn_log(self, n: str) -> list:
        result = list(filter(lambda x: x.find(n) != -1, self.history))

        return result
