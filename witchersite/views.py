from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import StartDataForm, ActionForm
from . base_units import *
from . enemy_units import *
from . game import *
from . witcher_unit import *
from django.http import JsonResponse, response


def index(request):
    return render(request, 'witchersite/index.html')


def about(request):
    return render(request, 'witchersite/about.html')


def project(request):
    return render(request, 'witchersite/project.html')


def welcome(request):
    error = ''
    if request.method == 'POST':
        form = StartDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game')

        else:
            error = 'Форма заполнена некорректно'
    form = StartDataForm()

    data = {

        'form': form,
        'error': error
    }
    return render(request, 'witchersite/witcher.html', data)


def get_initial_values():

    datas = StartData.objects.last()
    witcher_level = int(datas.witcher_level)
    enemy_level = int(datas.enemy_level)
    enemy_amount = int(datas.enemy_amount)

    return witcher_level, enemy_level, enemy_amount


def get_env_and_start(witcher_level, enemy_level, enemy_amount, session_key):
    game = ModelGame.objects.create(session_key=session_key, turn=0)
    game.save()
    witcher = WitcherModel.objects.create(name='Ведьмак', level=witcher_level, hp=400*witcher_level,
                                          attack_power=30*witcher_level, threshold_hp=(witcher_level*400)*0.3,
                                          max_hp=400*witcher_level, game=game)
    witcher.save()

    type_enemy = random.randint(0, 2)
    if type_enemy == 0:
        for el in range(0, enemy_amount):
            drowner = DrownerModel.objects.create(name='Утопец', level=enemy_level, hp=200*enemy_level,
                                          attack_power=50*enemy_level, game=game, accuracy=0.55, crit=0.1)
            drowner.save()

    elif type_enemy == 1:
        for el in range(0, enemy_amount):
            bandit = BanditModel.objects.create(name='Бандит', level=enemy_level, hp=150*enemy_level,
                                          attack_power=25*enemy_level, game=game, accuracy=0.85, crit=0.13)
            bandit.save()

    else:
        for el in range(0, enemy_amount):
            ghost = GhostModel.objects.create(name='Призрак', level=enemy_level, hp=300*enemy_level,
                                              attack_power=40*enemy_level, game=game, accuracy=0.65,
                                              crit=0.08, ability=4, treshold_hp=(300*enemy_level)*0.3)
            ghost.save()
    return witcher_level, enemy_level, enemy_amount, type_enemy


def game(request):
    error = ''
    session_key = request.session.session_key
    if not session_key:
         request.session.cycle_key()
         session_key = request.session.session_key
    print(session_key)
    if 'is_game_started' in request.session:
        cookie_is_started = request.session['is_game_started']
        print('check1')

    else:
        cookie_is_started = False
        print('check2')

    if not cookie_is_started:
        witcher_level, enemy_level, enemy_amount = get_initial_values()
        initial_data = get_env_and_start(witcher_level, enemy_level, enemy_amount, session_key)
        request.session['is_game_started'] = True
        request.session['type_enemy'] = initial_data[3]
        print('check3')

    game = ModelGame.objects.filter(session_key=session_key).last()
    witcher = WitcherModel.objects.filter(game=game).last()

    type_enemy = request.session['type_enemy']

    if request.method == 'GET':
        form = ActionForm(request.GET)
        if form.is_valid():
            form.save()
            return redirect('/')

        else:
            error = 'Форма заполнена некорректно'

    form = ActionForm

    if type_enemy == 0:
        enemy = DrownerModel.objects.filter(game=game)
        enemy_amount = enemy.count()
        data = {
            'enemy': enemy,
            'witcher': witcher,
            'amount': enemy_amount,
            'form': form,
            'error': error,
            'game': game
        }
        return render(request, 'witchersite/brief.html', data)

    elif type_enemy == 1:
        enemy = BanditModel.objects.filter(game=game)
        enemy_amount = enemy.count()
        data = {
            'enemy': enemy,
            'witcher': witcher,
            'amount': enemy_amount,
            'form': form,
            'error': error,
            'game': game
        }
        return render(request, 'witchersite/brief.html', data)
    else:
        enemy = GhostModel.objects.filter(game=game)
        enemy_amount = enemy.count()
        data = {
            'enemy': enemy,
            'witcher': witcher,
            'amount': enemy_amount,
            'form': form,
            'error': error,
            'game_turn': game
        }
        return render(request, 'witchersite/brief.html', data)


