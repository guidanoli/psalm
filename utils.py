
" PUBLIC FUNCTIONS "

def isList(value) -> bool:
  """ Checks if value is list """
  return type(value) == type([])

def isStringBoolean(value) -> bool:
  """ Checks if value is either 'true' or 'false' """
  return type(value) == type('') and value in ["true", "false"]

def isStringInteger(value) -> bool:
  """ Checks if value is a string and contains only numbers """
  return type(value) == type('') and value.isdigit()

def isString(value) -> bool:
  """ Checks if value is string """
  return type(value) == type('')

def containsChars(string: str, *chars) -> bool:
  """ Checks if string contains any of the characters in chars """
  for c in chars:
    if c in string:
      return True
  return False

def validateFilename(filename: str, extension: str="") -> bool:
  """ Checks if filename contains expected extension """
  from re import match
  return type(filename) == type('') and match("[^<>:\"\\/|?*]+"+extension, filename).groups() != None
