from flask import render_template
from app import app

# Views


@app.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    message = "Goals pitching"
    return render_template('index.html', message=message)


@app.route('/goal/<goal_id>')
def goal(goal_id):
    '''
    View goal page function that returns the goal details page and its data
    '''
    return render_template('goal.html', id=goal_id)
