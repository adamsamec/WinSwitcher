from pynput.keyboard import Key, KeyCode
import unicodedata as ud

# Wrapper class for key objects  which allows for comparision of those key objects when they are defined only using the virtual key codes.
class MyKey:

  # Initializes the object.
  def __init__(self, key):
    self.key = key

  # Returns the hash derived from the 'vk' or 'char' attributes of the inner key object, or falls back to the hash of the inner key object if those attributes are not set.
  def __hash__(self):
    if hasattr(self.key, 'vk')and not (self.key.vk is None):
      return int(self.key.vk)
    if hasattr(self.key, 'char')and not (self.key.char is None):
      return ord(self.key.char)
    return self.key.__hash__()

  # Returns the result of the equality comparison with the given object.
  def __eq__(self, other):
    if isinstance(other, MyKey):
      return MyKey.isEqual(self.key, other.key)
    if isinstance(other, (Key, KeyCode)):
      return MyKey.isEqual(self.key, other)

  # Returns the result of the inequality comparison with the given object.
  def __neq__(self, other):
    return not (self == other)

  # Returns the result of the equality comparison of the two given key objects in a way such that the comparison  works if the keys are defined only by the virtual key codes.
  @staticmethod
  def isEqual(a, b):
    if hasattr(a, 'vk') and hasattr(b, 'vk') and not (a.vk is None) and not (b.vk is None):
      # The keys are defined using the virtual key codes, so use them for the comparison
        return a.vk == b.vk
        # Otherwise, fall back to key objects comparison
    return a == b

# Utility functions:

# Returns the base character of the given char, by removing any diacritics like accents or curls and strokes and the like.
def removeDiacriticsFromChar(char):
  desc = ud.name(char)
  cutoff = desc.find(' WITH ')
  if cutoff != -1:
    desc = desc[:cutoff]
    try:
      char = ud.lookup(desc)
    except KeyError:
      pass # removing "WITH ..." produced an invalid name
  return char

# Returns the given text with diacritics removed.
def removeDiacritics(text):
  result= ''
  for char in text:
    result += removeDiacriticsFromChar(char)
  return result

  # Returns whether the given search text is found in the given target text. The search is not diacritics and case sensitive.
def isFoundNotSensitive(searchText, targetText):
  searchText = searchText.lower()
  targetText = targetText.lower()
  findInOrig = targetText.find(searchText)
  findInBase = removeDiacritics(targetText).find(searchText)
  result = (findInOrig >= 0) or (findInBase >= 0)
  return result