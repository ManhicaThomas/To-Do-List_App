.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from app import Task

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db = SQLAlchemy(app)

@app.route('/')
def list_tasks():
"""Displays a list of all tasks with their details (priority, due date, completion status)."""
    tasks = Task.query.order_by(Task.due_date.asc()).all()
return render_template('tasks.html', tasks=tasks)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    """Handles creating new tasks.
    - GET: Renders the task creation form.
    - POST: Validates and creates a new task in the database."""
    if request.method == 'GET':
        return render_template('create_task.html')
    elif request.method == 'POST':
        task = Task(
            task=request.form['task'],
            priority=request.form['priority'],
due_date=request.form['due_date']
)
try:
db.session.add(task)
db.session.commit()
return redirect(url_for('list_tasks'))
except Exception as e:

print(f"Error creating task: {e}")
return render_template('create_task.html', error="Error creating task")

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Handles editing an existing task.
    - GET: Renders the task edit form with pre-filled details.
    - POST: Validates and updates the existing task in the database."""
    task = Task.query.get(task_id)
    if not task:
return redirect(url_for('list_tasks')) 

if request.method == 'GET':
        return render_template('edit_task.html', task=task)
    elif request.method == 'POST':
        task.task = request.form['task']
        task.priority = request.form['priority']
task.due_date = request.form['due_date']
try:
db.session.commit()
return redirect(url_for('list_tasks'))
except Exception as e:

print(f"Error editing task: {e}")
return render_template('edit_task.html', task=task, error="Error editing task")

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    """Deletes a task from the database."""
    task = Task.query.get(task_id)
    if not task:
return redirect(url_for('list_tasks'))

try:
db.session.delete(task)
        db.session.commit()
return redirect(url_for('list_tasks'))
except Exception as e:

print(f"Error deleting task: {e}")
        return redirect(url_for('list_tasks'), error="Error deleting task")
