from api.models import Student_union_menu
from api.defaults import default_keyboard
from django.core.exceptions import ObjectDoesNotExist
import random

def select_student():
    keyboard_ = {'type': 'buttons', 'buttons': ['음식 종류', '음식 가격', '메뉴 추천', '인기 메뉴', '랜덤 메뉴']}
    res = {'message': {'text': '선택해주세요'}, 'keyboard': keyboard_}

    return res


def random_menu():
    food_list = Student_union_menu.objects.all()
    random_key = random.choice(food_list)
    msg = "추천메뉴는 " + random_key.name + "(" + random_key.price + ")입니다."

    res = {"message": {"text": msg}, 'keyboard': default_keyboard}

    return res

def menu_kind():
    foods = Student_union_menu.objects.all()
    food_str = ''

    for food in foods:
        food_str += food.name + "(" + food.price + ")" + "\n"

    food_str = food_str[:len(food_str) - 1]

    res = {'message': {'text': food_str}, 'keyboard': default_keyboard}
    return res

def menu_price():
    food_list = Student_union_menu.objects.all()
    buttons = []

    for food in food_list:
        buttons.append(food.name)

    keyboard_ = {'type': 'buttons', 'buttons': buttons}
    res = {'message': {'text': '원하는 음식을 선택해주세요'}, 'keyboard': keyboard_}

    return res

def recommend_menu():
    food_list = Student_union_menu.objects.all()
    buttons = []

    for food in food_list:
        buttons.append(food.name)

    keyboard_ = {'type': 'buttons', 'buttons': buttons}
    res = {'message': {'text': '추천 할 음식을 선택해주세요'}, 'keyboard': keyboard_}

    return res

def best_menu():
    foods = list(Student_union_menu.objects.all().order_by('-popular'))
    msg = "가장 인기있는 음식은?\n"

    count = 1
    prev_food = foods[0]
    rank = 1
    for food in foods:

        if prev_food.popular == food.popular:
            msg += str(rank) + "위 " + str(food.popular) + "표 " + food.name + "(" + food.price + ")"
        else:
            rank = count
            msg += str(count) + "위 " + str(food.popular) + "표 " + food.name + "(" + food.price + ")"

        prev_food = food
        count += 1
        if count > 5: break
        else: msg+="\n"

    res = {'message': {'text': msg}, 'keyboard': default_keyboard}
    return res

def select_recommend_menu(content):
    try :
        food = Student_union_menu.objects.get(name=content)
    except ObjectDoesNotExist:
        res = {'message': {'text': '옳지 않은 데이터입니다.'}, 'keyboard': default_keyboard}
        return res

    food.popular += 1
    food.save()
    res = {'message': {'text': '추천 완료되었습니다!'}, 'keyboard': default_keyboard}
    return res

def select_menu_price(content):
    try:
        food = Student_union_menu.objects.get(name=content)
    except ObjectDoesNotExist:
        res = {'message': {'text': '옳지 않은 데이터입니다.'}, 'keyboard': default_keyboard}
        return res

    msg = food.name + "의 가격은 " + food.price + "입니다."
    res = {'message': {'text': msg}, 'keyboard': default_keyboard}
    return res