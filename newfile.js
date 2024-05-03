fetch('https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english', {
  method: 'POST',
  headers: {
    'Authorization': 'AlienX_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    inputs: 'I love coding!',
    parameters: {
      max_length: 50
    }
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
