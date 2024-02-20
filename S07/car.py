class car:
    #  init is when you move an object to a class.
    def __init__(self, brand): #self is a parameter of all methos and it is always a parameter. It is the object of a class
        self.car_brand = brand
        self.speed = 0


    def set_speed(self, speed):
        self.speed= speed

    def get_speed(self):
        return self.speed

    def get_brand_nationality(self):
        if self.car_brand == "Renault":
            return "France"
        elif self.car_brand == "Ferrari":
            return "Italy"


mycar = car("Renault")
print(mycar.get_speed())
mycar.set_speed(80)
print(mycar.get_speed())

print(mycar.get_brand_nationality())

yourcar = car("Ferrari")
print(yourcar.speed)
print(yourcar.get_speed())