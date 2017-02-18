from django.http import JsonResponse

from api.student_buttons import *
from api.skyrounge_buttons import *
from api.woojung_buttons import *
from api.kunja_buttons import *
from api.defaults import *

from api.models import Chatter,Chat
import json
from django.views.decorators.csrf import csrf_exempt

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

    if user.next_chat_code==0 :
        if "학생회관" == content:
            user.set_next_chat_code(1)
            res=select_student()

        elif "찬 스카이라운지" == content:
            user.set_next_chat_code(2)
            res=select_skyrounge()

        elif "우정당 학생 식당" == content:
            user.set_next_chat_code(3)
            res=select_woojung()

        elif "군자관" == content:
            user.set_next_chat_code(4)
            res=select_kunja()

    elif int(user.next_chat_code/10)==0 :
        if user.next_chat_code==1 :
            if "랜덤 메뉴" == content:
                user.set_next_chat_code(0)
                res=random_menu()

            elif "음식 종류" == content:
                user.set_next_chat_code(0)
                res=menu_kind()

            elif "음식 가격" == content:
                user.set_next_chat_code(10)
                res=menu_price()

            elif "메뉴 추천" == content:
                user.set_next_chat_code(11)
                res=recommend_menu()

            elif "인기 메뉴" == content:
                user.set_next_chat_code(0)
                res=best_menu()

        elif user.next_chat_code==2:
            user.set_next_chat_code(20)
            res=sky_lunch_or_dinner()

        elif user.next_chat_code==3:
            user.set_next_chat_code(30)
            res=select_day(content)

        elif user.next_chat_code==4:
            user.set_next_chat_code(40)
            res = sky_lunch_or_dinner()

    elif int(user.next_chat_code/100)==0 :
        if int(user.next_chat_code/10)==1:
            if user.next_chat_code%10==0:
                user.set_next_chat_code(0)
                res = select_menu_price(content)

            elif user.next_chat_code%10==1 :
                user.set_next_chat_code(0)
                res=select_recommend_menu(content)

        else :
            chatter = Chatter.objects.get(user_key=user_key)
            chattings = list(Chat.objects.filter(user=chatter).order_by("-created_date"))

            if int(user.next_chat_code/10)==2:
                if content == "중식":
                    res = sky_select_lunch(chattings[1].content)
                else:
                    res = sky_select_dinner(chattings[1].content)
                user.set_next_chat_code(0)

            elif int(user.next_chat_code / 10) == 3:
                res=menu_print(content,chattings[1].content)
                user.set_next_chat_code(0)

            elif int(user.next_chat_code / 10 )== 4:
                if content == "중식":
                    res = kunja_select_lunch(chattings[1].content)
                else:
                    res = kunja_select_dinner(chattings[1].content)
                user.set_next_chat_code(0)
    else:
        user.set_next_chat_code(0)

    return JsonResponse(res, status=200)



