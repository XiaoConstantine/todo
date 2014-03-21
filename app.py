import pymongo
from bson.objectid import ObjectId
import json_util
from flask import Flask, render_template, url_for, json, request, make_response
try:
    from flask_cors import cross_origin
except:
    from flask.ext.cors import cross_origin

app = Flask(__name__)
app.debug = True
connection = pymongo.Connection('localhost', 27017)
todos = connection['demo']['todos']


def json_load(data):
    return json.loads(data, object_hook=json_util.object_hook)

def json_dump(data):
    return json.dumps(data, default=json_util.default)

@app.after_request
def after_request(data):
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, DELETE, UPDATE, PUT, OPTIONS"
    return response


@app.route('/')
@cross_origin(origins='*')
def index():
    return render_template("index.html")

#list all items in mongo
@app.route('/todos', methods=['GET'])
@cross_origin(origins='*')
def list_todos():
    return json_dump(list(todos.find())), 200

#get specific id item
@app.route('/todos', methods=['GET'])
def get_todos(todo_id):
    objectid = None
    try:
        objectid = ObjectId(todo_id)
    except:
        return json_dump({"result": "invalid id"}), 400
    todo = todos.find_one({'_id':objectid})
    if todo is None:
        return json_dump({"result": "No such id object" + todo_id}), 404
    return json_dump(todo), 200

#create new item into db
@app.route('/todos',  methods=['POST'])
@cross_origin(origins='*')
def new_todo():
    todo = json_load(request.data)
    todos.save(todo)
    return json_dump(todo), 200

#update exist item
@app.route('/todos/<todo_id>', methods=['PUT'])
@cross_origin(origins='/todos/*')
def update_todo(todo_id):
    data = json_load(request.data)
    todos.save(data)
    return json_dump({'result':'OK'}), 200

#delete item
@app.route('/todos/<todo_id>', methods=['DELETE'])
@cross_origin(origins='/todos/*')
def delete_todo(todo_id):
    todos.remove(ObjectId(todo_id))
    return json_dump({'result':'OK'}), 200


if __name__ == '__main__':
    app.run()



