from django.db import models
from enum import Enum


class ModelGame(models.Model):
    session_key = models.CharField(max_length=128, default=None)
    beginned_game = models.BooleanField(default=False)
    turn = models.PositiveIntegerField('Ход', default=0)


class StartData(models.Model):
    witcher_level = models.PositiveIntegerField('Уровень Ведьмака')
    enemy_level = models.PositiveIntegerField('Уровень Противников')
    enemy_amount = models.PositiveIntegerField('Количество противников')

    def __int__(self):
        return self.witcher_level, self.enemy_level, self.enemy_amount

    class Meta:
        verbose_name = "Данные"
        verbose_name_plural = "Данные"


class Action(models.Model):
    action = models.PositiveIntegerField('Следующее действие')

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"


class Enemies(models.Model):

    class Meta:
        abstract = True
    level = models.IntegerField("Уровень противника", default=0)
    hp = models.IntegerField("Здоровье противника", default=0)
    attack_power = models.PositiveIntegerField("Сила атаки", default=0)
    accuracy = models.FloatField("Точность", default=0)
    ability = models.IntegerField("Способности", default=3)
    crit = models.FloatField("Крит", default=0)
    treshold_hp = models.IntegerField("Пороговое здоровье", default=0)


class BanditModel(Enemies):
    name = models.CharField("Название", max_length=20)
    attack_speed = models.IntegerField("Скорость атаки", default=1)
    dodge = models.BooleanField("Уклонение", default=False)
    special_ability = models.IntegerField("Спец. способность", default=1)
    cry_chance = models.FloatField("Шанс клича", default=0.85)
    crying = models.BooleanField("Клич", default=False)
    block = models.BooleanField("Шанс блока", default=False)
    game = models.ForeignKey(ModelGame, on_delete=models.CASCADE, default=None, null=False)

    def __str__(self):
        return '{0}  {1}% {2}хп {3} сила атаки'.format('Бандит', self.accuracy, self.hp, self.attack_power)


class GhostModel(Enemies):
    name = models.CharField("Название", max_length=20)
    last_turn_ability_used = models.IntegerField("Ход использования способности", default=-1)
    in_astral = models.BooleanField("состояние ухода в астрал", default=False)
    game = models.ForeignKey(ModelGame, on_delete=models.CASCADE, default=None, null=False)

    def __str__(self):
        return '{0}  {1}% {2}хп {3} сила атаки'.format('Призрак', self.accuracy, self.hp, self.attack_power)


class DrownerModel(Enemies):
    name = models.CharField("Название", max_length=20)
    in_rage = models.BooleanField("В ярости", default=False)
    attack_speed = models.IntegerField("Скорость атаки", default=1)
    game = models.ForeignKey(ModelGame, on_delete=models.CASCADE, default=None, null=False)

    def __str__(self):
        return '{0} {1}% {2}хп {3} сила атаки'.format('Утопец', self.accuracy, self.hp, self.attack_power)


class WitcherModel(models.Model):
    name = models.CharField("Имя", max_length=20)
    level = models.IntegerField("Уровень Ведьмака", default=0)
    hp = models.IntegerField("Здоровье Ведьмака")
    attack_power = models.IntegerField("Сила атаки")
    crit = models.FloatField("Шанс крита", default=0.16)
    last_turn_power_attack = models.IntegerField("Последнее использование силовой атаки", default=-1)
    max_hp = models.IntegerField("Максимальное здоровье")
    threshold_hp = models.FloatField("Пороговое здоровье")
    energy = models.IntegerField("Энергия", default=100)
    max_energy = models.IntegerField("Максимальная энергия", default=100)
    shield = models.IntegerField("Щит", default=0)
    accuracy = models.FloatField("Точность", default=0.95)
    game = models.ForeignKey(ModelGame, on_delete=models.CASCADE, default=None, null=False)
    swallow = models.IntegerField("Ласточка", default=2)
    thunder = models.IntegerField("Гром", default=2)
    tawny_owl = models.IntegerField("Неясыть", default=1)
    last_swallow = models.IntegerField("Последнее использование Ласточки", default=-1)
    last_thunder = models.IntegerField("Последнее использование Грома", default=-1)
    last_tawny_owl = models.IntegerField("Последнее использование Неясыти", default=-1)

    def __str__(self):
        return 'Ведьмак {0}й ур, {1}%, {2}хп, {3} сила атаки, {4} текущий щит, {5} текущий уровень энергии'.format(
                                        self.level, self.accuracy, self.hp, self.attack_power, self.shield, self.energy)






