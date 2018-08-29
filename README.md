# url-shortener
Python web app built with Flask to shorten urls via rest api

# Installation Instructions
1. Open command prompt (windows) or terminal (mac/linux)
2. Navigate to the project path: cd C:\\...\\...\url-shortener
3. Run the command: pip install -r requirements.txt

# Running the App
1. Run the command: python app.py
2. Use an application like Postman to make GET/POST requests

# Shorten URL Example - POST Request
- Request type: POST
- URL: localhost:5000/shorten_url
- Headers: {'Content-Type': 'application/json'}
- Body: {'url': 'www.helloworld.com'} 
- Response: {"shortened_url": "http://localhost:5000/ghpzy"}

# Redirect Example - GET Request
- Request type: GET
- URL: localhost:5000/ghpzy
- Response: redirected to the the original URL (www.helloworld.com) / returned the contents of the original URL