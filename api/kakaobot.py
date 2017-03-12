from django.http import JsonResponse

from api.student_buttons import *
from api.skyrounge_buttons import *
from api.woojung_buttons import *
from api.kunja_buttons import *
from api.defaults import *

from api.models import Chatter,Chat
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def friend(request):
    res = {}
    request_str = request.body.decode("utf-8")
    request_json = json.loads(request_str)
    user_key = request_json['user_key']


    if request.method=='POST':
        user = Chatter.objects.get_or_create(user_key=user_key)
        res = {"message": {"text": "안녕하세요!"}, 'keyboard': default_keyboard}

    return JsonResponse(res, status=200)

@csrf_exempt
def friend_delete(request,user_key):
    try:
        user = Chatter.objects.get(user_key=user_key)
        user.delete()
    except ObjectDoesNotExist:
        pass

    return JsonResponse({},status=200)


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

    user,created=Chatter.objects.get_or_create(user_key=user_key)

    chats=Chat.objects.filter(user=user).order_by("-created_date")
    if chats.count()>=5 :
        chats.last().delete()


    if chats.count()>0 :
        if chats.first().content==content :
            if user.next_chat_code == 0:
                user.chat.all().delete()
            else :
                user.set_next_chat_code(0)
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

        elif "Info" == content:
            user.set_next_chat_code(0)
            res = {"message": {"text": "버그 발생시 eunseo9808@naver.com으로 메일 주세요\n"
                                       "소스 : https://github.com/eunseo9808/sejong_food"}, 'keyboard': default_keyboard}

    elif int(user.next_chat_code/10)==0 :
        if user.next_chat_code==1 :
            if "메뉴 추천" == content:
                user.set_next_chat_code(0)
                res=random_menu()

            elif "음식 종류" == content:
                user.set_next_chat_code(0)
                res=menu_kind()

            elif "음식 가격" == content:
                user.set_next_chat_code(10)
                res=menu_price()

            elif "메뉴 추천하기" == content:
                user.set_next_chat_code(11)
                res=recommend_menu()

            elif "인기 메뉴" == content:
                user.set_next_chat_code(0)
                res=best_menu()
            else :
                user.set_next_chat_code(0)

        elif user.next_chat_code==2:
            user.set_next_chat_code(20)
            res=sky_lunch_or_dinner()

        elif user.next_chat_code==3:
            user.set_next_chat_code(30)
            res=select_day(content)
            if res['message']['text']=='해당하는 메뉴가 없습니다.' :
                user.set_next_chat_code(0)

        elif user.next_chat_code==4:
            user.set_next_chat_code(40)
            res = sky_lunch_or_dinner()
        else :
            user.set_next_chat_code(0)

    elif int(user.next_chat_code/100)==0 :
        if int(user.next_chat_code/10)==1:
            if user.next_chat_code%10==0:
                user.set_next_chat_code(0)
                res = select_menu_price(content)

            elif user.next_chat_code%10==1 :
                user.set_next_chat_code(0)
                res=select_recommend_menu(content)
            else :user.set_next_chat_code(0)

            if res['message']['text'] == '옳지 않은 데이터입니다.':
                user.set_next_chat_code(0)
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
                user.set_next_chat_code(0)
                res=menu_print(content,chattings[1].content)

            elif int(user.next_chat_code / 10 )== 4:
                user.set_next_chat_code(0)
                if content == "중식":
                    res = kunja_select_lunch(chattings[1].content)
                else:
                    res = kunja_select_dinner(chattings[1].content)

    else:
        user.set_next_chat_code(0)

    return JsonResponse(res, status=200)



