import logging
import datetime
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

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

def analyze_sentiment(text):
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions",
            headers={"Authorization": "Bearer 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", "Content-Type": "application/json"},
            json={"inputs": text}
        )
        if response.status_code == 200:
            result = response.json()[0]
            logging.info("Sentiment analysis result: %s", result)
            if 'label' in result:
                return result['label']
        else:
            logging.error("Failed to analyze sentiment: %s", response.text)
    except Exception as e:
        logging.error('Failed to analyze sentiment: %s', e)
    return None


def detect_fraud(new_customer):
    same_email_count = sum(1 for issue in issues if issue.email == new_customer.email)
    if same_email_count >= EMAIL_THRESHOLD:
        return "Potential fraud detected: Multiple issues have been reported using the same email address within a short period."
    
    same_name_count = sum(1 for issue in issues if issue.name == new_customer.name)
    if same_name_count >= NAME_THRESHOLD:
        return "Potential fraud detected: Multiple issues have been reported using the same name within a short period."
    
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
        
        sentiment_label = analyze_sentiment(issue)
        
        if sentiment_label is None:
            return jsonify({"error": "Failed to analyze sentiment"})
        
        new_customer = Customer(name, email, item, issue, sentiment_label)
        
        fraud_message = detect_fraud(new_customer)
        if fraud_message:
            return jsonify({"error": fraud_message})
        
        issues.append(new_customer)
        
        return jsonify({
            "message": "Issue submitted successfully!",
            "sentiment_label": sentiment_label
        })
    except Exception as e:
        logging.error('Failed to submit issue: %s', e)
        return jsonify({"error": "Failed to submit issue"}), 500

@app.route('/view_issues')
def view_issues():
    if not issues:
        return "No issues have been submitted yet."
    else:
        result = "Here are the submitted issues:<br>"
        for idx, customer in enumerate(issues, start=1):
            result += f"Issue {idx}:<br>Name: {customer.name}<br>Email: {customer.email}<br>Item: {customer.item}<br>Issue: {customer.issue}<br>Sentiment: {customer.sentiment_label}<br><br>"
        return result

if __name__ == '__main__':
    app.run(debug=True)

