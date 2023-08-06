import socket
import threading
import time
import re

import requests

class TwitchPlaysBase:
	"""
	DONT USE THIS CLASS UNLESS YOU ARE EXTEDNING IT
	this is an abstract class that handles a lot of the logic. a subclass can
	implement it by calling this classes init at the begining of their init.
	calling start_threads at the end of its init. and implementing get_messages.

	VOTE_INTERVAL how many seconds in between vote counts
	OPTIONS an array of options for input
	    eg ["1", "walk"] would mean people can type play_1 and play_walk
	"""
	def __init__(self, VOTE_INTERVAL=5, OPTIONS=[], **kwargs):
		self.VOTE_INTERVAL = VOTE_INTERVAL
		self.result = None
		self.votes = {"null": 0}
		for key in OPTIONS:
			if key not in self.votes.keys():
				self.votes[key] = 0
				print(key + " : " + str(self.votes[key]))
		self.pattern = re.compile(r"play_(\w+)")

	def start_threads(self):
		"""called at the end of subclass __init__"""
		t1 = threading.Thread(target = self.get_messages)
		t1.start()
		t2 = threading.Thread(target = self.count_votes_loop)
		t2.start()


	def handle_message(self, user, message):
		print(user + " : " + message)
		match = self.pattern.match(message.lower())

		if not match:
			return
		key = match.group(1)
		self.votes[key] +=1
		print("voted for " + key)

	def get_messages(self):
		"""
		this method gets the messages from the source (twitch or command line or
		whatever) and calls handle_message with the username and message. since this
		this should be implemented by the subclass
		"""
		raise NotImplementedError

	def count_votes_loop(self):
		"""does a voting round every VOTE_INTERVAL seconds"""
		while True:
			time.sleep(self.VOTE_INTERVAL)
			self.count_votes()

	def count_votes(self):
		"""function that determines the result of a voting round"""
		print("counting votes, ", self.votes)
		majority = "null"

		for key in self.votes:
			if self.votes[key] > self.votes[majority]:
				majority = key

		for key in self.votes:
			self.votes[key] = 0

		if majority == "null":
			return None

		self.result = majority

	def vote_result(self):
		"""
		this can be called in an update loop and will return results if they exist.
		if the voting period isn't over, it will return None
		"""
		result = self.result
		self.result = None
		return result


class TwitchPlaysOnline(TwitchPlaysBase):
	"""Inputs will be from the Twitch Channel"""
	def __init__(self, SERVER="irc.twitch.tv", PORT=6667,
		     PASS=None, BOT=None, CHANNEL=None, OWNER=None,
		     **kwargs):
		super().__init__(**kwargs)
		self.SERVER = SERVER
		self.PORT = PORT
		self.PASS = PASS
		self.BOT = BOT
		self.CHANNEL = CHANNEL
		self.OWNER = OWNER

		self.irc = socket.socket()

		self.irc.connect((SERVER, PORT))
		self.irc.send(("PASS " + PASS + "\n" +
			  "NICK " + BOT + "\n" +
			  "JOIN #" + CHANNEL + "\n").encode())
		self.start_threads()


	def get_messages(self):
		def join_chat():
			Loading = True
			while Loading:
				readbuffer_join = self.irc.recv(1024)
				readbuffer_join = readbuffer_join.decode()
				print(readbuffer_join)
				for line in readbuffer_join.split("\n")[0:-1]:
					print(line)
					Loading = loading_complete(line)

		def loading_complete(line):
			if("End of /NAMES list" in line):
				print("TwitchBot has joined " + self.CHANNEL + "'s Channel!")
				send_message(self.irc, "Hello World!")
				return False
			else:
				return True

		def send_message(irc, message):
			messageTemp = "PRIVMSG #" + self.CHANNEL + " :" + message
			irc.send((messageTemp + "\n").encode())

		def get_user(line):
			#global user
			colons = line.count(":")
			colonless = colons-1
			separate = line.split(":", colons)
			user = separate[colonless].split("!", 1)[0]
			return user

		def get_message(line):
			#global message
			try:
				colons = line.count(":")
				self.message = (line.split(":", colons))[colons]
			except:
				self.message = ""
			return self.message

		def console(line):
			if "PRIVMSG" in line:
				return False
			else:
				return True

		join_chat()
		self.irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
		while True:
			try:
				readbuffer = self.irc.recv(1024).decode()
			except:
				readbuffer = ""
			for line in readbuffer.split("\r\n"):
				if line == "":
					continue
				if "PING :tmi.twitch.tv" in line:
					print(line)
					msgg = "PONG :tmi.twitch.tv\r\n".encode()
					self.irc.send(msgg)
					print(msgg)
					continue
				else:
					try:
						self.handle_message(get_user(line), get_message(line))
					except Exception as e:
						print("ERROR: ", e)


class TwitchPlaysOffline(TwitchPlaysBase):
	"""Inputs will be from the command line"""
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.start_threads()

	def get_messages(self):
		while True:
			self.handle_message("console", input())
