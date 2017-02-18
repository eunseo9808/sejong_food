import requests
import time

url='http://sejong.unifox.kr/save_all'

while True:
	response = requests.get(url)
	print(response.text)
	time.sleep(3600)

