# -*- coding: utf-8 -*- 
from django.shortcuts import render
from api.food_crawl import save_data
from api.models import *
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def save_all(request):
	save_student_data(request)
	save_skyrounge_data(request)
	save_woojung_data(request)
	save_kunja_data(request)
	return HttpResponse("완료", status=200)

@csrf_exempt
def save_student_data(request):
	menu_list=save_data(0)
	for menu in menu_list:
		if menu['menu']=='': break
		try :
			tmp=Student_union_menu.objects.create(name=menu['menu'], price=menu['price'])
			tmp.save()
		except IntegrityError:
			pass
	return HttpResponse("완료", status=200)

@csrf_exempt
def save_skyrounge_data(request):
	menu_list=save_data(1)
	Skyrounge_menu.objects.all().delete()
	for menu in menu_list:
		try :
			tmp=Skyrounge_menu.objects.create(day=menu['day'], lunch=menu['lunch'], dinner=menu['dinner'])
			tmp.save()
		except IntegrityError:
			pass
	return HttpResponse("완료", status=200)

@csrf_exempt
def save_woojung_data(request):
	cource_list=save_data(2)
	Woojung_menu.objects.all().delete()
	for cource in cource_list:
		try:
			tmp=Woojung.objects.create(name=cource['corner_name'], running_time=cource['oper_hour'])
		except IntegrityError:
			tmp=Woojung.objects.get(name=cource['corner_name'])
		for menu in cource['menu_info']:
			if not tmp.menus.filter(day=menu['day']).count()==0:
				break;
			menu_tmp=Woojung_menu.objects.create(price=menu['price'], day=menu['day'], menu=menu['menu'])
			menu_tmp.save()
			tmp.menus.add(menu_tmp)
		tmp.save()
	return HttpResponse("완료", status=200)

@csrf_exempt
def save_kunja_data(request):
	menu_list=save_data(3)
	kunja_menu.objects.all().delete()
	for menu in menu_list:
		try:
			tmp=kunja_menu.objects.create(day=menu['day'], lunch=menu['lunch'], dinner=menu['dinner'])
			tmp.save()
		except IntegrityError:
			pass

	return HttpResponse("완료", status=200)

@csrf_exempt
def get_student_data(request):
	menus=Student_union_menu.objects.all()
	menu_list=[]
	for menu in menus:
		menu_dict={}
		menu_dict['name']=menu.name
		menu_dict['price']=menu.price
		menu_list.append(menu_dict)
	return HttpResponse(json.dumps(menu_list), status=200)

@csrf_exempt
def get_skyrounge_data(request):
	menus=Skyrounge_menu.objects.all()
	menu_list=[]
	for menu in menus:
		menu_dict={}
		menu_dict['day']=menu.day
		menu_dict['dinner']=menu.dinner
		menu_dict['lunch']=menu.lunch
		menu_list.append(menu_dict)
	return HttpResponse(json.dumps(menu_list), status=200)	

@csrf_exempt
def get_kunja_data(request):
	menus=kunja_menu.objects.all()
	menu_list=[]
	for menu in menus:
		menu_dict={}
		menu_dict['day']=menu.day
		menu_dict['dinner']=menu.dinner
		menu_dict['lunch']=menu.lunch
		menu_list.append(menu_dict)
	return HttpResponse(json.dumps(menu_list), status=200)

@csrf_exempt
def get_woojung_data(request):
	menus=Woojung.objects.all()
	menu_list=[]
	for menu in menus:
		menu_dict={}
		menu_dict['name']=menu.name
		menu_dict['running_time']=menu.running_time
		tmp=menu.menus.all()
		real_menu=[]
		for tmp_menu in tmp:
			real_menu_dict={}
			real_menu_dict['day']=tmp_menu.day
			real_menu_dict['name']=tmp_menu.menu
			real_menu_dict['price']=tmp_menu.price
			real_menu.append(real_menu_dict)
		menu_list['menus']=real_menu
		menu_list.append(menu_dict)
	return HttpResponse(json.dumps(menu_list), status=200)

from multiprocessing import Process
from api.views import save_all
import time

def periodic_save(request):
	p = Process(target=timer, args=(request,))
	p.start()
	return HttpResponse("완료", status=200)


def timer(request):
	while True:
		time.sleep(1)
		save_all(request)
		print("삐용삐용")