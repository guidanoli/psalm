import sys

try:
    f = open("psalms_unformatted.txt","r")
    s = f.read()
    f.close()
except IOError:
    print("Couldn't read Psalms text file.")
    sys.exit()

before_and_after_words = []
untouched_words = []
removed_words = []
unwanted_chars = [str(num) for num in list(range(0,10))]
border_chars = [',','.',':',';','?','!','\'','(',')']
for w in s.split():
    old_w = w
    unwanted = False
    for c in unwanted_chars:
        if c in w:
            removed_words.append(w)
            unwanted = True
            break
    if not unwanted:
        for c in border_chars:
            w = w.strip(c)
        if old_w != w:
            before_and_after_words.append([old_w,w])
        else:
            untouched_words.append(w)
total = len(s.split())
modified = len(before_and_after_words)
untouched = len(untouched_words)
removed = len(removed_words)

print("%20s"%"total of words:","%10d"%total,"%10.2f%%"%(100))
print("%20s"%"modified words:","%10d"%modified,"%10.2f%%"%(100*modified/total))
print("%20s"%"untouched words:","%10d"%untouched,"%10.2f%%"%(100*untouched/total))
print("%20s"%"removed words:","%10d"%removed,"%10.2f%%"%(100*removed/total))

mod_w_count = {}
for mod_w in before_and_after_words:
    mod_w_before = mod_w[0]
    mod_w_after = mod_w[1]
    if not mod_w_after in mod_w_count:
        mod_w_count[mod_w_after] = [mod_w_before]
    elif not mod_w_before in mod_w_count[mod_w_after]:
        # different initial string to the same final string
        mod_w_count[mod_w_after].append(mod_w_before)

try:
    f = open("modified_words.txt","w")
    f.write("\n".join(["%20s "%k+str(len(v))+"\t"+" | ".join(v) for k,v, in mod_w_count.items()]))
    f.close()
except IOError:
    print("Could not write modified words file")
