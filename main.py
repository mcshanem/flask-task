import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5

# Load variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

# Connect Bootstrap to Flask app
Bootstrap5(app)

# In-memory tasks, future update will put these in database (<Id>, <task description>, <boolean finished>)
tasks = [
    {'id': 0, 'description': 'Feed the monkey', 'done': False},
    {'id': 1, 'description': 'Solve world hunger. Tell no one.', 'done': False},
    {'id': 2, 'description': 'Go to Jazzercise', 'done': True}
]

next_id = 3


@app.route('/', methods=['GET', 'POST'])
def home():
    global next_id, tasks

    if request.method == 'POST':
        # Handle new task
        if 'new_task_text' in request.form:
            tasks.append({
                'id': next_id,
                'description': request.form['new_task_text'],
                'done': False})
            next_id += 1

        # Handle deleted and completed tasks
        else:
            tasks = [task for task in tasks if 'delete_' + str(task['id']) not in request.form]

            for task in tasks:
                if 'checkbox_' + str(task['id']) in request.form:
                    task['done'] = True
                else:
                    task['done'] = False

    # Sort the task list
    tasks.sort(key=lambda x: x['done'])

    return render_template('index.html', tasks=tasks)


if __name__ == '__main__':
    app.run(debug=True)
