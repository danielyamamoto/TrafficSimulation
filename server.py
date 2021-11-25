from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from agents import TrafficLight, Vehicle
from model import StreetModel

def StreetModel_portrayal(agent):
    if agent is None:
        return

    portrayal = { }

    if type(agent) is TrafficLight:
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#00FF00", "#FCF4A3", "#FF0000"] # G, Y, R
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif type(agent) is Vehicle:
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#FAFAFA", "#69C7B7", "#3D81C2"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = CanvasGrid(StreetModel_portrayal, 30, 30, 600, 600)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}]
)

model_params = {

}

server = ModularServer(
    #StreetModel, [canvas_element, chart_element], "Traffic Simulation", model_params
    StreetModel, [canvas_element], "Traffic Simulation", model_params
)
server.port = 8521