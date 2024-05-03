import datetime
from transformers import pipeline

class Customer:
    def __init__(self, name, email, item, issue):
        self.name = name
        self.email = email
        self.item = item
        self.issue = issue
        self.timestamp = datetime.datetime.now()  # Add timestamp attribute

def display_menu():
    print("Hello! AIXperience at your service. How can I help you today?")
    print("1. Submit a new issue")
    print("2. View all submitted issues")
    print("3. What item do you have to submit")
    print("4. Exit")

def submit_issue(issues):
    print("Great! Let's start by getting some information about you.")
    name = input("What is your username? ")
    while True:
        email = input("Enter your valid email address? ")
        if validate_email(email):
            break
        else:
            print("Invalid email address. Please try again.")
            
    item = input("What items did you receive? ")
    issue = input("Please describe your issue: ")
    
    # Perform sentiment analysis on the issue description
    sentiment_analyzer = pipeline("sentiment-analysis")
    sentiment_result = sentiment_analyzer(issue)
    sentiment_score = sentiment_result[0]['score']
    sentiment_label = sentiment_result[0]['label']
    
    print(f"Sentiment Analysis Result: {sentiment_label} (Score: {sentiment_score})")
    
    new_customer = Customer(name, email, item, issue)
    issues.append(new_customer)
    print("Thank you! Your issue has been submitted successfully!")
    # Check for fraud after submission
    check_fraud(new_customer, issues[:-1])
    return new_customer

def view_issues(issues):
    if not issues:
        print("No issues have been submitted yet.")
    else:
        print("Here are the submitted issues:")
        for customer in issues:
            print("Name:", customer.name)
            print("Email:", customer.email)
            print("Items:", customer.item)  
            print("Issue:", customer.issue)
            print()
        
        unique_items = set(customer.item.lower() for customer in issues)
        
        print("\nHistory of items submitted:")
        for item in unique_items:
            print(item)

def validate_email(email):
    if "@" in email and "." in email.split("@")[1]:
        return True
    return False

def check_fraud(new_issue, previous_issues):
    # Define a threshold for the number of issues per email within a time frame
    ISSUE_THRESHOLD = 3
    TIME_FRAME = datetime.timedelta(days=7)

    # if there similarity in items with previous issues
    similar_items = [issue for issue in previous_issues if issue.item.lower() == new_issue.item.lower()]

    # if the same email address is associated with multiple issues in a short period
    current_time = datetime.datetime.now()
    similar_email_count = sum(1 for issue in previous_issues if issue.email == new_issue.email and (current_time - issue.timestamp) < TIME_FRAME)

    # if there number of similar items or the number of issues with the same email address exceeds the threshold
    if len(similar_items) > 1:
        print("Potential fraud detected: Similar items have been reported by multiple customers.")
    if similar_email_count > ISSUE_THRESHOLD:
        print("Potential fraud detected: Multiple issues have been reported using the same email address within a short period.")

def main():
    issues = []  # List to store submitted issues

    while True:
        display_menu()
        choice = input("Please choose an option: ")

        if choice == '1':
            submit_issue(issues)
        elif choice == '2':
            view_issues(issues)
        elif choice == '3':
            view_issues(issues)
        elif choice == '4':
            print("Thank you for using AIXperience. Have a nice day!")
            break
        else:
            print("I'm sorry, I didn't understand that. Please try again.")

if __name__ == "__main__":
    main()
