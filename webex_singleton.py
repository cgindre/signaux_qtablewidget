# -*- coding: utf-8 -*-

class  Singleton (object):
    instance = None       # Attribut statique de classe
    def __new__(cls):
        "méthode de construction standard en Python"
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

# Utilisation
monSingleton1 =  Singleton()
monSingleton2 =  Singleton()

# monSingleton1 et monSingleton2 renvoient à la même instance
assert monSingleton1 is monSingleton2
