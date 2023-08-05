import random

JOES_DICTIONARY = ["right", "awesome", "interesting", "cool"]

def generate(max_limit=4):
  try:
    max_limit = int(max_limit)
    
    if max_limit <= 0:
      raise ValueError

  except ValueError:

    raise ValueError("Make sure you enter an integer greater than 0")

  word = ""

  for i in range(max_limit):
    rand_word = random.choice(JOES_DICTIONARY)
    word += rand_word[0].upper() + rand_word[1:]

  return word

