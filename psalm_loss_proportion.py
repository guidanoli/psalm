import sys

try:
    f = open("psalms_unformatted.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

lines = s.split('\n')
words = []
unwanted_chars = [str(num) for num in list(range(0,10))]
border_chars = [',','.',':',';','?','!','\'','(',')']
for w in s.split():
    unwanted = False
    for c in unwanted_chars:
        if c in w:
            unwanted = True
            break
    if not unwanted:
        for c in border_chars:
            w = w.strip(c)
        words.append(w)

print("lines = ",str(lines)[:200])
print("words = ",str(words)[:200])
