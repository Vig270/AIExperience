import logging
from transformers import pipeline

logging.basicConfig(filename='sentiment_analysis.log', level=logging.ERROR)

class Customer:
    def __init__(self, name, email, item, issue, sentiment_label):
        self.name = name
        self.email = email
        self.item = item
        self.issue = issue
        self.sentiment_label = sentiment_label

issues = []
EMAIL_THRESHOLD = 3
NAME_THRESHOLD = 3

classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)

def analyze_sentiment(text):
    try:
        result = classifier(text)[0]
        logging.info("Sentiment analysis result: %s", result)
        
        if 'label' in result:
            return result['label']
        else:
            return None
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

def submit_issue(name, email, item, issue):
    sentiment_label = analyze_sentiment(issue)
    
    if sentiment_label is None:
        return {"error": "Failed to analyze sentiment"}
    
    new_customer = Customer(name, email, item, issue, sentiment_label)
    
    fraud_message = detect_fraud(new_customer)
    if fraud_message:
        return {"error": fraud_message}
    
    issues.append(new_customer)
    
    return {
        "message": "Issue submitted successfully!",
        "sentiment_label": sentiment_label
    }

def view_issues():
    if not issues:
        return "No issues have been submitted yet."
    else:
        result = "Here are the submitted issues:\n"
        for idx, customer in enumerate(issues, start=1):
            result += f"Issue {idx}:\nName: {customer.name}\nEmail: {customer.email}\nItem: {customer.item}\nIssue: {customer.issue}\nSentiment: {customer.sentiment_label}\n\n"
        return result

# Example usage:
# submit_issue("John Doe", "john@example.com", "pen", "The pen is not working properly.")
# print(view_issues())
