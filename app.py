from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'FLORIDA_TECH'  # Change this to a secure secret key in a real-world application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# Define Quiz Result Model
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Questions and Answers
from quiz_data import questions
from quiz_data_2 import questions_2
from quiz_data_3 import questions_3
# Move db.create_all() call inside the if __name__ == '__main__' block
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

# Homepage route
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/network_security')
def network_security():
    return render_template('network_security.html')

@app.route('/cryptography')
def cryptography():
    return render_template('cryptography.html')

@app.route('/re')
def re():
    return render_template('re.html')

@app.route('/web-app-exploit')
def webappexploit():
    return render_template('web_exploitation.html')

@app.route('/forensics')
def forensics():
    return render_template('forensics.html')

@app.route('/quiz', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Store user's answer
        user_answer = request.form.get('answer')
        current_question_index = int(request.form.get('question_index', 0))
        current_question = questions[current_question_index]

        # Check if the answer is correct
        if user_answer == current_question['correct_answer']:
            # Increment user's score
            session['score'] = session.get('score', 0) + 1

        # Move to the next question or display the result
        next_question_index = current_question_index + 1
        if next_question_index < len(questions):
            return redirect(url_for('index', question_index=next_question_index))

        # If all questions are answered, redirect to results
        return redirect(url_for('results'))

    # Display the current question
    question_index = int(request.args.get('question_index', 0))
    current_question = questions[question_index]
    return render_template('quiz.html', question=current_question, question_index=question_index)

@app.route('/quiz2', methods=['GET', 'POST'])
def roundtwo():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Store user's answer
        user_answer = request.form.get('answer')
        current_question_index = int(request.form.get('question_index', 0))
        current_question = questions_2[current_question_index]

        # Check if the answer is correct
        if user_answer == current_question['correct_answer']:
            # Increment user's score
            session['score'] = session.get('score', 0) + 1

        # Move to the next question or display the result
        next_question_index = current_question_index + 1
        if next_question_index < len(questions_2):
            return redirect(url_for('roundtwo', question_index=next_question_index))

        # If all questions are answered, redirect to results
        return redirect(url_for('results2'))

    # Display the current question
    question_index = int(request.args.get('question_index', 0))
    current_question = questions_2[question_index]
    return render_template('quiz2.html', question=current_question, question_index=question_index)

@app.route('/quiz3', methods=['GET', 'POST'])
def roundthree():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Store user's answer
        user_answer = request.form.get('answer')
        current_question_index = int(request.form.get('question_index', 0))
        current_question = questions_3[current_question_index]

        # Check if the answer is correct
        if user_answer == current_question['correct_answer']:
            # Increment user's score
            session['score'] = session.get('score', 0) + 1

        # Move to the next question or display the result
        next_question_index = current_question_index + 1
        if next_question_index < len(questions_3):
            return redirect(url_for('roundthree', question_index=next_question_index))

        # If all questions are answered, redirect to results
        return redirect(url_for('results3'))

    # Display the current question
    question_index = int(request.args.get('question_index', 0))
    current_question = questions_3[question_index]
    return render_template('quiz3.html', question=current_question, question_index=question_index)

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user's score
    score = session.pop('score', 0)

    # Save quiz result to the database
    user = User.query.filter_by(username=session['username']).first()
    quiz_result = QuizResult(user_id=user.id, score=score)
    db.session.add(quiz_result)
    db.session.commit()

    return render_template('results.html', score=score)

@app.route('/results2')
def results2():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user's score
    score = session.pop('score', 0)

    # Save quiz result to the database
    user = User.query.filter_by(username=session['username']).first()
    quiz_result = QuizResult(user_id=user.id, score=score)
    db.session.add(quiz_result)
    db.session.commit()

    return render_template('results2.html', score=score)

@app.route('/results3')
def results3():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Retrieve user's score
    score = session.pop('score', 0)

    # Save quiz result to the database
    user = User.query.filter_by(username=session['username']).first()
    quiz_result = QuizResult(user_id=user.id, score=score)
    db.session.add(quiz_result)
    db.session.commit()

    return render_template('results3.html', score=score)

@app.route('/retake')
def retake():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Clear user's score from session
    session.pop('score', None)

    return redirect(url_for('index', question_index=0))

@app.route('/retake2')
def retake2():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Clear user's score from session
    session.pop('score', None)

    return redirect(url_for('roundtwo', question_index=0))

@app.route('/retake3')
def retake3():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Clear user's score from session
    session.pop('score', None)

    return redirect(url_for('roundthree', question_index=0))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            return redirect(url_for('index', question_index=0))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('score', None)
    return redirect(url_for('login'))

@app.route('/terminal')
def terminal():
    return render_template('terminal.html')

import subprocess

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    command = data['command']
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return jsonify({'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': e.output})

@app.route('/robots.txt')
def robots():
   return render_template('robots.html')

if __name__ == '__main__':
    app.run(debug=True)
