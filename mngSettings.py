# Settings Manager
# guidanoli

DEFAULT_STGS = {
    "qtwords": "30",
    "qtmarks": "true",
    "psalmspath": "verses.txt",
    "tknlistpath": "tknlist.tk",
    "tokenpath": "token.tk",
}

SETTINGS_PATH = "psalm.cfg"
TYPE_STR = type("")
TYPE_LIST = type([])

def _validateFilename( filename , extension = "" ):
  from re import match
  return match("[^<>:\"\\/|?*]+"+extension,filename).groups() != None

def _isBoolean( value ):
  return value in ["true", "false"]

def _validateEdit( label , new_value ):
  # add here the requirements for the settings
  if label == "tknlistpath":
    return _validateFilename(new_value,".tk")
  elif label == "tokenpath":
    return _validateFilename(new_value,".tk")
  elif label == "psalmspath":
    return _validateFilename(new_value,".txt")
  elif label == "qtwords":
    return new_value.isdigit()
  elif label == "qtmarks":
    return _isBoolean(new_value)

def _validateString( s ):
  # returns True if OK, False if invalid
  assert(type(s)==TYPE_STR)
  return not( True in [ (c in ['=','\n']) for c in s ] )

def _writeSettings( settings_list ):
  assert(type(settings_list)==TYPE_LIST)
  try:
    f = open(SETTINGS_PATH,"w")
    f.write( "\n".join([ "=".join(s) for s in settings_list ]) )
    f.close()
  except IOError:
    print("Could not write cfg file.")
    return False
  return True

def _getSettingsList():
  # returns settings as
  # <dict> "ok":boolean
  # if ok == True , TYPE_LIST:list
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
  if type(s) != TYPE_LIST:
    print("Setting isn't table.")
    return False
  if len(s) != 2:
    print("Setting table size is wrong.")
    return False
  if True in [ type(x) != TYPE_STR for x in s]:
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
  assert(type(settings_list)==TYPE_LIST)
  assert(type(label)==TYPE_STR)
  for s in settings_list:
    if _getSettingLabel(s) == label:
      return _getSettingValue(s)
  return None

def _printSettings( settings_list ):
  assert(type(settings_list)==TYPE_LIST)
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
  assert(type(settings_list)==TYPE_LIST)
  assert(type(label)==TYPE_STR)
  assert(type(new_value)==TYPE_STR)
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

def getSetting( label ):
  # returns setting value through label
  # returns None if error occurrs
  assert(type(label)==TYPE_STR)
  slist = _getSettingsList()
  if slist == None:
    return None
  return _getSettingValueFromLabel(slist,label)

def launch( cmd ):
  assert(type(cmd)==TYPE_STR)
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

