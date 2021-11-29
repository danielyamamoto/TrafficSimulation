import random
from mesa import Agent

class TrafficLight(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = pos[0]
        self.pox_y = pos[1]
        self.state = "#FFFF00"
        self.is_near = False
        self.is_color_selected = False
        self.timer = 10
    
    def change(self):
        if self.is_near:
            if self.is_color_selected:
                self.chanceColor()
            else:
                self.state = self.getColor()
        else:
            possible_steps = self.model.grid.get_neighborhood(self.pos, moore = False, include_center = False)
            for step in possible_steps:
                other = self.model.grid.get_cell_list_contents(step)
                if len(other) >= 1:
                    self.is_near = True
                    break

    def step(self):
        self.timer = self.timer - 1
        self.change()

    def getColor(self):
        colors = ["#00FF00", "#FFFF00", "#FF0000"] # G, Y, R
        self.is_color_selected = True
        return random.choice(colors)

    def chanceColor(self):
        if self.state == "#00FF00":
            self.state = "#FFFF00"
        elif self.state == "#FFFF00":
            self.state = "#FF0000"
        else:
            self.state = "#00FF00"

class Vehicle(Agent):
    def __init__(self, unique_id, pos, ori, model):
        super().__init__(unique_id, model)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.ori_x = ori[0]
        self.ori_y = ori[1]

    def boundaries(self, pos):
        return pos[0] > 0 and pos[0] < self.model.size - 1 and pos[1] > 0 and pos[1] < self.model.size - 1

    def step(self):
        self.move()
    
    def move(self):
        new_pos = (self.pos[0] + self.ori_x, self.pos[1] + self.ori_y)
        # Get neighbors of the new pos
        other_agents = self.model.grid.get_cell_list_contents(new_pos)
        # Check if there are any trafficlights
        trafficlights = [obj for obj in other_agents if isinstance(obj, TrafficLight)]
        # Check if there are any vehicles
        vehicles = [obj for obj in other_agents if isinstance(obj, Vehicle)]
        
        if len(vehicles) == 0 and len(trafficlights) == 0 and self.boundaries(new_pos) == True:
            self.model.grid.move_agent(self, new_pos)
        elif len(vehicles) != 0:
            return
        elif len(trafficlights) != 0:
            if trafficlights[0].state == "#FF0000":
                return
            else:
                self.model.grid.move_agent(self, new_pos)

                new_dir = [[0,1,10,9],[1,0,9,9],[0,-1,9,10],[-1,0,10,10]]
                rand = self.random.randint(0, 3)

                if self.ori_x != new_dir[rand][0] and self.ori_y != new_dir[rand][1]:
                    self.ori_x = new_dir[rand][0]
                    self.ori_y = new_dir[rand][1]
                    self.model.grid.move_agent(self, (new_dir[rand][2], new_dir[rand][3]))
        else:
            self.model.num_vehicles -= 1
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

        if len(other_agents) >= 1:
            self.move()
            return