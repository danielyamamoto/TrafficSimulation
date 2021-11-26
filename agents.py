from mesa import Agent
import random

class TrafficLight(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = 1
        self.pox_y = 1
        self.state = self.getColor()
        self.timer = 10
    
    def change(self):
        if self.state == "#00FF00":
            self.state = "#FFFF00"
        elif self.state == "#FFFF00":
            self.state = "#FF0000"
        else:
            self.state = "#00FF00"
    
    def step(self):
        print("I'm a traffic light " + str(self.unique_id))
        self.timer = self.timer - 1
        self.change()

    def getColor(self):
        colors = ["#00FF00", "#FFFF00", "#FF0000"] # G, Y, R
        return random.choice(colors)

class Vehicle(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = 1
        self.pox_y = 1

    def step(self):
        print("I'm a vehicle " + str(self.unique_id))
    
    def move(self):
        pass