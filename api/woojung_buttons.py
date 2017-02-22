from django.core.exceptions import ObjectDoesNotExist

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
    try:
        woojung = Woojung.objects.get(name=content)
    except ObjectDoesNotExist:
        return {'message': {'text': '해당하는 메뉴가 없습니다.'}, 'keyboard': default_keyboard}

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
    try :
        woojung = Woojung.objects.get(name=prev_content)
    except ObjectDoesNotExist:
        return {'message': {'text': '해당하는 메뉴가 없습니다.'}, 'keyboard': default_keyboard}

    menu = Woojung_menu.objects.filter(day=content).get(type=woojung)
    if menu.menu == '' :
        res = {'message': {'text': "해당하는 값에 데이터가 없습니다."}, 'keyboard': default_keyboard}
    else :
        res = {'message': {'text': menu.menu + "(" + menu.price + ")"}, 'keyboard': default_keyboard}
    return res