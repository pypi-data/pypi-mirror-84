import socket
import threading
import requests

votes = {"null": 0}

# Inputs will be from the Twitch Channel
class TwitchPlaysOnline:
	def __init__(self, SERVER, PORT, PASS, BOT, CHANNEL, OWNER, OPTIONS = []):
		self.SERVER = SERVER
		self.PORT = PORT
		self.PASS = PASS
		self.BOT = BOT
		self.CHANNEL = CHANNEL
		self.OWNER = OWNER
	
		self.message = ""
		user = ""
		irc = socket.socket()

		irc.connect((SERVER, PORT))
		irc.send((	"PASS " + PASS + "\n" +
					"NICK " + BOT + "\n" +
					"JOIN #" + CHANNEL + "\n").encode())

		for key in OPTIONS:
			if key not in votes.keys():
				votes[key] = 0
				print(key + " : " + str(votes[key]))

		def game_control():

			self.message

			while True:

				for key in votes:
					if ("play_" + key) == self.message.lower():
						votes[key] += 1
						print("voted for " + key)
						self.message = ""


		def twitch():

			global user
			self.message

			def join_chat():
				Loading = True
				while Loading:
					readbuffer_join = irc.recv(1024)
					readbuffer_join = readbuffer_join.decode()
					print(readbuffer_join)
					for line in readbuffer_join.split("\n")[0:-1]:
						print(line)
						Loading = loading_complete(line)

			def loading_complete(line):
				if("End of /NAMES list" in line):
					print("TwitchBot has joined " + CHANNEL + "'s Channel!")
					send_message(irc, "Hello World!")
					return False
				else:
					return True

			def send_message(irc, message):
				messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
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
			irc.send("CAP REQ :twitch.tv/tags\r\n".encode())
			while True:
				try:
					readbuffer = irc.recv(1024).decode()
				except:
					readbuffer = ""
				for line in readbuffer.split("\r\n"):
					if line == "":
						continue
					if "PING :tmi.twitch.tv" in line:
						print(line)
						msgg = "PONG :tmi.twitch.tv\r\n".encode()
						irc.send(msgg)
						print(msgg)
						continue
					else:
						try:
							user = get_user(line)
							message = get_message(line)
							print(user + " : " + message)
						except Exception:
							pass

		def start():
			t1 = threading.Thread(target = twitch)
			t1.start()
			t2 = threading.Thread(target = game_control)
			t2. start()	

		start()

	def vote_results(self):
		majority = "null"

		for key in votes:
			if votes[key] > votes[majority]:
				majority = key

		for key in votes:
			votes[key] = 0

		if majority == "null":
			return None

		return majority


# Inputs will be from the command line
class TwitchPlaysOffline:
	def __init__(self, SERVER, PORT, PASS, BOT, CHANNEL, OWNER, OPTIONS = []):
		self.SERVER = SERVER
		self.PORT = PORT
		self.PASS = PASS
		self.BOT = BOT
		self.CHANNEL = CHANNEL
		self.OWNER = OWNER

		self.message = ""
		user = ""

		for key in OPTIONS:
			if key not in votes.keys():
				votes[key] = 0
				print(key + " : " + str(votes[key]))

		def game_control():

			self.message

			while True:

				for key in votes:
					if ("play_" + key) == self.message.lower():
						votes[key] += 1
						print("voted for " + key)
						self.message = ""

					if "check" == self.message.lower():
						print(self.voteResults())
						self.message = ""

		def twitch():
			while True:
				self.message = input()

		def start():
			t1 = threading.Thread(target = twitch)
			t1.start()
			t2 = threading.Thread(target = game_control)
			t2. start()	

		start()

	def vote_results(self):
		majority = "null"

		for key in votes:
			if votes[key] > votes[majority]:
				majority = key
			votes[key] = 0

		if majority == "null":
			return None

		return majority	