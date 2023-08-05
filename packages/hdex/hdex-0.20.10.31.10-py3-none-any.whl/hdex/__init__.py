def crunch(la, lb, allstr, sml, fname):
  word = [""]
  l = la
  while (l<=lb):
    for strg in allstr:
      n = l - len(strg)
      p = int(pow(10,n))
      for m in range(0,p):
        a = len(str(m))
        stnum = ""
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + sml + strg.lower())
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + strg.lower() + sml + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + sml + strg.capitalize())
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + strg.capitalize() + sml + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(strg.lower() + stnum + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + strg.lower())
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(strg.capitalize() + stnum + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + strg.capitalize())
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + sml + strg.upper())
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        if a>(n-1):
          continue
        for x in range(0,n-(a+1)):
          stnum = stnum + str(0)
        word.append(stnum + strg.upper() + sml + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(strg.upper() + stnum + str(m))
      for m in range(0,p):
        stnum = ""
        a = len(str(m))
        for x in range(0,n-a):
          stnum = stnum + str(0)
        word.append(stnum + str(m) + strg.upper())
    l += 1
  word.pop(0)
  if isinstance(fname, str):
    f = open(fname, "a")
    for w in word:
      f.write(w + "\n")
    f.close()
  else:
    return word

