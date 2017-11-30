import sqlite3

connection=sqlite3.connect("Students Database.db")
conn = connection.cursor()

cmd = "create table  if not exists StudentA("\
 	"id int,"\
 	"name varchar(50),"\
 	"roll varchar(50),"\
 	"gender varchar(5),"\
 	"dept varchar(10),"\
 	"lastSeen text,"\
 	"attendenceCount int"\
 ")"

conn.execute(cmd)
print 'Database table created succesfully'
connection.close()
