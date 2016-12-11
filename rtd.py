import random

def rollDie(number):
    roll = 0
	for i in range(number):
        roll += random.randint(1,20)
    return roll