def user_action(request):
    data = request.POST
    action = data.get("action")
    return_dict = dict()
    return_dict['action'] = action
    session_key = request.session.session_key
    game_model = ModelGame.objects.filter(session_key=session_key).last()
    witcher_model = WitcherModel.objects.filter(game=game_model).last()
    type_enemy = request.session['type_enemy']
    enemies = []

    if type_enemy == 0:
        enemy_model = DrownerModel.objects.filter(game=game_model)
        for enemy in enemy_model:
            drowner = Drowner(1)
            drowner.hp = enemy.hp
            drowner.level = enemy.level
            drowner.attack_power = enemy.attack_power
            drowner.accuracy = enemy.accuracy
            drowner.ability = enemy.ability
            drowner.crit = enemy.crit
            drowner.attack_speed = enemy.attack_speed
            drowner.in_rage = enemy.in_rage
            enemies.append(drowner)

    elif type_enemy == 1:
        enemy_model = BanditModel.objects.filter(game=game_model)
        bandit = Bandit(1)
        for enemy in enemy_model:
            bandit.hp = enemy.hp
            bandit.level = enemy.level
            bandit.attack_power = enemy.attack_power
            bandit.accuracy = enemy.accuracy
            bandit.ability = enemy.ability
            bandit.crit = enemy.crit
            bandit.attack_speed = enemy.attack_speed
            bandit.dodge = enemy.dodge
            bandit.special_ability = enemy.special_ability
            bandit.cry_chance = enemy.cry_chance
            bandit.crying = enemy.crying
            bandit.block = enemy.block
            enemies.append(bandit)
    else:
        enemy_model = GhostModel.objects.filter(game=game_model)
        for enemy in enemy_model:
            ghost = Ghost(1)
            ghost.hp = enemy.hp
            ghost.level = enemy.level
            ghost.attack_power = enemy.attack_power
            ghost.accuracy = enemy.accuracy
            ghost.ability = enemy.ability
            ghost.crit = enemy.crit
            ghost.threshold_hp = enemy.treshold_hp
            ghost.last_turn_ability_used = enemy.last_turn_ability_used
            ghost.in_astral = enemy.in_astral
            enemies.append(ghost)


    witcher = Witcher(1)
    witcher.hp = witcher_model.hp
    witcher.max_hp = witcher_model.max_hp
    witcher.shield = witcher_model.shield
    witcher.level = witcher_model.level
    witcher.threshold_hp = witcher_model.threshold_hp
    witcher.attack_power = witcher_model.attack_power
    witcher.crit = witcher_model.crit
    witcher.energy = witcher_model.energy
    witcher.max_energy = witcher_model.max_energy
    witcher.accuracy = witcher_model.accuracy
    witcher.last_turn_power_attack = witcher_model.last_turn_power_attack
    witcher.last_turn_potions_used = {Potions.swallow: witcher_model.last_swallow,
                          Potions.thunder: witcher_model.last_thunder, Potions.tawny_owl: witcher_model.last_tawny_owl}
    witcher.potions = {Potions.swallow: witcher_model.swallow, Potions.thunder: witcher_model.thunder,
                                                                             Potions.tawny_owl: witcher_model.tawny_owl}
    beginning_game = Game(witcher, enemies)
    beginning_game.turn = game_model.turn
    message = {}
    message['log'] = []
    message['error_code'] = ''

    endgame = beginning_game.fight(int(action), message)
    print('this endgame ', endgame)
    if endgame[0]:
        clear_models(request)
        return_dict['message'] = 'game_ended'
        if endgame[1]:
            return_dict['win_witcher'] = 'witcher_wins'
        else:
            return_dict['win_witcher'] = 'enemies_wins'
        print('check33')
        return JsonResponse(return_dict)

    else:
        update_models(witcher, enemy_model, witcher_model, enemies, game_model, beginning_game)

    return_dict['message'] = message['error_code']
    return_dict['history'] = message['log']
    print('check44')
    print(message)
    return JsonResponse(return_dict)


