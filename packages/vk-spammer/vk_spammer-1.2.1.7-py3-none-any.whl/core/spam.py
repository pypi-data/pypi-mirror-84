#!/usr/bin/python
# Author: https://vk.com/id181265169
# https://github.com/fgRuslan/vk-spammer

import vk, urllib.request, urllib.error, urllib.parse, json, random, time
import threading
import sys

username = input("Login: ")
password = input("Password: ")

url = "https://oauth.vk.com/token?grant_type=password&client_id=3697615&client_secret=AlVXZFMUqyrnABp8ncuU&username=%s&password=%s" % (username, password)

try:
    r = urllib.request.urlopen(url)
except urllib.error.HTTPError:
    print("�� ���������� �������������� (�������� ����������� ������� ����� ��� ������)")
    quit(1)

r = r.read()
token = json.loads(r)["access_token"] 
session = vk.Session(access_token = token)
vk = vk.API(session)

foo = [
	"hi",
	"2",
	"3",
	"fuck",
	"5"
]

victim = input("User id: ")

try:
	temp = int(victim)
except Exception as e:
	print("Resolving screen name...")
	r = vk.utils.resolveScreenName(screen_name = victim, v = 5.73)
	victim = r["object_id"]
	print("It is: " + victim)

r = vk.users.get(user_id = victim, fields = "id", v = 5.73)
r = r[0]["id"]

victim = r
class MainThread(threading.Thread):
	def run(self):
		print("-" * 60)
		while(True):
			try:
				msg = random.choice(foo)
				time.sleep(random.randint(1,3) + random.randint(1,4))
				time.sleep(random.randint(1,2) + random.randint(1,2))
				r = vk.messages.send(peer_id = victim, message = msg, v = 5.73)
				print("Sent ", msg)
			except Exception as e:
				print(e)
				pass

def main():
	try:
		thread = MainThread()
		thread.daemon = True
		thread.start()

		while thread.is_alive():
			thread.join(1)
	except KeyboardInterrupt:
		print("Ctrl+C pressed...")
		sys.exit(1)

main()