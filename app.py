# modules
from flask import Flask, jsonify, abort, make_response, request, redirect
import short_url
import json
import validators

# create an instance of the web app
app = Flask(__name__)

# json database
url_db = [
    {
        'id': 1,
        'url': 'http://www.google.com',
        'shortened_url': '867nv'
    },
    {
        'id': 2,
        'url': 'http://www.babylonhealth.com',
        'shortened_url': '25t52'
    }
]

# define route /
@app.route("/")
def hello(): # function that will be executed when route localhost:5000/ is accessed
    return "URL Shortener App built with Python and Flask"

# define GET route <shortened_url>
@app.route('/<shortened_url>', methods=['GET'])
def get_url(shortened_url):
    url_key = short_url.decode_url(shortened_url) # decode the shortened url
    url = [url for url in url_db if url['id'] == url_key] # find the url key in the url_db
    if len(url) == 0: # error handling
        abort(404)
    redirect_link = url[0]['url']
    return redirect(redirect_link, code=302) #jsonify({'url': url[0]})

# define POST route /shorten_url
@app.route('/shorten_url', methods=['POST'])
def create_shortened_url():

    req_data = request.get_json() # store json post request object in variable
    
    # error handling
    if not req_data or not 'url' in req_data: # if json post request object is empty or missing url key
        abort(400)
    elif not validators.url(req_data['url']): # if json post request object is invalid url
        return("Error: you must provide a valid URL! For example: http://www.google.com")
    else:
        new_url = {
            'id': url_db[-1]['id'] + 1,
            'url': req_data['url'],
            'shortened_url': short_url.encode_url(url_db[-1]['id'] + 1)
        }

        url_db.append(new_url)
        return jsonify({'url': new_url}), 201


# define 404 error handler route
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'not found'}), 404)

# define 400 error handler route
@app.errorhandler(400)
def not_found400(error):
    return make_response(jsonify({'error': '400 - failed to decode json object'}), 400)

# this flask app will be run if app.py is run
if __name__ == '__main__':
    app.run(debug=True)