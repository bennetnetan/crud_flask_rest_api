from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = {}
next_id = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.json
    tasks[next_id] = data['name']
    response = {'id': next_id, 'name': data['name']}
    next_id += 1
    return jsonify(response), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    if task_id in tasks:
        tasks[task_id] = data['name']
        return jsonify({'id': task_id, 'name': data['name']})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == "__main__":
    app.run(debug=True)