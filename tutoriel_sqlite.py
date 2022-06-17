# coding: utf-8

import sqlite3 as lite
import sys


connect = None
print("type(connect) = ", type(connect))

# Variable connect qui va permettre de se connecter à la base de données.
connect = lite.connect('Jeff.db')

print("type(connect) = ", type(connect))

# Le curseur est utilisé pour gérer la base de données.
curseur = connect.cursor()

print("type(curseur) = ", type(curseur))

# Instructions pour connaître version de sqlite3
curseur.execute('SELECT SQLITE_VERSION()')
data = curseur.fetchone()[0]
print("Sqlite vesrion {}".format(data))

print("Les différentes tables sont : ", curseur.execute('TABLES'))
#curseur.executive("CREATE TABLE inventaire(id INT, name TEXT, price FLOAT)")