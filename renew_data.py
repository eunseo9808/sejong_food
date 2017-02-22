import requests
import time
from threading import Thread
url='http://sejong.unifox.kr/save_all'

def timer():
	while True:
		response = requests.get(url)
		print(response.text)
		time.sleep(1)

background_thread = Thread(target=timer, args=())
background_thread.start()

