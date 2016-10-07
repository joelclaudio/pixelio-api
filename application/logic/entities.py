class Player(object):
    position = (0, 0)

    alive = False

    size = 10

    def eat(self, food_value):
        self.size += food_value

    def radius(self):
        return self.size/2 # Find a better size formula