import sqlite3, sys

db = sqlite3.connect('sv.db')
dbc = db.cursor()

try:
    dbc.execute('''CREATE TABLE pamIDs
                    (svdID qty, pamID text, StreetAddress text, coords text)''')
except sqlite3.OperationalError:
    print("Table already exists; continuing...")

db.close()

def createRow(pamID, StreetAddress, coords):
    db = sqlite3.connect('sv.db')
    dbc = db.cursor()
    for row in dbc.execute('SELECT * FROM pamIDs ORDER BY svdID'):
        i = row[0]
    try:
        i += 1
    except NameError:
        i = 1
    newRow = [(i, pamID, StreetAddress, coords)]
    dbc.executemany('INSERT INTO pamIDs VALUES (?,?,?,?)', newRow)
    db.commit()
    dbc.close()

def FindPamID(y):
    db = sqlite3.connect('sv.db')
    dbc = db.cursor()
    for x in dbc.execute('SELECT pamID FROM pamIDs'):
        if x[0] == y:
            print("Found {}".format(y))
            dbc.close()
            return True
    dbc.close()
    return False

# if __name__ == '__main__':
#     x = FindPamID('t2TlAVwDPpGKW2qB_lReMA')
#     print(x)
## Only use this to troubleshoot