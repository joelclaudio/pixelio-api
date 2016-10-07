from .entities import Player

from .utils.coroutines import waitseconds
import random


class GameWorld(object):
    #object {location, size}
    players = []

    dimensions = (1200, 700)

    max_food = 100
    scheduled_food = 0
    food = []
    max_ttf = 120

    tasks = []

    def get_random_food(self):
        return (random.randrange(0, self.dimensions[0]), random.randrange(0, self.dimensions[1]), random.randint(0, 0xFFFFFF))

    def spawn_fruit(self):
        self.scheduled_food += 1
        for i in waitseconds(random.randrange(0, self.max_ttf)):
            yield None

        self.food.append(self.get_random_food())
        self.scheduled_food -= 1

    def vanish_food(self):
        while True:
            for i in waitseconds(random.randrange(0, 30)):
                yield None

            del self.food[random.randint(0, len(self.food))]

    def manage_food(self):
        while True:
            for i in range(len(self.food) + self.scheduled_food, self.max_food):
                self.tasks.append(self.spawn_fruit())

            yield None

    def start(self):
        self.tasks.append(self.manage_food())

    def update_tasks(self):
        for task in self.tasks:
            try:
                next(task)
            except StopIteration:
                self.tasks.remove(task)

    def tick(self):
        self.update_tasks()

    def update_world(self):
        pass