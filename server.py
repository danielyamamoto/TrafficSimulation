from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

from agents import TrafficLight, Vehicle
from model import StreetModel

def StreetModel_portrayal(agent):
    if agent is None:
        return

    portrayal = { }

    if type(agent) is TrafficLight:
        portrayal["Layer"] = 1
        portrayal["Color"] = agent.state
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Vehicle:
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#69C7B7"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = CanvasGrid(StreetModel_portrayal, 20, 20, 600, 600)

model_params = {
    "nVehicles": UserSettableParameter("slider", "Number of vehicles", 10, 1, 20)
}

server = ModularServer(
    StreetModel, [canvas_element], "Traffic Simulation", model_params
)
server.port = 8521