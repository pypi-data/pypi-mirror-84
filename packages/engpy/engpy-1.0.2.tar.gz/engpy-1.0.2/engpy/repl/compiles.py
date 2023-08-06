import re
brackets = re.compile('[\-\+\w\d\.]+\([\w\d\-\+\^]+\)')
inbrackets = re.compile('\([\w\d\-\+\^]+\)')