def update_models(witcher, enemy_model, witcher_model, enemies, game_model, beginning_game):

    for i in range(len(enemies)):

        if isinstance(enemies[i], Drowner):
            enemy_model[i].hp = enemies[i].hp
            enemy_model[i].level = enemies[i].level
            enemy_model[i].attack_power = enemies[i].attack_power
            enemy_model[i].accuracy = enemies[i].accuracy
            enemy_model[i].ability = enemies[i].ability
            enemy_model[i].crit = enemies[i].crit
            enemy_model[i].attack_speed = enemies[i].attack_speed
            enemy_model[i].in_rage = enemies[i].in_rage
            enemy_model[i].save()

        elif isinstance(enemies[i], Bandit):
            enemy_model[i].hp = enemies[i].hp
            enemy_model[i].level = enemies[i].level
            enemy_model[i].attack_power = enemies[i].attack_power
            enemy_model[i].accuracy = enemies[i].accuracy
            enemy_model[i].ability = enemies[i].ability
            enemy_model[i].crit = enemies[i].crit
            enemy_model[i].attack_speed = enemies[i].attack_speed
            enemy_model[i].dodge = enemies[i].dodge
            enemy_model[i].special_ability = enemies[i].special_ability
            enemy_model[i].cry_chance = enemies[i].cry_chance
            enemy_model[i].crying = enemies[i].crying
            enemy_model[i].block = enemies[i].block
            enemy_model[i].save()
        else:
            enemy_model[i].hp = enemies[i].hp
            enemy_model[i].level = enemies[i].level
            enemy_model[i].attack_power = enemies[i].attack_power
            enemy_model[i].accuracy = enemies[i].accuracy
            enemy_model[i].ability = enemies[i].ability
            enemy_model[i].crit = enemies[i].crit
            enemy_model[i].treshold_hp = enemies[i].threshold_hp
            enemy_model[i].last_turn_ability_used = enemies[i].last_turn_ability_used
            enemy_model[i].in_astral = enemies[i].in_astral
            enemy_model[i].save()

    witcher_model.hp = witcher.hp
    witcher_model.shield = witcher.shield
    witcher_model.level = witcher.level
    witcher_model.threshold_hp = witcher.threshold_hp
    witcher_model.attack_power = witcher.attack_power
    witcher_model.crit = witcher.crit
    witcher_model.energy = witcher.energy
    witcher_model.max_energy = witcher.max_energy
    witcher_model.max_hp = witcher.max_hp
    witcher_model.accuracy = witcher.accuracy
    witcher_model.last_turn_power_attack = witcher.last_turn_power_attack
    witcher_model.last_swallow = witcher.last_turn_potions_used[Potions.swallow]
    witcher_model.last_thunder = witcher.last_turn_potions_used[Potions.thunder]
    witcher_model.last_tawny_owl = witcher.last_turn_potions_used[Potions.tawny_owl]
    witcher_model.swallow = witcher.potions[Potions.swallow]
    witcher_model.thunder = witcher.potions[Potions.thunder]
    witcher_model.tawny_owl = witcher.potions[Potions.tawny_owl]
    witcher_model.save()

    game_model.turn = beginning_game.turn
    game_model.save()


def clear_models(request):
    session_key = request.session.session_key
    if 'type_enemy' in request.session:
        type_enemy = request.session['type_enemy']

        game_model = ModelGame.objects.filter(session_key=session_key).last()
        witcher_model = WitcherModel.objects.filter(game=game_model).last()
        WitcherModel.objects.filter(game=game_model).delete()

        if type_enemy == 0:
            DrownerModel.objects.filter(game=game_model).delete()

        elif type_enemy == 1:
            BanditModel.objects.filter(game=game_model).delete()
        else:
            GhostModel.objects.filter(game=game_model).delete()

        ModelGame.objects.filter(session_key=session_key).delete()
        del request.session['type_enemy']
        del request.session['is_game_started']
        request.session.modified = True
        # StartData.objects.last().delete()


def end_game(request):
    clear_models(request)
    winner = request.GET['win']
    print(type(winner))
    if winner == '0':
        print('check55')
        data = {
            'winner': 'witcher'
        }
    else:
        print('check66')
        data = {
            'winner': 'enemies'
        }
    print(data)
    return render(request, 'witchersite/endgame.html', data)
