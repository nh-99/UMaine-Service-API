from flask import Flask, request, jsonify

from utils import textbooks, messagecenter, schedule

app = Flask(__name__)

@app.route('/studentcenter/textbooks/isbns', methods=['GET'])
def get_textbooks():
	json_data = request.get_json(force=True)
	username = json_data['username']
	password = json_data['password']
	isbns = textbooks.get_isbns_from_mainestreet(username, password)
	toReturn = {}
	if isbns is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : isbns }
	else:
		toReturn = { "status": "success", "isbns" : isbns }
	return jsonify(toReturn)

@app.route('/studentcenter/textbooks/prices', methods=['GET'])
def get_prices():
	json_data = request.get_json(force=True)
	isbns = json_data['isbns']
	prices = textbooks.get_textbook_prices(isbns)
	toReturn = {}
	if isbns is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : prices }
	else:
		toReturn = { "status": "success", "prices" : prices }
	return jsonify(toReturn)
	
@app.route('/studentcenter/messages', methods=['GET'])
def get_messages():
	username = request.args.get('username')
	password = request.args.get('password')
	messages = messagecenter.get_messages_from_mainestreet(username, password)
	toReturn = {}
	if messages is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : messages }
	else:
		toReturn = messages
	return jsonify(toReturn)
    
@app.route('/studentcenter/schedule', methods=['GET'])
def get_schedule():
	username = request.args.get('username')
	password = request.args.get('password')
	schedule = schedule.get_schedule_from_mainestreet(username, password)
	toReturn = {}
	if messages is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : schedule }
	else:
		toReturn = schedule
	return jsonify(toReturn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
