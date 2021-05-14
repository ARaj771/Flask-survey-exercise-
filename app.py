from flask import Flask, request, render_template,redirect,flash
from flask_debugtoolbar import DebugToolbarExtension
from flask import session

from surveys import satisfaction_survey 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not-secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def start_survey():
    """ The initial page in the survey"""
    title =  satisfaction_survey.title
    instructions = satisfaction_survey.instructions
   
    return render_template('initial_page.html',title = title, instructions = instructions)

@app.route('/question/<int:question_num>')
def  ask (question_num):
    """ Asks survey question num"""
    title =  satisfaction_survey.title
    question = satisfaction_survey.questions[question_num]
    size = len(satisfaction_survey.questions)

    responses = session.get('responses')

    if (question_num >= size) and (len(responses) == size) :
        return redirect ("/thanks")

    if (len(responses) < size) and  (question_num != len(responses)):
        flash('Please answer the next question in the survey')
        return redirect(f'/question/{len(responses)}')
    
    return render_template("questions.html",title = title, question = question)

@app.route('/answer',methods=['POST'])
def survey_data():
    value = request.form['ans']
    responses.append(value)
    session['responses'] = responses

    if len(session.get('responses')) == len(satisfaction_survey.questions):
        return redirect ("/thanks")
    else:
        return redirect(f'/question/{len(responses)}')

@app.route('/thanks')
def say_thanks():
    question = satisfaction_survey.questions
    
    return render_template('thanks.html',questions = question)

@app.route('/reset_session', methods = ['POST'])
def reset_session():
    """ resets responses list to empty."""
    
    session['responses'] = responses
    return redirect ('/question/0')