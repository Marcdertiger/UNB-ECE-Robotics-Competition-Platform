import MySQLdb


db = MySQLdb.connect("localhost", "ps3robot", "RaspPS3Robot", "PS3Robot")
curs=db.cursor()

# note that I'm using triplle quotes for formatting purposes
# you can use one set of double quotes if you put the whole string on one line
try:
#    curs.execute ("""INSERT INTO command (name, enmotors, report) values('monster', 0, 1)""")
    curs.execute ("""INSERT INTO command values('walle', CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 10, 100, 100, 100, 100, 1)""")

    db.commit()
    print "Data committed"

except:
    print "Error: the database is being rolled back"
    db.rollback()
