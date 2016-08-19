from service_utils import root_dir, nice_json
from flask import Flask, request
from flask.ext.cors import CORS
import json
from db import users
from db.users import User

from werkzeug import generate_password_hash, check_password_hash
from werkzeug.exceptions import NotFound

app = Flask(__name__)
CORS(app)
users.db.create_all()

@app.route("/register", methods=['POST'])
def register():
    json_data = request.get_json(force=True)
    username = json_data['username']
    email = json_data['email']
    hashed_password = generate_password_hash(json_data['password'])
    user = User(username, email, hashed_password)
    
    response = "" # The response to return to the user
    if not User.query.filter_by(email=user.email).count():
        users.db.session.add(user)
        users.db.session.commit()
        response = {'status':'success','message':'User created successfully!'}
    else:
        response = {'status':'error','message':'User with this email already exists'}
        
    return nice_json(response)

@app.route("/login", methods=['POST'])
def login():
    json_data = request.get_json(force=True)
    username = json_data['username']
    password = json_data['password']
    
    response = ""
    if User.query.filter_by(username=username).count():
        user = User.query.filter_by(username=username).first()
        if check_password_hash(str(user.password), password):
            response = {'status':'success','message':'Logged in successfully'}
        else:
            response = {'status':'error','message':'Incorrect username or password'}
    else:
        response = {'status':'error','message':'Incorrect username or password'}
            
    return nice_json(response)
    
@app.route("/services/add", methods=['POST'])
def add_service():
    json_data = request.get_json(force=True)
    username = json_data['username']
    password = json_data['password']
    service_name = json_data['service_name']
    service_key = json_data['service_key']
    
    response = ""
    if User.query.filter_by(username=username).count():
        user = User.query.filter_by(username=username).first()
        if check_password_hash(str(user.password), password):
            if user.serviceKeys != None:
                current_services = json.loads(user.serviceKeys)
                current_services["services"].append({'name':service_name, 'key':service_key})
                user.serviceKeys = json.dumps(current_services)
                users.db.session.add(user)
                users.db.session.commit()
            else:
                current_services = {'services':[]}
                current_services["services"].append({'name':service_name, 'key':service_key})
                user.serviceKeys = json.dumps(current_services)
                users.db.session.add(user)
                users.db.session.commit()
            response = {'status':'success','message':'Added service successfully'}
        else:
            response = {'status':'error','message':'Incorrect username or password'}
    else:
        response = {'status':'error','message':'Incorrect username or password'}
            
    return nice_json(response)
    
@app.route("/services/get", methods=['POST'])
def get_service():
    json_data = request.get_json(force=True)
    username = json_data['username']
    password = json_data['password']
    service_name = json_data['service_name']
    
    response = ""
    if User.query.filter_by(username=username).count():
        user = User.query.filter_by(username=username).first()
        if check_password_hash(str(user.password), password):
            if user.serviceKeys is not None:
                services = json.loads(user.serviceKeys)
                for service in services['services']:
                    print(service['name'])
                    if service_name == service['name']:
                        response = {'status':'success','message':'Key found successfully', 'key':service['key']}
            else:
				response = {'status':'error','message':'Service not found'}
        else:
            response = {'status':'error','message':'Incorrect username or password'}
    else:
        response = {'status':'error','message':'Incorrect username or password'}
    
    if response is '':
        response = {'status':'error','message':'Service not found'}
    return nice_json(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
