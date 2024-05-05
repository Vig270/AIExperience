async function fetchSentimentAnalysis(text) {
    try {
        const response = await fetch('https://api-inference.huggingface.co/models/SamLowe/roberta-base-go_emotions', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer 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', // Replace with your actual API key
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                inputs: text,
                parameters: {
                    max_length: 50
                }
            })
        });
        if (!response.ok) {
            throw new Error('Failed to fetch sentiment analysis');
        }
        const data = await response.json();
        return data[0];
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

async function analyzeSentiment(issue) {
    try {
        const sentimentResult = await fetchSentimentAnalysis(issue);
        if (sentimentResult === null) {
            console.log('Sentiment result is null.'); // Debug statement
            return null;
        }
        
        console.log('Sentiment Score:', sentimentResult.score); // Debug statement: Log the sentiment score to the console
        
        // Define threshold values for positive, negative, and neutral sentiment
        const positiveThreshold = 0.9; // Adjust as needed
        const negativeThreshold = 0.2; // Adjust as needed
        const neutralThreshold = 0.5; // Adjust as needed
        
        // Determine sentiment based on the sentiment score
        if (sentimentResult.score >= positiveThreshold) {
            console.log('Sentiment is positive.'); // Debug statement
            return 'Positive';
        } else if (sentimentResult.score <= negativeThreshold) {
            console.log('Sentiment is negative.'); // Debug statement
            return 'Negative';
        } else if (sentimentResult.score >= neutralThreshold && sentimentResult.score < positiveThreshold && sentimentResult.score > negativeThreshold) {
            console.log('Sentiment is neutral.'); // Debug statement
            return 'Neutral';
        } else {
            console.log('Sentiment is uncertain.'); // Debug statement
            return 'Uncertain';
        }
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

document.getElementById('new-issue-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent form submission

    // Get form values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const item = document.getElementById('item').value;
    const issue = document.getElementById('issue').value;

    // Perform sentiment analysis
    const sentimentLabel = await analyzeSentiment(issue);
    if (sentimentLabel === null) {
        // Handle error
        return;
    }

    // Create issue object
    const newIssue = {
        name: name,
        email: email,
        item: item,
        issue: issue,
        sentiment: sentimentLabel // Include sentiment in the issue object
    };

    // Display the submitted issue with sentiment analysis
    displayIssue(newIssue);

    // Clear the form fields
    document.getElementById('new-issue-form').reset();
});

function displayIssue(issue) {
    const issuesList = document.getElementById('issues');
    const issueItem = document.createElement('li');
    issueItem.innerHTML = `Name: ${issue.name}, Email: ${issue.email}, Item: ${issue.item}, Issue: ${issue.issue}<br>
    <div class="sentiment-info">
        <span class="sentiment-label">Sentiment:</span> ${issue.sentiment}
    </div>`;
    issuesList.appendChild(issueItem);
}
