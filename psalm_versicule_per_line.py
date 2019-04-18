import sys, re

try:
    f = open("psalms_unformatted.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

pat = re.compile("\d+:\d+")
vers = []
old_end = 0
for n in pat.finditer(s):
    v = s[old_end:n.start()].strip()
    if len(v) > 0:
        vers.append(v.replace('\n',' '))
    old_end = n.end()
if len(s[old_end:].strip()) > 0:
    vers.append(s[old_end:].strip().replace('\n',' '))

try:
    f = open("psalms_vers.txt","w")
    s = f.write('\n'.join(vers))
    f.close()
except IOError:
    print("Couldn't write formatted Psalms text file.")
    sys.exit()
    
