<<<<<<< HEAD
from flask import Flask, render_template
from flask import Flask
=======
#!/usr/bin/env python3
"""model to display the to-do list"""
from flask import Flask, render_template, request, redirect, url_for
>>>>>>> origin/master
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Ensure the database and tables are created
with app.app_context():
    db.create_all()

# Home route to list all tasks
@app.route('/')
<<<<<<< HEAD
def index():
    tasks = Task.query.all()
=======
def list_tasks():
    """Displays a list of all tasks with their details (priority, due date, completion status)."""
    tasks = Task.query.order_by(Task.due_date.asc()).all()
>>>>>>> origin/master
    return render_template('index.html', tasks=tasks)

# Route to create a new task
@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    """Handles creating new tasks."""
    if request.method == 'POST':
        task_name = request.form['task']
        task_priority = request.form['priority']
        task_due_date = request.form['due_date']

        new_task = Task(task=task_name, priority=task_priority, due_date=task_due_date)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            print(f"Error creating task: {e}")
            return render_template('create_task.html', error="Error creating task")
    
    return render_template('create_task.html')

# Route to edit an existing task
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Handles editing an existing task."""
    task = Task.query.get_or_404(task_id)

    if request.method == 'POST':
        task.task = request.form['task']
        task.priority = request.form['priority']
        task.due_date = request.form['due_date']
        task.completed = 'completed' in request.form  # Checkbox for task completion

        try:
            db.session.commit()
            return redirect(url_for('list_tasks'))
        except Exception as e:
            print(f"Error editing task: {e}")
            return render_template('edit_task.html', task=task, error="Error editing task")

    return render_template('edit_task.html', task=task)

# Route to delete a task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Deletes a task from the database."""
    task = Task.query.get_or_404(task_id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('list_tasks'))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return redirect(url_for('list_tasks'), error="Error deleting task")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

