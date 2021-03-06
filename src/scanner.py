"""This is the main engine of the program"""

import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading
import time


class Scanner:

	def __init__(self, url, payload):
		self.target_url = url
		self.payload = payload

	def extract_forms(self):
		response = requests.get(self.target_url)
		soup_obj = BeautifulSoup(response.text, 'lxml')
		list_forms = soup_obj.findAll('form')
		return list_forms

	def inject_payload(self):
		list_forms = self.extract_forms()
		list_of_tasks = []

		#t1 = time.time()

		for form in list_forms:
			self.scanLoad(form)
			# t = threading.Thread(target=self.scanLoad, args=(form,))
			# t.start()
			# list_of_tasks.append(t)

		# for task in list_of_tasks:
		# 	task.join()

		#t2 = time.time()

		#print('[!] Completed in {}'.format(t2-t1))

	def scanLoad(self, form):
		input_box = form.findAll('input')
		post_data = {}

		for i in range(len(self.payload)):
			for box in input_box:
				box_name = box.get('name')
				type_box = box.get('type')
				input_value = box.get('value')
				if type_box == 'text':
					input_value = self.payload[i]

				post_data[box_name]=input_value

			result = requests.post(self.target_url,data=post_data)

			if self.payload[i] in result.text:
				print('\n[!] VULNERABILITY DETECTED!--> ' + self.payload[i])
				print('[*] LINK IS ',self.target_url)
				print('---FORM DATA---')
				print(form)
				print('\n')
			else:
				print("[+] OK. \n")
