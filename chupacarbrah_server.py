import os
from flask import Flask, request, jsonify
from flask_restful import Api


application = Flask(__name__)
application._static_folder = os.path.abspath("templates/static/")
api = Api(application)

global cars
cars = {}

global DEBUG
DEBUG = 1

if DEBUG:
    cars["51f317ec266e4adb956212201f87ba51"] = {"VIN": "1A2B", "maker": "Generic", "log": []}


@application.route('/')
def base_path():
    return status_endpoint()





@application.route("/api/v1/status")
def status_endpoint():
    global cars
    # curl "http://localhost:5000/api/v1/status"
    return jsonify(cars)


global cmds
cmds = []


@application.route("/api/v1/rpc", methods=["GET", "POST"])
def rpc_endpoint():
    global cmds
    can_message = ""
    if request.method == 'GET':
        can_message = cmds.pop(0)
    if request.method == 'POST':
        cmds.append(request.args.get('cmd'))
    return jsonify(can_message)


@application.route("/api/v1/cars", methods=["GET", "POST", "DELETE", "OPTIONS"])
def cars_endpoint():
    global cars
    car_uuid = ""
    if request.method == 'GET' or request.method == 'POST':
        car_uuid = request.args.get('car_uuid')

    if request.method == 'GET':
        # curl "http://localhost:5000/api/v1/cars?car_uuid=51f317ec266e4adb956212201f87ba52"
        data = ""
        if car_uuid in cars:
            data = cars[car_uuid]
        return jsonify(data)

    elif request.method == 'POST':
        """
        curl --header "Content-Type: application/json" \
        --request POST \
        --data '{"car_uuid":"51f317ec266e4adb956212201f87ba52", "VIN": "1A2B", "maker": "Generic", "log":{"timestamp":"20200501120000","GPS":"00"}}' \
        "http://localhost:5000/api/v1/cars"
        """
        data = request.json
        VIN = "0000"
        maker = "unknown"
        new_log = []
        if "VIN" in data:
            VIN = data["VIN"]
        if "maker" in data:
            maker = data["maker"]
        if "log" in data:
            new_log = data["log"]
        if "car_uuid" in data:
            car_uuid = data["car_uuid"]

            if car_uuid not in cars:
                # new car
                cars[car_uuid] = {"VIN": VIN, "maker": maker, "log": []}

            if "VIN" in cars[car_uuid]:
                cars[car_uuid]["VIN"] = VIN
            if "maker" in cars[car_uuid]:
                cars[car_uuid]["maker"] = maker
            if "log" in cars[car_uuid]:
                cars[car_uuid]["log"].append(new_log)
        return jsonify(car_uuid)
    elif request.method == 'DELETE' or request.method == 'OPTIONS':
        return jsonify("")
    return jsonify('Error 405 Method Not Allowed')


@application.route("/api/v1/flush", methods=["GET"])
def flus_endpoint():
    global cars
    if request.method == 'GET':
        # curl "http://localhost:5000/api/v1/flush?token=d517ad99d272117ec2656e4adb80802e8e74b6ab1"
        token = request.args.get('token')
        if token == "d517ad99d272117ec2656e4adb80802e8e74b6ab1":
            cars = {}
            return jsonify("FLUSHED!")
    return jsonify(cars)


if __name__ == '__main__':
    if DEBUG > 0:
        application.debug = True
    application.run(threaded=True)



