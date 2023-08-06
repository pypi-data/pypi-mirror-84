import json
import random


with open('quotes.json') as f:
  q = json.load(f)


with open('jokes.json','rb') as g:
  j = json.load(g)


def print_quote_and_jokes():
  stop = len(q)
  start = 0
  x = random.randint(start, stop)
  print("Jokes and Quotes\n")
  print("Quote : ")
  print(q[x]["text"])
  print("- " + q[x]["author"])

  stop = len(j)
  x = random.randint(start, stop)
  print("\nJoke : ")
  print(j[x]["body"])