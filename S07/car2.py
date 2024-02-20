class car:
    #  init is when you move an object to a class.
    def __init__(self, brand, speed = 0): #self is a parameter of all methos and it is always a parameter. It is the object of a class
        self.car_brand = brand
        self.speed = speed


    def set_speed(self, speed):
        self.speed = speed

class Ferrari(car):
    pass

mycar = car("Renault")
yourcar = Ferrari("Ferrari")
print(yourcar.car_brand)
yourcar.set_speed(120)
print(yourcar.speed)