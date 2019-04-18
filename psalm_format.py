import sys

try:
    f = open("psalms_unformatted.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

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
        
w_len = len(words)
s_len = len(s.split())
print("%20s"%"All:","%10d"%s_len,"%10.2f%%"%(100.00))
print("%20s"%"Filtered:","%10d"%w_len,"%10.2f%%"%(100*w_len/s_len))
print("%20s"%"Loss:","%10d"%(s_len-w_len),"%10.2f%%"%(100*(1-w_len/s_len)))
