class Configuration_Erastem():
    """
    Classe gérant la configuration d'Erastem
    C'est un singleton
    """
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            cls._sealed = False
        return cls.instance

test1 = Configuration_Erastem()
print("id(test1) = ", id(test1))
test2 = Configuration_Erastem()
print("id(test2) = ", id(test2))
print(test1 is test2)


