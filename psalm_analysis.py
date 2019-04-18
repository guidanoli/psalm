import sys

try:
    f = open("psalms_unformatted.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

v = s.split()
chars = [ chr(i) for i in range(0,256) ]
end = [ 0 for c in chars ]
for w in v:
    for i in range(0,len(chars)):
        if w[0] == chars[i]:
            end[i] += 1
indexes = list(range(len(end)))
indexes.sort(key=end.__getitem__)
sorted_chars = list(map(chars.__getitem__, indexes))
sorted_end = list(map(end.__getitem__, indexes))
for i in range(0,len(chars)):
    print(" "+sorted_chars[i]+"\t"+str(sorted_end[i]))
