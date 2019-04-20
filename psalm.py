import json, facebook
from mngSettings import getSetting

TKNCURR_PATH = getSetting("tokenpath")
PSLAMS_PATH = getSetting("psalmspath")
N_OF_WORDS = int(getSetting("qtwords"))
QUATOTAION_MARKS = True if bool(getSetting("qtmarks")) else False

def GetPsalm( filename , maxNumWords ):
  """ Generates a random psalm passage with
  a maximum number of words by reading every
  versicle of the Psalms book (one per line)
  
  Returns phrase or None if IO error """
  from random import choice  
  try:
      f = open(filename, "r")
      s = f.read()
      f.close()
  except IOError:
      print("Couldn't read Pslams.")
      return None

  psalm = s.replace('\n',' ').split()
  dictionary = {}
  for i in range(0, len(psalm)-1):
    if not psalm[i] in dictionary:
      dictionary[psalm[i]] = [psalm[i+1]]
    else:
      dictionary[psalm[i]].append(psalm[i+1])

  first_word = choice(psalm)
  while not first_word[0].isupper():
    first_word = choice(psalm)

  psalm_phrase = [ first_word ]
  for i in range(0, maxNumWords):
    last_word = psalm_phrase[-1]
    next_word = choice(dictionary[last_word])
    psalm_phrase.append(next_word)
    
  phrase = " ".join(psalm_phrase)
  if not '.' in phrase:
    phrase = phrase + '.'
  else:
    while not '.' in psalm_phrase[-1]:
      psalm_phrase.pop()
    phrase = " ".join(psalm_phrase)
  
  if QUATOTAION_MARKS:
    return '"'+phrase+'"'
  else:
    return phrase
    
def IsBotMessage( msg ):
  if QUATOTAION_MARKS:
    from re import match
    m = match("\A\".*\"\Z", msg)
    return m != None and m.groups() != None
  else:
    return True

def PsalmBot( event, context ):
  # Main function
  # Parameters are ignored
  # No return value
  print("Bot running...")
  token = ""
  try:
      f = open(TKNCURR_PATH, "r")
      token = f.readline()
      f.close()
  except IOError:
      print("Could not read token file.")
      return

  graph = facebook.GraphAPI(access_token=token)
  print("Generating message...")
  msg = GetPsalm(PSLAMS_PATH, N_OF_WORDS)
  if msg == None:
    return
  while len(msg) < 5:
    # THRESHHOLD
    msg = GetPsalm(PSLAMS_PATH, N_OF_WORDS)
    if msg == None:
      return
  
  try:
      post = graph.put_object("me", "feed", message=msg)
      print("Message posted: \""+msg+"\".")
      print(json.dumps(post))
  except facebook.GraphAPIError:
      print("An error occurred while trying to post to feed.")
      return

  return
