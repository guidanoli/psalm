import json, facebook, sys
from psalm import IsBotMessage
from mngSettings import getSetting

TKNCURR_PATH = getSetting("tokenpath")

removal_log = []

def Centralize( w ):
  if "\n" in w.strip("\n"):
    v = w.split("\n")
    new_v = ""
    for vi in v:
      new_vi = Centralize(vi)
      new_v += new_vi + "\n"
    return new_v[:-1]
  else:
    s = ( 80 - len(w) ) // 2
    if s >= 0:
      return s*" "+w
    return 0

def LoadingBar( done , total ):
  bar_length = 60
  done_qt = int((done/total)*bar_length)
  not_done_qt = bar_length - done_qt
  bar = done_qt * "#" + not_done_qt * "-"
  return bar

def GetLog( limit ):
  output = ""
  for i in range(limit):
    if i < len(removal_log):
      output += removal_log[i]
    output += "\n"
  return output

def DisplayLoadingScreen( done , total ):
  output = "\n"*11
  output += Centralize("Loading") + "."*(done%3) + "\n"*2
  output += Centralize(LoadingBar(done,total))
  output += "\n"*2
  output += Centralize(GetLog(9))
  output += "\n"
  print(output)

def CleanScreen( ):
  print("\n"*25)

def ConstrainString( s, tam, dots ):
  if len(s) <= tam:
    return s
  if tam < dots:
    dots = 0
  return s[:tam-dots]+"."*dots

token = ""
try:
  f = open(TKNCURR_PATH,"r")
  token = f.readline()
  f.close()
except IOError:
  print("\nNo token found. Aborting.\n")
  sys.exit()
    
graph = facebook.GraphAPI(access_token=token)
posts = graph.get_connections("me","feed")["data"]
rem_count = 0
done_count = 0
total_count = len(posts)
    
for p in posts:
  post_id = p["id"]
  done_count += 1
  last_bit = post_id.split('_')[-1]
  msg = "[{}] ".format(last_bit)
  if ("message" in p):
    constr_message = ConstrainString(p["message"],20,3)
    if IsBotMessage(p["message"]):
      try:
        graph.delete_object(post_id)
        msg += "\"" + constr_message + "\" deleted"
        rem_count += 1
      except facebook.GraphAPIError:
        #move on trying to delete the rest...
        msg += " Error while trying to remove"
        pass
    else:
      msg += "\"" + constr_message + "\" isn't a bot message"
  else:
    msg += " Does not carry a message"
  removal_log = [msg] + removal_log
  DisplayLoadingScreen(done_count,total_count)

if rem_count > 0:
  CleanScreen()
    
print("\nRemoved posts: {}\nTotal # of posts: {}\n".format(rem_count,total_count))
