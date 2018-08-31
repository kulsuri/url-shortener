# url-shortener
Python web app built with Flask to shorten urls via rest api

# Pre-requisites
- Python 3.6

# Installation Instructions
1. Open command prompt (windows) or terminal (mac/linux)
2. Navigate to the project path: 
```
cd C:\path\to\url-shortener
```
3. Run the command:
```
pip install -r requirements.txt
```
# Running the App
1. Run the command: 
```
python app.py
```
2. Use an application like Postman to make GET/POST requests
- Note: if you want a new empty database, please delete the urls.db

# Shorten URL Example - POST Request
- Request type:
```
POST
```
- URL: 
```
localhost:5000/shorten_url
```
- Headers: 
```
{'Content-Type': 'application/json'}
```
- Body: 
```
{'url': 'www.babylonhealth.com'}
``` 
- Response: 
```
{"shortened_url": "http://localhost:5000/25t52"}
```

# Redirect Example - GET Request
- Request type:
```
GET
```
- URL: 
```
localhost:5000/25t52
```
- Response: redirected to the the original URL (http://babylonhealth.com) / returned the contents of the original URL

# View SQLite Database - GET Request
- Request type:
```
GET
```
- URL: 
```
localhost:5000
```
- Response:
```
[
  [
    1, 
    "http://w3.com", 
    "867nv"
  ], 
  [
    2, 
    "http://babylonhealth.com", 
    "25t52"
  ], 
  [
    3, 
    "http://google.com", 
    "ghpzy"
  ], 
  [
    4, 
    "http://theverge.com", 
    "6vyv6"
  ], 
  [
    5, 
    "http://hotukdeals.com", 
    "pbq8b"
  ], 
  [
    6, 
    "http://youtube.com", 
    "4xct4"
  ]
]
```
# Scaling
The solution allows for scaling due to:
- suitable error handling
- url validation reducing computational expense
- url normalization/formatting to prevent replication in the database
- built with functional programming in mind
- shortened urls are stored in a sqlite database, separate to the code, for fast retrieval 

How I would scale the app:
- run the application on a proper web server such as Apache or Nginx that supports execution of python
- these will easily handle many simultaneous connections
