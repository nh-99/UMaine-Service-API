from flask import Flask, request, jsonify

from app.utils import textbooks

app = Flask(__name__)

@app.route('/studentcenter/getisbns', methods=['GET'])
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

@app.route('/studentcenter/getprices', methods=['GET'])
def get_prices():
	json_data = request.get_json(force=True)
	isbns = json_data['isbns']
	prices = textbooks.get_textbook_prices(isbns)
	toReturn = {}
	if isbns is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : isbns }
	else:
		toReturn = { "status": "success", "prices" : prices }
	return jsonify(toReturn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
