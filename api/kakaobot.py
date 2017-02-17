from django.http import HttpResponse
from django.http import JsonResponse
from api.models import *
import random
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import ast

default_button=["학생회관", "찬 스카이라운지","우정당 학생 식당", "군자관"]
default_keyboard={'type': 'buttons', 'buttons':default_button}

@csrf_exempt
def friend(request):
    request_str = request.body.decode("utf-8")
    request_json = json.loads(request_str)
    user_key = request_json['user_key']
    if request.method=='POST':
        user = Chatter.objects.create(user_key=user_key)
        user.save()
        res = {"message": {"text": "안녕하세요!"}, 'keyboard': default_keyboard}
        return JsonResponse(res, status=200)

    elif request.method=='DELETE':
        user = Chatter.objects.get(user_key=user_key)
        chattings=Chat.objects.filter(user=user).delete()
        user.delete()

@csrf_exempt
def keyboard(request):
    res = default_keyboard
    return JsonResponse(res)

@csrf_exempt
def message(request):

    request_str=request.body.decode("utf-8")
    request_json=json.loads(request_str)
    content=request_json['content']
    user_key=request_json['user_key']

    user=Chatter.objects.filter(user_key=user_key)
    if user.count()==0 :
        user=Chatter.objects.create(user_key=user_key)
        user.save()
    else :
        user=user.first()

    chats=Chat.objects.filter(user=user).order_by("-created_date")
    if chats.count()>=5 :
        chats.last().delete()
    elif chats.count()>0 :
        if chats.first().content==content :
            res = {"message": {"text": content}, 'keyboard': default_keyboard}

            return JsonResponse(res, status=200)

    chat=Chat.objects.create(user=user, content=content)
    chat.save()

    res = {"message": {"text": content}, 'keyboard': default_keyboard}

    if "랜덤 메뉴" == content:
        food_list = Student_union_menu.objects.all()
        random_key = random.choice(food_list)
        msg = "추천메뉴는 " + random_key.name + "(" + random_key.price + ")입니다."

        res = {"message": {"text": msg}, 'keyboard': default_keyboard}

    elif "찬 스카이라운지" == content:
        foods=Skyrounge_menu.objects.all()
        count=0
        days=[]

        for food in foods:
            days.append(food.day)


        keyboard_ = {'type': 'buttons', 'buttons': days}
        res = {'message': {'text': '날짜를 선택해주세요(일주일 단위로 업데이트 됩니다)'}, 'keyboard': keyboard_}

    elif "우정당 학생 식당" == content:
        woojungs = Woojung.objects.all()
        restaurant = []
        for woojung in woojungs:
            restaurant.append(woojung.name)
        keyboard_ = {'type': 'buttons', 'buttons': restaurant}
        res = {'message': {'text': '식당을 선택해주세요'}, 'keyboard': keyboard_}

    elif "군자관" == content:
        foods = kunja_menu.objects.all()
        count = 0
        days = []
        for food in foods:
            days.append(food.day)

        keyboard_ = {'type': 'buttons', 'buttons': days}
        res = {'message': {'text': '날짜를 선택해주세요'}, 'keyboard': keyboard_}

    elif "학생회관" == content:
        keyboard_= {'type': 'buttons', 'buttons':['음식 종류','음식 가격', '메뉴 추천','인기 메뉴', '랜덤 메뉴']}
        res = {'message': {'text': '선택해주세요'}, 'keyboard': keyboard_}

    elif "음식 종류" == content:
        foods = Student_union_menu.objects.all()
        food_str=''

        for food in foods:
            food_str+=food.name+"("+food.price+")"+"\n"

        food_str.strip()

        res = {'message': {'text': food_str}, 'keyboard': default_keyboard}

    elif "음식 가격" == content:
        food_list = Student_union_menu.objects.all()
        buttons=[]

        for food in food_list:
            buttons.append(food.name)

        keyboard_ = {'type': 'buttons', 'buttons': buttons}
        res = {'message': {'text': '원하는 음식을 선택해주세요'}, 'keyboard': keyboard_}

    elif "메뉴 추천" == content:
        food_list = Student_union_menu.objects.all()
        buttons = []

        for food in food_list:
            buttons.append(food.name)

        keyboard_ = {'type': 'buttons', 'buttons': buttons}
        res = {'message': {'text': '추천 할 음식을 선택해주세요'}, 'keyboard': keyboard_}
    elif "인기 메뉴"==content:
        foods = list(Student_union_menu.objects.all().order_by('-popular'))
        msg="가장 인기있는 음식은?\n"

        count=1
        prev_food=foods[0]
        rank=1
        for food in foods:
            if prev_food.popular==food.popular :
                msg += str(rank) + "위 " + str(food.popular) + "표 " + food.name + "(" + food.price + ")\n"
            else :
                rank=count
                msg+=str(count)+"위 "+str(food.popular)+"표 "+food.name+"("+food.price+")\n"

            prev_food = food
            count+=1
            if count>5 : break

        res = {'message': {'text': msg}, 'keyboard': default_keyboard}

    else :
        chatter = Chatter.objects.get(user_key=user_key)
        chattings = list(Chat.objects.filter(user=chatter).order_by("-created_date"))
        foods=Student_union_menu.objects.filter(name=content)

        if foods.count() > 0 :
            if chattings[1].content=="메뉴 추천":
                food = foods.first()
                food.popular+=1
                food.save()
                res = {'message': {'text': '추천 완료되었습니다!'}, 'keyboard': default_keyboard}
            else :
                food=foods.first()
                print("?????")
                msg=food.name+"의 가격은 "+food.price+"입니다."
                res = {'message': {'text': msg}, 'keyboard': default_keyboard}
        else :


            if chattings[1].content=="찬 스카이라운지":
                keyboard_ = {'type': 'buttons', 'buttons': ['중식', '석식']}
                res = {'message': {'text': '중식, 석식 선택해주세요.'}, 'keyboard': keyboard_}
            elif chattings[1].content=="우정당 학생 식당":
                woojung = Woojung.objects.get(name=content)
                foods = Woojung_menu.objects.filter(type=woojung)
                days = []
                for food in foods:
                    days.append(food.day)

                if len(days) == 0 :
                    res = {'message': {'text': '해당하는 메뉴가 없습니다.'}, 'keyboard': default_keyboard}
                else :
                    keyboard_ = {'type': 'buttons', 'buttons': days}
                    res = {'message': {'text': '날짜를 선택해주세요'}, 'keyboard': keyboard_}
            elif chattings[1].content == "군자관":
                keyboard_ = {'type': 'buttons', 'buttons': ['중식', '석식']}
                res = {'message': {'text': '중식, 석식 선택해주세요.'}, 'keyboard': keyboard_}

            else:
                if chattings[2].content == "찬 스카이라운지":
                    if content == "중식":
                        menu = Skyrounge_menu.objects.get(day=chattings[1].content).lunch
                        res = {'message': {'text': menu}, 'keyboard': default_keyboard}
                    else:
                        menu = Skyrounge_menu.objects.get(day=chattings[1].content).dinner
                        res = {'message': {'text': menu}, 'keyboard': default_keyboard}

                elif chattings[2].content == "우정당 학생 식당":
                    woojung = Woojung.objects.get(name=chattings[1].content)
                    menu = Woojung_menu.objects.filter(day=content).get(type=woojung)

                    keyboard_ = {'type': 'buttons', 'buttons': default_button}
                    res = {'message': {'text': menu.menu + "(" + menu.price + ")"}, 'keyboard': keyboard_}

                elif chattings[2].content == "군자관":
                    if content == "중식":
                        menu = kunja_menu.objects.get(day=chattings[1].content).lunch
                        res = {'message': {'text': menu}, 'keyboard': default_keyboard}
                    else:
                        menu = kunja_menu.objects.get(day=chattings[1].content).dinner
                        res = {'message': {'text': menu}, 'keyboard': default_keyboard}

    return JsonResponse(res, status=200)



