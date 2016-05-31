import MySQLdb


db = MySQLdb.connect("localhost", "ps3robot", "RaspPS3Robot", "PS3Robot")
curs=db.cursor()

# note that I'm using triplle quotes for formatting purposes
# you can use one set of double quotes if you put the whole string on one line
try:
    curs.execute ("""INSERT INTO command (name, enmotors, report) values('monster', 0, 1)""")

    db.commit()
    print "Data committed"

except:
    print "Error: the database is being rolled back"
    db.rollback()
