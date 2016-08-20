from flask import Flask, request, jsonify

from app.utils import textbooks

app = Flask(__name__)

@app.route('/studentcenter/textbooks', methods=['GET'])
def get_textbooks():
	json_data = request.get_json(force=True)
	username = json_data['username']
	password = json_data['password']
	isbns = textbooks.get_isbns_from_mainestreet(username, password)
	toReturn = {}
	if isbns is not -1 and not -2:
		toReturn = { "status": "error", "errorCode" : isbns }
	else:
		#mailer.email_pin_change(username, password, newPin)
		toReturn = { "status": "success", "isbns" : isbns }
	return jsonify(toReturn)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
