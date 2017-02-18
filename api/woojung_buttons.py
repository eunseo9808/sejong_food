from api.models import Woojung
from api.models import Woojung_menu
from api.defaults import default_keyboard,default_button

def select_woojung():
    woojungs = Woojung.objects.all()
    restaurant = []
    for woojung in woojungs:
        restaurant.append(woojung.name)

    keyboard_ = {'type': 'buttons', 'buttons': restaurant}
    res = {'message': {'text': '식당을 선택해주세요'}, 'keyboard': keyboard_}

    return res

def select_day(content):
    woojung = Woojung.objects.get(name=content)
    foods = Woojung_menu.objects.filter(type=woojung)
    days = []
    for food in foods:
        days.append(food.day)

    if len(days) == 0:
        res = {'message': {'text': '해당하는 메뉴가 없습니다.'}, 'keyboard': default_keyboard}
    else:
        keyboard_ = {'type': 'buttons', 'buttons': days}
        res = {'message': {'text': '날짜를 선택해주세요'}, 'keyboard': keyboard_}

    return res

def menu_print(content,prev_content):
    woojung = Woojung.objects.get(name=prev_content)
    menu = Woojung_menu.objects.filter(day=content).get(type=woojung)

    keyboard_ = {'type': 'buttons', 'buttons': default_button}
    res = {'message': {'text': menu.menu + "(" + menu.price + ")"}, 'keyboard': keyboard_}
    return res