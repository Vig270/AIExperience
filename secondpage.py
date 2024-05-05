import datetime
import logging
import requests
from flask import Flask, request, render_template, jsonify
from transformers import pipeline

app = Flask(__name__)

# Set up logging
logging.basicConfig(filename='sentiment_analysis.log', level=logging.ERROR)

class Customer:
    def __init__(self, name, email, item, issue, sentiment_label):
        self.name = name
        self.email = email
        self.item = item
        self.issue = issue
        self.sentiment_label = sentiment_label
        self.timestamp = datetime.datetime.now()

issues = []
EMAIL_THRESHOLD = 3
NAME_THRESHOLD = 3

# Initialize sentiment analysis pipeline
classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def analyze_sentiment(text):
    try:
        result = classifier(text)[0]
        logging.info("Sentiment analysis result: %s", result)
        
        if 'label' in result:
            return result['label']
        else:
            logging.error("Sentiment analysis failed: No label found in result")
            return None
    except Exception as e:
        logging.error('Failed to analyze sentiment: %s', e)
        return None

def detect_fraud(new_customer):
    try:
        same_email_count = sum(1 for issue in issues if issue.email == new_customer.email)
        if same_email_count >= EMAIL_THRESHOLD:
            return "Potential fraud detected: Multiple issues have been reported using the same email address within a short period."
        
        same_name_count = sum(1 for issue in issues if issue.name == new_customer.name)
        if same_name_count >= NAME_THRESHOLD:
            return "Potential fraud detected: Multiple issues have been reported using the same name within a short period."
        
        return None
    except Exception as e:
        logging.error('Failed to detect fraud: %s', e)
        return None

@app.route('/')
def index():
    return render_template('secondpage.html')

@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    try:
        name = request.form['name']
        email = request.form['email']
        item = request.form['item']
        issue = request.form['issue']
        
        # Perform sentiment analysis on the issue description
        sentiment_label = analyze_sentiment(issue)
        
        # Creating a Customer object
        new_customer = Customer(name, email, item, issue, sentiment_label)
        
        # Check for fraud
        fraud_message = detect_fraud(new_customer)
        if fraud_message:
            return fraud_message
        
        issues.append(new_customer)
        
        # Returning a JSON response including sentiment analysis result
        return jsonify({
            "message": "Issue submitted successfully!",
            "sentiment_label": sentiment_label
        })
    except Exception as e:
        logging.error('Failed to submit issue: %s', e)
        return jsonify({"error": "Failed to submit issue. Please try again later."}), 500

@app.route('/view_issues')
def view_issues():
    try:
        if not issues:
            return "No issues have been submitted yet."
        else:
            result = "Here are the submitted issues:<br>"
            for idx, customer in enumerate(issues, start=1):
                result += f"Issue {idx}:<br>Name: {customer.name}<br>Email: {customer.email}<br>Item: {customer.item}<br>Issue: {customer.issue}<br>Sentiment: {customer.sentiment_label}<br><br>"
            return result
    except Exception as e:
        logging.error('Failed to view issues: %s', e)
        return jsonify({"error": "Failed to view issues. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
