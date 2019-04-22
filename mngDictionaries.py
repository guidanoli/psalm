import utils

""" Dictionary module """

def MakePhrase( dictionary_path, word_limit = 30, uppercase = True, end_chars = []):
  """ Generates a random phrase from dictionary
  dictionary_path : str ~ *.dict
    - path of dictionary file
  word_limit : int > 1
    - maximum length if end_char was found with word_limit words
    - minimum length if end_char wasn't found yet with word_limit words
  uppercase : boolean
    - let first char be in uppercase
  end_chars : list of chars
    - list of chars that will terminate the phrase
    - if empty, phrase will end in whatever char
  Returns phrase or None if IO error occurrs
  """
  
  from random import choice

  dictionary = {}
  try:
    f = open(dictionary_path, "r")
    for w in f:
      w_lst = w.split()
      dictionary[w_lst[0]] = w_lst[1:]
    f.close()
  except IOError:
    print("Couldn't read file.")
    return None

  words = list(dictionary.keys())
  first_word = choice(words)
  if uppercase:
    while not first_word[0].isupper():
      first_word = choice(words)

  phrase_vec = [first_word]
  end_found = True if len(end_chars) == 0 else False
  end_pos = 0
  while word_limit > 0 or not end_found:
    last_word = phrase_vec[-1]
    next_word = choice(dictionary[last_word])
    for c in end_chars:
      if c in next_word:
        end_found = True
    phrase_vec.append(next_word)
    word_limit -= 1

  return " ".join(phrase_vec)

def MakeDict( input_path, output_path = None ):
  """ Generates dictionary out of text file
  input_path : str ~ *.txt
    - path of text file
  output_path : str ~ *.dict
    - path of dictionary file
    - if null, will inherit input file's name
  Returns output file name or None if an IO error occurrs
  """
  
  from re import match
  
  assert(utils.validateFilename(input_path,".txt"))
  if output_path == None or output_path == "":
    filename = match("(.*).txt",input_path).groups()[0]
    output_path = filename+".dict"
  else:
    assert(utils.validateFilename(output_path, ".dict"))
  
  # read file
  try:
    f = open(input_path, "r")
    s = f.read()
    f.close()
  except IOError:
    print("Couldn't read file "+input_path+".")
    return None
  
  # dictionary
  words = s.replace('\n',' ').split()
  dictionary = {}
  for i in range(0, len(words)-1):
    if not words[i] in dictionary:
      dictionary[words[i]] = [words[i+1]]
    else:
      dictionary[words[i]].append(words[i+1])
  
  dict_string = '\n'.join(w+' '+' '.join(nw) for w, nw in dictionary.items())
  
  # write file
  try:
    f = open(output_path, "w")
    f.write(dict_string)
    f.close()
  except IOError:
    print("Couldn't write file "+output_path+".")
    return None
    
  return output_path
