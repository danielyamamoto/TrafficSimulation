from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents import TrafficLight, Vehicle
from schedule import RandomActivationByType

class StreetModel(Model):
    def __init__(self, nVehicles = 4, nLights = 4, nSize = 20):
        super().__init__()
        self.num_vehicles = nVehicles
        self.num_lights = nLights
        self.size = nSize
        self.grid = MultiGrid(nSize, nSize, False)
        self.schedule = RandomActivationByType(self)

        self.datacollector = DataCollector(
            {
                "Vehicle": lambda m: m.schedule.get_type_count(Vehicle),
                "TrafficLight": lambda m: m.schedule.get_type_count(TrafficLight)
            }
        )
        
        origin_pos = [[10,0],[0,9],[9,19],[19,10]]
        orient = [[0,1],[1,0],[0,-1],[-1,0]]
        # Create Vehicles
        for i in range(self.num_vehicles):
            rand = self.random.randint(0, 3)
            x1 = origin_pos[rand][0]
            y1 = origin_pos[rand][1]
            x2 = orient[rand][0]
            y2 = orient[rand][1]
            v = Vehicle(i, (x1, y1), (x2, y2), self)
            self.grid.place_agent(v, (x1, y1))
            self.schedule.add(v)

        pos_lig = [[8,9],[9,11],[10,8],[11,10]]
        count = 0
        # Create TrafficLights
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            x = pos_lig[count][0]
            y = pos_lig[count][1]
            t = TrafficLight(i, (x, y),self)
            count += 1
            self.grid.place_agent(t, (x, y))
            self.schedule.add(t)

    # Advances the model by one step
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        ps = []
        for i in range(self.num_vehicles):
            xy = self.schedule.agents[i].pos
            p = [xy[0], xy[1], 0]
            ps.append(p)
        return ps

    def run_model(self, step=20):
        for i in range(step):
            print(self.step())