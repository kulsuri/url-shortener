# modules
from flask import Flask, jsonify, abort, make_response, request

# create an instance of the web app
app = Flask(__name__)

# json database
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

# define route /
@app.route("/")
def hello(): # function that will be executed when route localhost:5000/ is accessed
    return "Hello World"

# define GET route /tasks
@app.route('/shorten_url', methods=['GET'])
def get_tasks(): # function that will be executed when route localhost:5000/tasks is accessed
    return jsonify({'tasks': tasks})

# define GET route /shorten_url/<task_id>
@app.route('/shorten_url/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# define POST route /shorten_url
@app.route('/shorten_urley', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get['description', ""],
        'done': False
    }

    tasks.append(new_task)
    return jsonify({'task': new_task}), 201

# define 404 error handler route
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# define 400 error handler route
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': '400 - failed to decode json object'}), 400)

if __name__ == '__main__':
    app.run(debug=True)