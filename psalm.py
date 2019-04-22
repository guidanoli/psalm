import json, facebook
from mngSettings import getSetting

TKNCURR_PATH = getSetting("tokenpath")
DICTPATH = getSetting("dictpath")
WORD_LIMIT = getSetting("wordlimit")
UPPERCASE = getSetting("upperfirst")
ENDCHARS = getSetting("endchars")
QUATOTAION_MARKS = getSetting("quotmarks")

def GetPhrase() -> str:
  """ Generates a random phrase from dictionary
  Returns phrase or None if IO error
  """
  from mngDictionaries import MakePhrase
  phrase = MakePhrase(DICTPATH, WORD_LIMIT, UPPERCASE, ENDCHARS)
  if phrase != None and QUATOTAION_MARKS:
    phrase = '"' + phrase + '"'
  return phrase

def IsBotMessage(msg: str) -> bool:
  if QUATOTAION_MARKS:
    from re import match
    m = match("\A\".*\"\Z", msg)
    return m != None and m.groups() != None
  else:
    return True

def PsalmBot( event, context ) -> None:
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
  msg = GetPhrase()
  if msg == None:
    return
  
  try:
      post = graph.put_object("me", "feed", message=msg)
      print("Message posted:\n"+msg)
      print(json.dumps(post))
  except facebook.GraphAPIError:
      print("An error occurred while trying to post to feed.")
      return

  return
