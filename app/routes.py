from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, HiddenField
from wtforms.validators import DataRequired, NumberRange
import numpy as np

bp = Blueprint('main', __name__)

# List of questions corresponding to each feature
QUESTIONS = [
    ("social_energy", "How would you rate your social energy?"),
    ("alone_time_preference", "How much do you prefer alone time?"),
    ("talkativeness", "How talkative are you?"),
    ("deep_reflection", "How often do you engage in deep reflection?"),
    ("group_comfort", "How comfortable are you in groups?"),
    ("party_liking", "How much do you enjoy parties?"),
    ("listening_skill", "How would you rate your listening skills?"),
    ("empathy", "How empathetic are you?"),
    ("creativity", "How creative do you consider yourself?"),
    ("organization", "How organized are you?"),
    ("leadership", "How strong are your leadership skills?"),
    ("risk_taking", "How willing are you to take risks?"),
    ("public_speaking_comfort", "How comfortable are you with public speaking?"),
    ("curiosity", "How curious are you?"),
    ("routine_preference", "How much do you prefer routine?"),
    ("excitement_seeking", "How much do you seek excitement?"),
    ("friendliness", "How friendly are you?"),
    ("emotional_stability", "How emotionally stable are you?"),
    ("planning", "How much do you plan ahead?"),
    ("spontaneity", "How spontaneous are you?"),
    ("adventurousness", "How adventurous are you?"),
    ("reading_habit", "How often do you read?"),
    ("sports_interest", "How interested are you in sports?"),
    ("online_social_usage", "How much do you use social media?"),
    ("travel_desire", "How much do you desire to travel?"),
    ("gadget_usage", "How much do you use gadgets?"),
    ("work_style_collaborative", "How collaborative is your work style?"),
    ("decision_speed", "How quickly do you make decisions?"),
    ("stress_handling", "How well do you handle stress?")
]

QUESTIONS_PER_PAGE = 10

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear()
        session['responses'] = [None] * len(QUESTIONS)
        return redirect(url_for('main.questions', page=0))
    return render_template('index.html')

@bp.route('/questions', methods=['GET', 'POST'])
@bp.route('/questions/<int:page>', methods=['GET', 'POST'])
def questions(page=0):
    if 'responses' not in session:
        return redirect(url_for('main.index'))
    
    total_pages = (len(QUESTIONS) + QUESTIONS_PER_PAGE - 1) // QUESTIONS_PER_PAGE
    
    # Check if we should redirect to result page
    if page >= total_pages:
        if None not in session['responses']:
            return redirect(url_for('main.result'))
        else:
            # Find the first page with unanswered questions
            for i in range(total_pages):
                start_idx = i * QUESTIONS_PER_PAGE
                end_idx = min((i + 1) * QUESTIONS_PER_PAGE, len(QUESTIONS))
                if None in session['responses'][start_idx:end_idx]:
                    return redirect(url_for('main.questions', page=i))
            return redirect(url_for('main.result'))
    
    # Create form for current page
    class QuestionForm(FlaskForm):
        pass
    
    start_idx = page * QUESTIONS_PER_PAGE
    end_idx = min((page + 1) * QUESTIONS_PER_PAGE, len(QUESTIONS))
    
    # Add fields for each question on this page
    for i in range(start_idx, end_idx):
        feature, question_text = QUESTIONS[i]
        setattr(QuestionForm, feature, FloatField(
            question_text,
            validators=[
                DataRequired(),
                NumberRange(min=0, max=10, message="Please enter a value between 0 and 10")
            ],
            render_kw={"min": 0, "max": 10, "step": 0.5, "class": "slider", "id": f"q{i}"}
        ))
    
    setattr(QuestionForm, 'page', HiddenField(default=page))
    setattr(QuestionForm, 'submit', SubmitField('Next Page' if page < total_pages - 1 else 'See Results'))
    
    form = QuestionForm()
    
    # Pre-populate form with existing responses
    if request.method == 'GET':
        for i in range(start_idx, end_idx):
            feature, _ = QUESTIONS[i]
            if session['responses'][i] is not None:
                getattr(form, feature).data = session['responses'][i]
    
    if form.validate_on_submit():
        # Save responses from this page
        responses = session['responses']
        for i in range(start_idx, end_idx):
            feature, _ = QUESTIONS[i]
            responses[i] = float(getattr(form, feature).data)
        
        session['responses'] = responses
        
        next_page = page + 1
        if next_page < total_pages:
            return redirect(url_for('main.questions', page=next_page))
        else:
            return redirect(url_for('main.result'))
    
    # Calculate progress
    answered = sum(1 for r in session['responses'] if r is not None)
    progress = int((answered / len(QUESTIONS)) * 100)
    
    return render_template(
        'question_page.html',
        form=form,
        questions=QUESTIONS[start_idx:end_idx],
        current_page=page,
        total_pages=total_pages,
        progress=progress,
        start_idx=start_idx
    )

@bp.route('/result')
def result():
    if 'responses' not in session or None in session['responses']:
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
            'Introvert': 'You recharge by spending time alone. You tend to be more reflective and enjoy deep conversations with close friends rather than large social gatherings. You value your privacy and often need time to process your thoughts internally.',
            'Extrovert': 'You gain energy from being around others. You enjoy social interactions and often feel energized after spending time with people. You tend to be outgoing, expressive, and comfortable in group settings.',
            'Ambivert': 'You have a balance of introvert and extrovert traits. You enjoy socializing but also value your alone time. You can adapt to different social situations and feel comfortable both in groups and spending time by yourself.'
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

@bp.route('/api/save_response', methods=['POST'])
def save_response():
    if 'responses' not in session:
        return jsonify({'success': False})
    
    data = request.get_json()
    question_idx = data.get('index')
    value = data.get('value')
    
    if question_idx is not None and value is not None and 0 <= question_idx < len(QUESTIONS):
        responses = session['responses']
        responses[question_idx] = float(value)
        session['responses'] = responses
        return jsonify({'success': True})
    
    return jsonify({'success': False})