import random
from mesa import Agent

class TrafficLight(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos_x = pos[0]
        self.pox_y = pos[1]
        self.state = self.setState()
        self.is_near = False
        self.is_color_selected = False
        self.timer = 20
    
    def setState(self):
        if self.pos_x == 8 or self.pos_x == 11:
            return "#FF0000"
        else:
            return "#00FF00"

    def change(self):
        if self.state == "#FF0000":
            self.timer = 20
            return "#00FF00"
        else:
            self.timer = 20
            return "#FF0000"

    def step(self):
        self.timer = self.timer - 1
        if self.timer == 0:
            self.state = self.change()

    def getColor(self):
        colors = ["#00FF00", "#FFFF00", "#FF0000"] # G, Y, R
        self.is_color_selected = True
        return random.choice(colors)
class Vehicle(Agent):
    def __init__(self, unique_id, pos, ori, model):
        super().__init__(unique_id, model)
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.ori_x = ori[0]
        self.ori_y = ori[1]
        self.prev_pos = (0,0)
        self.from_corner = False
        self.edge_move = (0,0)

    def boundaries(self, pos):
        return pos[0] >= 0 and pos[0] < self.model.size  and pos[1] >= 0 and pos[1] < self.model.size
    
    def pos_is_origin(self, pos):
        return pos == (10,0) or pos == (0,9) or pos == (9,19) or pos == (19,10)
    
    def corners(self, pos):
        if pos[0] == 0 and pos[1] == 0:
            move = (pos[0], pos[1]+1)
            self.edge_move = (0, 1)
        elif pos[0] == self.model.size-1 and pos[1] == 0:
            move = (pos[0]-1, pos[1])
            self.edge_move = (-1, 0)
        elif pos[0] == 0 and pos[1] == self.model.size-1:
            move = (pos[0]+1, pos[1])
            self.edge_move = (1, 0)
        else:
            move = (pos[0], pos[1]-1)
            self.edge_move = (0, -1)
        self.ori_x = self.edge_move[0]
        self.ori_y = self.edge_move[1]
        return move
        
        
    def newDirection(self, pos):
        x = pos[0]
        y = pos[1]
        
        if (x == 0 or x == self.model.size-1) and (y == 0 or y == self.model.size-1):
            return self.corners(pos)
        # X in range and Y on top
        if  0 <= pos[0] < self.model.size and pos[1] == self.model.size-1:
            x += 1
        # X in range and Y down
        elif 0 <= pos[0] < self.model.size and pos[1] == 0:
            x -= 1
        # Y in range and X right
        elif 0 <= pos[1] < self.model.size and pos[0] == self.model.size-1:
            y -= 1
        # Y in range and X left
        elif 0 <= pos[1] < self.model.size and pos[0] == 0:
            y += 1
        
        new_pos = (x,y)
        return new_pos
        
    def step(self):
        self.move()
    
    def move(self):
        new_pos = (self.pos[0] + self.ori_x, self.pos[1] + self.ori_y)
        
        if self.boundaries(new_pos) == False:
            new_pos = self.newDirection(self.pos)
            self.prev_pos = self.pos
    
        # Get neighbors of the new pos
        other_agents = self.model.grid.get_cell_list_contents(new_pos)
        # Check if there are any trafficlights
        trafficlights = [obj for obj in other_agents if isinstance(obj, TrafficLight)]
        # Check if there are any vehicles
        vehicles = [obj for obj in other_agents if isinstance(obj, Vehicle)]
            
        if len(vehicles) == 0 and len(trafficlights) == 0 and self.boundaries(new_pos) == True:
            if self.pos_is_origin(self.pos):
                rand = self.random.randint(0,1)
                if rand == 1:
                    new_dir = self.model.next_to_origin[self.pos]
                    if self.ori_x != new_dir[0] and self.ori_y != new_dir[1]:
                        self.ori_x = new_dir[0]
                        self.ori_y = new_dir[1]
                        self.model.grid.move_agent(self, (new_dir[2], new_dir[3]))
                else:
                    self.model.grid.move_agent(self, new_pos)
            else:
                self.prev_pos = self.pos
                self.model.grid.move_agent(self, new_pos)
        elif len(vehicles) != 0:
            return
        elif len(trafficlights) != 0:
            if trafficlights[0].state == "#FF0000":
                return
            else:
                self.prev_pos = self.pos
                self.model.grid.move_agent(self, new_pos)

                new_dir = [[0,1,10,9],[1,0,9,9],[0,-1,9,10],[-1,0,10,10]]
                rand = self.random.randint(0, 3)

                if self.ori_x != new_dir[rand][0] and self.ori_y != new_dir[rand][1]:
                    self.ori_x = new_dir[rand][0]
                    self.ori_y = new_dir[rand][1]
                    self.model.grid.move_agent(self, (new_dir[rand][2], new_dir[rand][3]))

        else:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

        if len(other_agents) >= 1:
            self.move()
            return