from api.models import kunja_menu
from api.defaults import default_keyboard

def select_kunja():
    foods = kunja_menu.objects.all()
    count = 0
    days = []
    for food in foods:
        days.append(food.day)

    keyboard_ = {'type': 'buttons', 'buttons': days}
    res = {'message': {'text': '날짜를 선택해주세요'}, 'keyboard': keyboard_}

    return res

def kunja_lunch_or_dinner():
    keyboard_ = {'type': 'buttons', 'buttons': ['중식', '석식']}
    res = {'message': {'text': '중식, 석식 선택해주세요.'}, 'keyboard': keyboard_}
    return res


def kunja_select_lunch(content):
    menu = kunja_menu.objects.get(day=content).lunch
    res = {'message': {'text': menu}, 'keyboard': default_keyboard}

    return res


def kunja_select_dinner(content):
    menu = kunja_menu.objects.get(day=content).dinner
    res = {'message': {'text': menu}, 'keyboard': default_keyboard}

    return res