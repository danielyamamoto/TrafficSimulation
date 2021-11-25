from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

from agents import TrafficLight, Vehicle
from schedule import RandomActivationByType

class StreetModel(Model):
    def __init__(self, nVehicles = 4, nLights = 2, size = 20):
        super().__init__()
        self.num_vehicles = nVehicles
        self.num_lights = nLights
        self.grid = SingleGrid(size, size, False)
        self.schedule = RandomActivationByType(self)

        self.datacollector = DataCollector(
            {
                "Vehicle": lambda m: m.schedule.get_type_count(Vehicle),
                "TrafficLight": lambda m: m.schedule.get_type_count(TrafficLight)
            }
        )
        
        # Create Vehicles
        for i in range(self.num_vehicles):
            x = self.random.randrange(20)
            y = self.random.randrange(20)
            v = Vehicle(i, (x, y), self)
            self.grid.place_agent(v, (x, y))
            self.schedule.add(v)

        # Create TrafficLights
        for i in range(self.num_vehicles, self.num_vehicles + self.num_lights):
            x = self.random.randrange(20)
            y = self.random.randrange(20)
            t = TrafficLight(i, (x, y),self)
            self.grid.place_agent(t, (x, y))
            self.schedule.add(t)

    def step(self):
    # Advances the model by one step
        print("Step")
        self.datacollector.collect(self)
        self.schedule.step()

    def run_model(self, step=200):
        for i in range(step):
            self.step()