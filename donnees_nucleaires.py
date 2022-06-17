# -*- coding: utf-8 -*-

import os
import sys
import sqlite3

DATABASE_NAME = "Jeff.db"

def init_cursor():
    """retourne Connection.cursor avec la base de donnees "Jeff.db" """
    sqliteConnection = sqlite3.connect(DATABASE_NAME)
    # Creating cursor object using connection
    cursor = sqliteConnection.cursor()
    return cursor

def list_fields_from_table(fields, table):
    """Retourne liste de champs issus d'une table"""

    # Chemin à fixer en relatif pour la suite ...
    print("os.getcwd() =", os.getcwd())
    os.chdir(r"C:\Users\cygindre\Documents\GitHub\erastem3\ihm\src\calcul")
    print("os.getcwd() =", os.getcwd())
    #cursor = init_cursor()
    #cursor.execute("SELECT " + fields + " FROM " + table)
    sqliteConnection = sqlite3.connect('Jeff.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT " + "symbole" + " FROM " + "Elements")
    list_fields = cursor.fetchall()
    # Transforme une liste de tuples d'objets en liste d'objet(tuple[0])
    list_fields = [ field[0] for field in list_fields ]
    return list_fields

class TableFlux:
    def __init__(self):
        self.data = dict()
        self.cle1 = 'Rapide'
        self.cle2 = 'Thermique'
        self.data[self.cle1] = [0.0]
        self.data[self.cle2] = [0.0]
        self.unite_flux = "n/cm²/s"
        self.cles = self.data.keys() # cleTriees -> keys ne donnent pas les cles triees
        self.temps=['T0']
        self.colT0=0
        self.sommes=[0.0]
        self.isfiltre=False
        # self.setConfigAdv(copy.deepcopy(self.ws.ini.configFiltreDef))#preinitialisation du filtre au comportement par defaut


    def setConfigAdv(self, cfgAdv):
        self.adv=cfgAdv
        self.majConfigAdv()


    def getConfigAdv(self):
        return self.adv


    def majConfigAdv(self):
        if self.isfiltre:
            self.advRedef=[]
            for ki in self.adv:
                if ki in ['PaI','THE']:
                    #self.data[ki]=[1.0]*len(self.temps)
                    for mat in self.adv[ki]:
                        if not self.adv[ki][mat][1]:
                            self.advRedef.append(mat)
                            if mat not in self.data:
                                self.data[mat]=[1.0]*len(self.temps)
            self.cleTriees=[self.cle1, self.cle2]+self.advRedef


if __name__ == "__main__":
    list_symbole = list_fields_from_table("symbole", "Elements")
    print("list_symbole = ", list_symbole)
