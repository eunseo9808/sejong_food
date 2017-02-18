from api.models import Skyrounge_menu
from api.defaults import default_keyboard

def select_skyrounge():
    foods = Skyrounge_menu.objects.all()
    count = 0
    days = []
    for food in foods:
        days.append(food.day)

    keyboard_ = {'type': 'buttons', 'buttons': days}
    res = {'message': {'text': '날짜를 선택해주세요(일주일 단위로 업데이트 됩니다)'}, 'keyboard': keyboard_}

    return res

def sky_lunch_or_dinner():
    keyboard_ = {'type': 'buttons', 'buttons': ['중식', '석식']}
    res = {'message': {'text': '중식, 석식 선택해주세요.'}, 'keyboard': keyboard_}
    return res

def sky_select_lunch(content):
    menu = Skyrounge_menu.objects.get(day=content).lunch
    if menu == '' :
        menu="해당하는 값에 데이터가 없습니다."
    res = {'message': {'text': menu}, 'keyboard': default_keyboard}

    return res

def sky_select_dinner(content):
    menu = Skyrounge_menu.objects.get(day=content).dinner
    if menu == '' :
        menu="해당하는 값에 데이터가 없습니다."
    res = {'message': {'text': menu}, 'keyboard': default_keyboard}

    return res