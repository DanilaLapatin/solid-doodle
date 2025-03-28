class Human:
    default_name = "def_name"
    default_age = 0
    def __init__(self,name = default_name, age = default_age, money, house):
        self.name = name
        self.age = age
        self.__money = money
        self.__house = house

    def info(self):
        print(f" name - {self.name}, age - {self.age}, money - {self.__money}, house - {self.__house}")

    @staticmethod
    default_info():
        print(f"default_name - {default_name}, default_age - {default_age}")
        
        
