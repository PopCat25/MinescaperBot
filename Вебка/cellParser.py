
def cellParser (elementClassLine):
    if elementClassLine[2] == "hd_closed" and len(elementClassLine) == 3 :
        return "*"
    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "hd_flag":
        return "F"
    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "hd_flag":
        return "x"
    elif elementClassLine[2] == "hd_opened":
        return str(elementClassLine[3]).split("e")[1]