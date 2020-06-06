import re


xx = "aaaaa"
x = re.search('aa', xx).span()
print( x )