def isZhChars(tok):    
    for x in tok:
        y = ord(x)
        rng1 = y >= 0x3400 and y <= 0x9fff
        rng2 = y >= 0xf900 and y <= 0xfaff
        if rng1 or rng2: continue
        else: return False
    return True