import csv

# pass all numbers as strings

def getValues(type, quality, parameter):
    # ducts hard-coded, as are only type with different format
    if type == "duct":
        if parameter == 1: # parameter for duct is inner diameter
            return 228
        elif parameter == 1.25:
            return 414
        elif parameter == 1.5:
            return 1.5
        else: return 0

    with open(f"{type}_table.csv", 'r', encoding = 'utf-8-sig') as fid:
        read = csv.reader(fid)
        vals = list(read)
    
    column = vals[0].index(quality)
    row = [rws[-1] for rws in vals].index(parameter)

    return [vals[1][column], vals[row][column]]