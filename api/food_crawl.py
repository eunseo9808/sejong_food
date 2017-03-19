# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url="http://m.sejong.ac.kr/front/cafeteria.do"

def save_data(num):
	if num==0 : 
		return get_student_data()
	elif num==2:
		return get_woojung_data()
	else :
		return get_sky_data(num)

def get_student_data():
	menu_str='· 치킨까스[3000]· 치킨가라아게동[3500]· 새우튀김알밥[3800]· 생선까스[3500]· 새우튀김우동[3500]· 어묵꼬치우동[3000]· 김치우동[2000]· 등심돈까스[4000]· 불닭치즈도리아[4500]· 카오팟무[3500]· 불닭비빔밥[3500]· 치즈불닭비빔밥[4000]· 매콤돈도리비빔밥[3500]· 치즈매콤돈도리비빔밥[4000]· 카오팟 무 곱빼기[4000]· 피자까스[4500]· 자장면[2000]· 만짜[3500]· 소금구이덮밥[3500]· 간장돼지불고기덮밥[3500]· 짬뽕[2500]· 짬짜면[3800]· 자장면 곱빼기[2500]· 짬뽕 곱빼기[3000]· 야채김밥[1200]· 치즈김밥[1400]· 참치김밥[2300]· 콩나물강된장비빔밥[1800]· 떡볶이[2500]· 치즈떡볶이[3000]· 떡만두국[3000]· 버섯육개장[3000]· 양푼이비빔밥[3000]· 참치마요비빔밥[3000]· 육회비빔밥[4500]· 라면[1800]· 떡라면[2000]· 치즈라면[2300]· 쌀국수[4500]· 참치마요비빔밥곱빼기[3500]· 잔치국수[2500]· 콜라[1000]· 환타포도[1000]· 스프라이트[1000]· 환타오렌지[1000]· 옛날칼국수[3000]· 순두부찌개[3500]· 치즈떡갈비덮밥[4000]· 환타파인애플[1000]· 에비카레동[4200]· 돈카츠카레동[4200]· 돈까스김치우동[4300]· 유부우동[1800]· 우삼겹된장찌개[4000]· 햄야채볶음밥[2500]· 햄야채볶음밥곱빼기[3000]· 소세지야채볶음밥[3500]· 소세지야채볶음밥곱빼기[4000]· 치킨볼야채볶음밥[3500]· 치킨볼야채볶음밥곱빼기[4000]· 불닭야채볶음밥[3500]· 불닭야채볶음밥곱빼기[4000]· 양념감자야채볶음밥[3500]· 양념감자야채볶음밥곱빼기[4000]· 함박스테이크야채볶음밥[3800]· 함박스테이크야채볶음밥곱빼기[4300]· 치즈오븐야채볶음밥[3800]· 매콤돈도리야채볶음밥[3500]· 매콤돈도리야채볶음밥곱빼기[4000]· 하와이안게살볶음밥[3800]· 하와이안게살볶음밥곱빼기[4300]'
	menus=menu_str.split('· ')
	menu_list=[]
	for menu in menus :
		menu_dict={}
		find_index=menu.find('[')
		menu_name=menu[:find_index]
		menu_price=menu[find_index+1: find_index+5]
		menu_dict['price']=menu_price
		menu_dict['menu']=menu_name
		menu_list.append(menu_dict)

	return menu_list

def get_sky_data(num):
	data={'type1' : str(num)}
	r = requests.post(url,data=data,allow_redirects=True)
	soup=BeautifulSoup(r.content,'lxml')
	menu_list=[]
	prev_menu_dict={}
	for menu in soup.find_all('tr'):
		menu_dict={}
		if int(menu['class'][0][5])%2 == 0 :
			prev_menu_dict['dinner']=menu.td.div.string.strip().replace("\"", "")
			menu_list.append(prev_menu_dict)
		else :
			menu_dict['day']=menu.find('th', rowspan='2').div.string
			lunch_str=menu.td.div.string.strip().replace("\"", "").replace("...", "\n")
			first_division = lunch_str.find(',')
			last_division = lunch_str.rfind(',')
			if first_division>=0 :
				menu_dict['lunch']=lunch_str[:first_division]+lunch_str[first_division+1:last_division]+lunch_str[last_division+1:]
			else :
				menu_dict['lunch']=lunch_str

			menu_dict['lunch']=menu_dict['lunch'].replace(',', '\n')






			prev_menu_dict=menu_dict
	return menu_list

def get_woojung_data():
	data={'type1' : '2'}
	woojung_list=[]
	r = requests.post(url,data=data,allow_redirects=True)
	soup=BeautifulSoup(r.content,'lxml')
	for corner in soup.find_all('div'):
		if 'h2' in corner['class'][0]:
#			print(corner.find_all('div', class_='article'))
			for tmp in corner.find_all('div'):
				if tmp['class'][0]=='article':
					article=tmp.div.table
					break

#			article=corner.find('div', class_="article").div.table
			corner_info=article.thead.tr.th.div
			corner_name=corner_info.strong.string
			oper_hour=corner_info.span.string
			woojung={}
			woojung['oper_hour']=oper_hour
			woojung['corner_name']=corner_name

			menu_list=[]
			menu_info=article.tbody
			for menu in menu_info.find_all('tr'):
				menu_dict={}
				menu_dict['day']=menu.th.div.string.strip()
				menu_name=menu.td.div.string.strip()
				
				price_division=menu_name.rfind('\n')
				menu_dict['menu']=menu_name[0:price_division]
				menu_dict['price']=menu_name[price_division+1:]
				menu_list.append(menu_dict)

			woojung['menu_info']=menu_list
			woojung_list.append(woojung)
	return woojung_list

