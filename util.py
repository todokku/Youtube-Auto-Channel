#functions I can use in more than one file
#(except I changed my code so I never use any of these in more than 1 file so its basically useless)
#(but I'm too lazy to change back)

import re


#if string contains regex the first match is returned, otherwise None is returned
def find_first(regex, string):
    matches = re.findall(regex, string)
    if len(matches) != 0:
        return matches[0]
    return None

#true if string contains regex
def contains(regex, string):
    return len(re.findall(regex, string)) != 0

#similar to find_first but with different arguments, return value does not include start or end
def parse(text, start, end = None):
    newtext = text[text.find(start)+len(start):]
    if end != None: #added this feature in sept 2016 so some older files might get fucked if I didn't do this right (but Im pretty sure I did)
        newtext = newtext[:newtext.find(end)]
    return newtext

