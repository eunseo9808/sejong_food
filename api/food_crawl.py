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
	menu_list=[]
	source_code=requests.get(url)
	plain_text=source_code.content
	soup=BeautifulSoup(plain_text,'lxml')

	for menu in soup.find_all("tr"):
		if 'seq' in menu['class'][0]:
			menu_dict={}
			menu_dict['menu']=menu.th.div.string
			menu_dict['price']=menu.td.div.string
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

