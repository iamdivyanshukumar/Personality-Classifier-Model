# Personality-Classifier-Model

A web application that classifies users into personality types (Introvert, Extrovert, or Ambivert) based on their responses to psychological questions. The system is built with **Flask**, **TensorFlow**, and modern web technologies.

---

## Features

- Personality assessment with 29 psychological questions  
- Progress tracking while answering the questionnaire  
- Real-time saving of responses  
- Machine learning-based personality classification  
- Responsive and clean user interface  
- Personality descriptions with confidence scores  

---

## Project Structure

```
personality-classifier/
├── app/                    # Main application package
│   ├── static/css/        # CSS stylesheets
│   ├── templates/         # HTML templates
│   ├── __init__.py        # Application factory
│   ├── model.py           # Model loading utilities
│   └── routes.py          # Application routes and logic
├── models/                # Trained models and preprocessing objects
├── notebooks/             # Jupyter notebooks for model development
├── myenv/                 # Virtual environment (ignored in git)
├── .env                   # Environment variables
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── wsgi.py                # WSGI server configuration
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/iamdivyanshukumar/Personality-Classifier-Model.git
cd Personality-Classifier-Model
```

Create and activate a virtual environment:

```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set up environment variables:

```bash
# Create a .env file in the project root with:
SECRET_KEY=your_secret_key_here
```

---

## Usage

Start the development server:

```bash
python app.py
```

Open your browser and navigate to:

```
http://localhost:5000
```

Steps:  
1. Complete the questionnaire by rating each statement on a scale of 0–10  
2. Submit responses  
3. View your personality classification results with explanations  

---

## Model Details

- **Input layer:** 29 features (user responses)  
- **Hidden layers:** Multiple dense layers with activation functions  
- **Output layer:** 3 classes (Introvert, Extrovert, Ambivert)  

Preprocessing steps:  
- StandardScaler for feature scaling  
- Label encoding for classification labels  

---


## Customization

- Modify questionnaire items in `app/routes.py` (`QUESTIONS` list)  
- Update personality descriptions in the result route  
- Retrain the model using the Jupyter notebook in `notebooks/`  
- Replace trained model files in `models/`  

