from flask import Flask, render_template, request, jsonify
import json, logging, os, atexit
from model import StreetModel

modelMesa = StreetModel()

def positionsToJSON(ps):
    posDICT = []
    for p in ps:
        pos = {
            "x" : p[0],
            "z" : p[1],
            "y" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)

def statesToJSON(ss):
    stateDICT = []
    for s in range(4):
        state = {
            "state" : ss[s]
        }
        stateDICT.append(state)
    return json.dumps(stateDICT)

app = Flask(__name__, static_url_path='')

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8585))

@app.route('/')
def root():
    return jsonify([{"message":"Hello World from IBM Cloud!"}])
    
@app.route('/mesa', methods=['POST', 'GET'])
def mesa():
    [positions, states] = modelMesa.step()
    resp = "{\"data\":" + positionsToJSON(positions) + "},{\"states\":" + statesToJSON(states) + "}"
    return resp
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)