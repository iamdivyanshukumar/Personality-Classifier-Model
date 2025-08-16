from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import numpy as np

bp = Blueprint('main', __name__)

# List of questions corresponding to each feature
QUESTIONS = [
    ("social_energy", "How would you rate your social energy? (1-10)"),
    ("alone_time_preference", "How much do you prefer alone time? (1-10)"),
    ("talkativeness", "How talkative are you? (1-10)"),
    ("deep_reflection", "How often do you engage in deep reflection? (1-10)"),
    ("group_comfort", "How comfortable are you in groups? (1-10)"),
    ("party_liking", "How much do you enjoy parties? (1-10)"),
    ("listening_skill", "How would you rate your listening skills? (1-10)"),
    ("empathy", "How empathetic are you? (1-10)"),
    ("creativity", "How creative do you consider yourself? (1-10)"),
    ("organization", "How organized are you? (1-10)"),
    ("leadership", "How strong are your leadership skills? (1-10)"),
    ("risk_taking", "How willing are you to take risks? (1-10)"),
    ("public_speaking_comfort", "How comfortable are you with public speaking? (1-10)"),
    ("curiosity", "How curious are you? (1-10)"),
    ("routine_preference", "How much do you prefer routine? (1-10)"),
    ("excitement_seeking", "How much do you seek excitement? (1-10)"),
    ("friendliness", "How friendly are you? (1-10)"),
    ("emotional_stability", "How emotionally stable are you? (1-10)"),
    ("planning", "How much do you plan ahead? (1-10)"),
    ("spontaneity", "How spontaneous are you? (1-10)"),
    ("adventurousness", "How adventurous are you? (1-10)"),
    ("reading_habit", "How often do you read? (1-10)"),
    ("sports_interest", "How interested are you in sports? (1-10)"),
    ("online_social_usage", "How much do you use social media? (1-10)"),
    ("travel_desire", "How much do you desire to travel? (1-10)"),
    ("gadget_usage", "How much do you use gadgets? (1-10)"),
    ("work_style_collaborative", "How collaborative is your work style? (1-10)"),
    ("decision_speed", "How quickly do you make decisions? (1-10)"),
    ("stress_handling", "How well do you handle stress? (1-10)")
]

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear()
        session['responses'] = []
        session['current_question'] = 0
        return redirect(url_for('main.question'))
    return render_template('index.html')

@bp.route('/question', methods=['GET', 'POST'])
def question():
    if 'responses' not in session:
        return redirect(url_for('main.index'))
    
    current_idx = session['current_question']
    
    if current_idx >= len(QUESTIONS):
        return redirect(url_for('main.result'))
    
    feature, question_text = QUESTIONS[current_idx]
    
    # Dynamically create form with current question
    class DynamicForm(FlaskForm):
        pass
    
    setattr(DynamicForm, feature, FloatField(
        question_text,
        validators=[
            DataRequired(),
            NumberRange(min=0, max=10, message="Please enter a value between 0 and 10")
        ]
    ))
    setattr(DynamicForm, 'submit', SubmitField('Next'))
    
    form = DynamicForm()
    
    if form.validate_on_submit():
        # Save response
        responses = session['responses']
        responses.append(float(getattr(form, feature).data))
        session['responses'] = responses
        session['current_question'] = current_idx + 1
        
        if session['current_question'] < len(QUESTIONS):
            return redirect(url_for('main.question'))
        else:
            return redirect(url_for('main.result'))
    
    # Calculate progress
    progress = int((current_idx / len(QUESTIONS)) * 100)
    
    return render_template(
        'question.html',
        form=form,
        question_text=question_text,
        current=current_idx + 1,
        total=len(QUESTIONS),
        progress=progress
    )

@bp.route('/result')
def result():
    if 'responses' not in session or len(session['responses']) != len(QUESTIONS):
        return redirect(url_for('main.index'))
    
    try:
        # Prepare input for model
        responses = np.array(session['responses']).reshape(1, -1)
        
        # Get models from app context
        models = current_app.models
        
        # Scale the input
        scaled_input = models['scaler'].transform(responses)
        
        # Make prediction
        prediction = models['model'].predict(scaled_input)
        predicted_class = np.argmax(prediction, axis=1)
        personality = models['label_encoder'].inverse_transform(predicted_class)[0]
        confidence = float(np.max(prediction))
        
        # Get personality description
        descriptions = {
            'Introvert': 'You recharge by spending time alone...',
            'Extrovert': 'You gain energy from being around others...',
            'Ambivert': 'You have a balance of introvert and extrovert traits...'
        }
        
        description = descriptions.get(personality, 'No description available.')
        
        # Clear session
        session.clear()
        
        return render_template(
            'result.html',
            personality=personality,
            confidence=confidence * 100,
            description=description
        )
    except Exception as e:
        current_app.logger.error(f"Error in result route: {str(e)}")
        return render_template('error.html'), 500