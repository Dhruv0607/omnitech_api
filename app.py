import settings
from flask import Flask, request
from flask_restful import Resource, Api
from payload import payload_calc
from payload import send_command_req

app = Flask(__name__)
api = Api(app)

settings.init()

class Home(Resource):
    def get(self):
        return "Hello"

class ColorCommand(Resource):
    def get(self):
        return {'rgbw': settings.rgbw}

    def post(self):
        settings.init()
        data = request.get_json()
        color = {'red': data['red'], 'green': data['green'], 'blue': data['blue'], 'white': data['white']}
        settings.rgbw.append(color)
        payload_calc("C")
        send_command_req()
        return color, 201

api.add_resource(ColorCommand, '/commandC')
api.add_resource(Home, '/')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

'''
TODO: 
    1. Calculate bytes of string (payload)
    2. Change byte size from hardcoded 0004 to 1.
    3. Link frontend and backend
'''
