from flask import Flask, request, jsonify
from flask_cors import CORS
#from app.utils import umainepinchanger, mailer
from utils import pinchanger, roomassignment

app = Flask(__name__)
CORS(app)

@app.route('/pin/change', methods=['POST'])
def change_pin():
	json_data = request.get_json(force=True)
	username = json_data['username']
	password = json_data['password']
	newPin = pinchanger.get_new_pin(username, password)
	toReturn = {}
	if newPin is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : newPin }
	else:
		#mailer.email_pin_change(username, password, newPin)
		toReturn = { "status": "success", "newPin" : newPin }
	return jsonify(toReturn)
	
@app.route('/assignment', methods=['GET'])
def check_assignment():
	json_data = request.get_json(force=True)
	username = json_data['username']
	password = json_data['password']
	roomAssignment = roomassignment.get_room_info(username, password)
	toReturn = {}
	if roomAssignment is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : roomAssignment }
	else:
		toReturn = roomAssignment
	return jsonify(toReturn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
