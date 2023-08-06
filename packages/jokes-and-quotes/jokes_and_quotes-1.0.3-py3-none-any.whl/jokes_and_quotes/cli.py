import argparse
import json
import random
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

def print_quote_and_jokes():
  my_file = os.path.join(THIS_FOLDER, 'quotes.json')
  with open(my_file) as f:
    q = json.load(f)
  my_file = os.path.join(THIS_FOLDER, 'jokes.json')
  with open(my_file,'rb') as g:
    j = json.load(g)
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


def main():
    parser = argparse.ArgumentParser(description = "Jokes and Quotes")
    parser.add_argument("-gen",action='store_true',help = "Generates Jokes and Quotes")
    args = parser.parse_args()
    print_quote_and_jokes()
    
if __name__ == "__main__":
    main()