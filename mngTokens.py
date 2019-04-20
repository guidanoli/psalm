# Token Manager
# guidanoli

from mngSettings import getSetting

TKNLIST_PATH = getSetting("tknlistpath")
TKNCURR_PATH = getSetting("tokenpath")

def formatLabel( label ):
    # make safe filename out of label
    return "".join([c for c in label if not c in ['=','\n']]).strip()

def getPartsFromLine( l ):
    parts = [p.strip() for p in l.split("=")]
    assert(len(parts)==2),"Incorrect token list syntax."
    return parts

def getTokenLabel( part ):
    return part[0]

def getTokenValue( part ):
    return part[1]

def addTokenToList( label, tkn ):
    try:
        f = open(TKNLIST_PATH,"r")
        tkn_list = [t for t in f]
        f.close()
    except FileNotFoundError:
        f = open(TKNLIST_PATH,"w")
        f.write(label+'='+tkn)
        f.close()
        return True
    except IOError:
        print("Error while trying read tknlist.")
        return False

    altered = False
    
    for index, t in enumerate(tkn_list):
        parts = getPartsFromLine(t)
        curr_value = getTokenValue(parts)
        curr_label = getTokenLabel(parts)
        if curr_label == label:
            # do not show token or ask to overwrite
            print("A token with that label already exists.")
            return False
        if curr_value == tkn:
            # if you have the token, you can rename it
            print("A token with that value already exists.")
            print("Current name:",curr_label)
            rename = input("Would you like to rename it (y/n)? ")
            if len(rename)>0 and rename[0].lower() == 'y':
                tkn_list[index] = label + '=' + curr_value
                altered = True

    if altered:
        try:
            f = open(TKNLIST_PATH,"w")
            f.write("\n".join(tkn_list))
            f.close()
        except IOError:
            print("Error while trying write tknlist.")
            return False
    else:
        try:
            f = open(TKNLIST_PATH,"a")
            if len(tkn_list) > 0:
                f.write('\n')
            f.write(label+'='+tkn)
            f.close()
        except IOError:
            print("Error while trying append tknlist.")
            return False
        
    return True    

def deleteTokenFromList( tkn ):
    try:
        f = open(TKNLIST_PATH,"r")
        tkn_list = [t for t in f]
        f.close()
    except FileNotFoundError:
        print("Token list not found")
        return False
    except IOError:
        print("Error while trying read tknlist.")
        return False

    found = False

    for t in tkn_list:
        parts = getPartsFromLine(t)
        curr_value = getTokenValue(parts)
        if curr_value == tkn:
            tkn_list.remove(t)
            found = True
            break

    if found:
        try:
            f = open(TKNLIST_PATH,"w")
            f.write("\n".join(tkn_list).strip())
            f.close()
        except IOError:
            print("Error while trying write tknlist.")
            return False
    else:
        print("Unexpected error. Token not found in list")
        return False

    return True

def getCurrentToken():
    # returns dict with current token if found
    # <dict> { "ok" : boolean }
    # if ok == True, <dict> also has "token" : string
    try:
        f = open(TKNCURR_PATH,"r")
        t = f.read().strip()
        f.close()
    except IOError:
        print("Could not read token file.")
        return {"ok":False}
    for invalid_char in [' ','=','\n']:
        if invalid_char in t:
            print("Incorrect token file syntax.")
            return {"ok":False}
    return {"ok":True,"token":t}

def saveAsCurrentToken( tkn ):
    # overwrites token.tk with tkn
    try:
        f = open(TKNCURR_PATH,"w")
        f.write(tkn)
        f.close()
    except IOError:
        return False
    return True

def getTokenList():
    # returns token list
    # [ [lbl1,tk1], [lbl2,tk2], [lbl3,tk3] ... ]
    try:
        f = open(TKNLIST_PATH,"r")
    except FileNotFoundError:
        print("Token list not found. Creating one...\n")
        try:
            f = open(TKNLIST_PATH,"w")
            f.write("")
            f.close()
        except IOError:
            print("Error while trying write tknlist.")
            return False
        return []
    except IOError:
        print("Error while trying read tknlist.")
        return []
    tkns = []
    for t in f:
        parts = getPartsFromLine(t)
        tkns.append(parts)
    f.close()
    return tkns

def printTokensIndexes( tkns ):
    # prints token labels and their indexation in file
    print("index\ttoken label")
    print("-------------------")
    for i in range(len(tkns)):
        print("[{}]\t{}".format(i+1,getTokenLabel(tkns[i])))
    print()

def getTokenFromList( tkns, index ):
    # returns token value from list tkns in index
    # <string> token
    return getTokenValue(tkns[index-1])

def getTokenLabelFromValue( tkn ):
    # returns dict with current token label if found
    # <dict> { "ok" : boolean }
    # if ok == True, <dict> also has "label" : string
    tkn_list = getTokenList()
    for p in tkn_list:
        if getTokenValue(p) == tkn:
            return {"ok":True,"label":getTokenLabel(p)}
    return {"ok":False}

def launch( cmd ):
    print()
    if( cmd == 'ts' ):
        #select token
        tkns = getTokenList()
        printTokensIndexes(tkns)
        if len(tkns) == 0:
            print("No tokens registered.")
        else:
            print("Function: SELECT")
            index = input("Token index: ")
            assert(index.isdigit()),"Index should be numeric."
            index_num = int(index)
            assert(index_num > 0 and index_num <= len(tkns)),"Invalid index."
            t = getTokenFromList(tkns,index_num)
            if saveAsCurrentToken(t):
                print("Token selected successfully.")
            else:
                print("Could not select token.")
    elif( cmd == 'tr' ):
        #register token
        label = formatLabel(input("Name your token: "))
        tkn = input("Paste your token: ")
        print()
        if addTokenToList( label, tkn ):
            print("Token registered successfully.")
    elif( cmd == 'td' ):
        #delete token
        tkns = getTokenList()
        printTokensIndexes(tkns)
        if len(tkns) == 0:
            print("No tokens registered.")
        else:
            print("Function: DELETE")
            index = input("Token index: ")
            assert(index.isdigit()),"Index should be numeric."
            index_num = int(index)
            assert(index_num > 0 and index_num <= len(tkns)),"Invalid index."
            t = getTokenFromList(tkns,index_num)
            if deleteTokenFromList( t ):
                print("Token deleted from list.")
    elif( cmd == 'tc' ):        
        #current token
        t_ret = getCurrentToken()
        t_ok = t_ret["ok"]
        if t_ok:
            tkn = t_ret["token"]
            l_ret = getTokenLabelFromValue(tkn)
            l_ok = l_ret["ok"]
            if l_ok:
                label = l_ret["label"]
                print("Current token:",label)
            else:
                print("Could not find current token label in list")
        else:
            print("Could not get current token.")
    else:
        print(cmd+" not recognized as command.")
    print()

