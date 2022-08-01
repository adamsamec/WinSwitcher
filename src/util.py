# Utility functions module.

import unicodedata as ud

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