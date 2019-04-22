# Settings Manager
# guidanoli

import utils

DEFAULT_STGS = {
    "dictpath": "dictionary.dict",
    "endchars": ".!?)",
    "psalmspath": "verses.txt",
    "wordlimit": "30",
    "quotmarks": "true",
    "tknlistpath": "tknlist.tk",
    "tokenpath": "token.tk",
    "upperfirst": "true",
}

SETTINGS_PATH = "settings.cfg"

""" VALIDATION FUNCTIONS """

def _validateEdit(label: str, new_value: str) -> bool:
  """ Validates new_value for a give setting """
  if label == "tknlistpath":
    return utils.validateFilename(new_value,".tk")
  elif label == "tokenpath":
    return utils.validateFilename(new_value,".tk")
  elif label == "psalmspath":
    return utils.validateFilename(new_value,".txt")
  elif label == "dictpath":
    return utils.validateFilename(new_value,".dict")
  elif label == "wordlimit":
    return utils.isStringInteger(new_value)
  elif label == "quotmarks":
    return utils.isStringBoolean(new_value)
  elif label == "upperfirst":
    return utils.isStringBoolean(new_value)
  elif label == "endchars":
    return True
  
def _validateString( s ):
  """ Returns validity of string s """
  return not utils.containsChars(s,'\n','=')

""" SETTINGS FUNCTIONS """

def _writeSettings( settings_list ):
  assert(utils.isList(settings_list))
  try:
    f = open(SETTINGS_PATH,"w")
    f.write( "\n".join([ "=".join(s) for s in settings_list ]) )
    f.close()
  except IOError:
    print("Could not write cfg file.")
    return False
  return True

def _getSettingsList():
  """ Returns settings list or None if IO Error or if file inexists """
  try:
    f = open(SETTINGS_PATH,"r")
    l = [ p.strip().split('=') for p in f ]
    f.close()
  except FileNotFoundError:
    print("Could not find cfg file. Creating default cfg file...")
    if _generateSettingsFile():
      print("The default cfg file was created successfully. Re-run me.")
    return None
  except IOError:
    print("Could not read cfg file.")
    return None
  return l

def _generateSettingsFile():
  # generates cfg file according to default settings
  # returns True if successful and False if error occurred on I/O
  return _writeSettings([ [k,v] for k,v in DEFAULT_STGS.items() ])

def _validateSettingFormat( s ):
  if not utils.isList(s):
    print("Setting isn't table.")
    return False
  if len(s) != 2:
    print("Setting table size is wrong.")
    return False
  if True in [ not utils.isString(x) for x in s]:
    print("Settings variables aren't string.")
    return False
  if False in [ _validateString(x) for x in s]:
    print("Settings variables are invalid.")
    return False
  return True

def _getSettingLabel( s ):
  assert(_validateSettingFormat(s))
  return s[0]

def _getSettingValue( s ):
  assert(_validateSettingFormat(s))
  return s[1]

def _formatSetting( label, new_value ):
  return [label,new_value]

def _getSettingValueFromLabel( settings_list , label ):
  assert(utils.isList(settings_list))
  assert(utils.isString(label))
  for s in settings_list:
    if _getSettingLabel(s) == label:
      return _getSettingValue(s)
  return None

def _printSettings( settings_list ):
  assert(utils.isList(settings_list))
  print("{:<20}{:<20}".format("Label","Value"))
  print("-"*40)
  for s in settings_list:
    if not _validateSettingFormat(s):
      return
    print("{:<20}{:<20}".format(_getSettingLabel(s),_getSettingValue(s)))
  if len(settings_list) == 0:
    print("No settings found.")

def _editSetting( settings_list , label , new_value ):
  # saves the new value in the cfg file
  assert(utils.isList(settings_list))
  assert(utils.isString(label))
  assert(utils.isString(new_value))
  if len(new_value) == 0 or not _validateString(new_value):
    print("\nInvalid string for new value.")
    return False
  lbl_list = [ _getSettingLabel(s) for s in settings_list ]
  if not label in lbl_list:
    print("\nUnexpected error occurred. Label not in list.")
    return False
  if not _validateEdit(label,new_value):
    print("\nNew value does not meet label requirementes. Check README.")
    return False
  idx = lbl_list.index(label)
  settings_list[idx] = _formatSetting(label,new_value)
  return _writeSettings(settings_list) 

""" PUBLIC FUNCTIONS """

def getSetting(label: str):
  """ Returns setting value if it exists """
  assert(utils.isString(label))
  slist = _getSettingsList()
  if slist == None:
    return None
  value = _getSettingValueFromLabel(slist,label)
  if label in ["tknlistpath", "tokenpath", "psalmspath","dictpath"] :
    return value
  elif label in ["quotmarks","upperfirst"]:
    return value == "true"
  elif label == "wordlimit":
    return int(value)
  elif label == "endchars":
    return [ c for c in value ]
  else:
    return None

def launch(cmd: str) -> None:
  """ Executes command """
  assert(utils.isString(cmd))
  if cmd == 'sd':
    #resets settings to default
    if _generateSettingsFile():
      print("Settings were set to default.")
  elif cmd in ['se','sv']:
    #print settings list
    slist = _getSettingsList()
    if slist == None:
      print("Could not print settings list.\n")
      return
    _printSettings(slist)
    if cmd == 'se':
      print()
      lbl = input("Label: ")
      curr_value = _getSettingValueFromLabel(slist,lbl)
      if curr_value == None:
        print("Label not recognized.\n")
        return
      print("Current value for '"+lbl+"': "+curr_value)
      new_value = input("Setting new value: ")
      if _editSetting(slist,lbl,new_value):
        print("New value set successfully.")
  else:
    print("Command '"+cmd+"' not recognized.")
  print()

