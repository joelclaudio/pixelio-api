from .entities import Player 

from .utils.coroutines import waitseconds
import random


class GameWorld(object):
    #object {location, size}
    players = []

    dimensions = (1280, 800)

    max_food = 100
    scheduled_food = 0
    food = []

    tasks = []

    def get_random_position(self):
        return (random.randrange(0, self.dimensions[0]), random.randrange(0, self.dimensions[1]))

    def spawn_fruit(self):
        self.scheduled_food += 1
        for i in waitseconds(random.randint(0, 10)):
            yield None

        self.food.append(self.get_random_position())
        self.scheduled_food -= 1

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

        pass

    def update_world(self):
        pass