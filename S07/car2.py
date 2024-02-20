class vehicle:   #this is the MOTHER class
    def set_speed(self, speed):
        self.speed = speed

class car(vehicle):
    #  init is when you move an object to a class.
    def __init__(self, brand, speed = 0): #self is a parameter of all methos and it is always a parameter. It is the object of a class
        self.car_brand = brand
        self.speed = speed


class Ferrari(car):
    def __init__(self):
        #call the init of the mother class
        super().__init__("Ferrari", 100) #con el super llamamos al init del car class
        self.music = "clasic"
    def make_cabrio(self):
        self.speed = 20
        self.music = "loud"
        return "Wow"

mycar = car("Renault")
yourcar = Ferrari()   #no ponemos FERRARI dentrpo del parentesis xqe ya hemos creado un init en el class ferrari
print(yourcar.car_brand)
yourcar.set_speed(120)
print(yourcar.speed)  #ferrari no tiene speed definido pero car si entcs si en ferrari no esta, va a car a mirar y sino a vehicle porq dependen d ellas
print(yourcar.make_cabrio(), "and music is", yourcar.music, "and speed is", yourcar.speed)