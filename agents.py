from mesa import Agent

class TrafficLight(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = 1
        self.pox_y = 1
        self.state = "Green"
        self.timer = 10
    
    def change(self):
        if self.timer > 6:
            self.state = "Green"
            print(self.state)
        elif self.timer > 3:
            self.state = "Yellow"
        else:
            self.state = "Red"
    
    def step(self):
        print("I'm a traffic light " + str(self.unique_id))
        self.timer = self.timer - 1
        self.change()

class Vehicle(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = 1
        self.pox_y = 1

    def step(self):
        print("I'm a vehicle " + str(self.unique_id))
    
    def move(self):
        pass