# FFR120 Homework 4
# Problem 13.1: Prisoner's dilemma with multiple rounds
# Author: Jamie Santos
# Date: 12/1/21


# Create a "prisoner" class
class Prisoner:
	def __init__(self):
		self.strategy = True	# Cooperate by default
		self.last_opponent = True
		self.score = 0

	# If switchNum turns have passed, prisoner  becomes a snitch
	def strategize(self,other,rnd,switchNum):
		#if rnd < switchNum and other.strategy:
		if rnd < switchNum and self.last_opponent:
			print("cooperate: round: " + str(rnd) + " trigger: " + str(switchNum))
			self.strategy = True
		else:
			print("betray: round: " + str(rnd) + " trigger: " + str(switchNum))
			self.strategy = False

	def get_sentence(self, t, r, p, s, other):
		if not self.strategy and other.strategy:
			print("T")
			self.score = t
		elif self.strategy and other.strategy:
			print("R")
			self.score = r
		elif not self.strategy and not other.strategy:
			print("P")
			self.score = p
		elif self.strategy and not other.strategy:
			print("S")
			self.score = s
		return self.score

	def track_opponent(self,last_opponent):
		self.last_opponent = last_opponent

