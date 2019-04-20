import sys, re, random

phrase_size = 30

try:
    f = open("psalms_vers.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

psalm = s.replace('\n',' ').split()
dictionary = {}
for i in range(0, len(psalm)-1):
  if not psalm[i] in dictionary:
    dictionary[psalm[i]] = [psalm[i+1]]
  else:
    dictionary[psalm[i]].append(psalm[i+1])

first_word = random.choice(psalm)
while not first_word[0].isupper():
  first_word = random.choice(psalm)

psalm_phrase = [ first_word ]
for i in range(0, phrase_size):
  last_word = psalm_phrase[-1]
  next_word = random.choice(dictionary[last_word])
  psalm_phrase.append(next_word)
  
phrase = " ".join(psalm_phrase)
if not '.' in phrase:
  phrase = phrase + '.'
else:
  while not '.' in psalm_phrase[-1]:
    psalm_phrase.pop()
  phrase = " ".join(psalm_phrase)

print()
print(phrase)
