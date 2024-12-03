from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/todos'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([{
        'id': todo.id,
        'title': todo.title,
        'completed': todo.completed
    } for todo in todos])

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = Todo(title=data['title'], description=data.get('description', ''))
    db.session.add(todo)
    db.session.commit()
    return jsonify({'id': todo.id, 'title': todo.title}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
