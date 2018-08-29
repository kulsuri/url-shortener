# modules
from flask import Flask, jsonify, abort, make_response, request, redirect
from urllib.parse import urlparse
import short_url
import json
import validators

# create an instance of the web app
app = Flask(__name__)

# url database
url_db = [
    {
        'id': 1,
        'url': 'http://google.com',
        'shortened_url': '867nv'
    },
    {
        'id': 2,
        'url': 'http://babylonhealth.com',
        'shortened_url': '25t52'
    }
]

# normalize/format urls to a specific format to prevent replication in url_db database
def url_normalizer(unformatted_url):
    p = urlparse(unformatted_url, 'http')
    if p.netloc:
        netloc = p.netloc
        path = p.path
    else:
        netloc = p.path
        path = ''
    if netloc.startswith('www.'):
         netloc = netloc[4:] # remove 'www.' from the start of urls for consistency & avoid replication 
    p = p._replace(netloc=netloc, path=path)
    return p.geturl()

# check if url already exists in url_db
def check_url_in_db(normalized_url):
    if not any(record['url'] == normalized_url for record in url_db):
        return True

# get the shortened url from the url_db database
def get_shortened_url_in_db(normalized_url):
    url = [url for url in url_db if url['url'] == normalized_url]
    return jsonify({'shortened_url': request.url_root + url[0]['shortened_url']}), 201

# get the full url from the url_db database
def get_full_url_in_db(shortened_url):
    # decode the shortened url
    url_key = short_url.decode_url(shortened_url)

    # find the url key in the url_db
    url = [url for url in url_db if url['id'] == url_key]
    
    # error handling
    if len(url) == 0: 
        abort(404)
    
    # return original url
    original_url = url[0]['url']

    return original_url

# create a new shortened url
def create_url(normalized_url):

    new_url = {
            'id': url_db[-1]['id'] + 1,
            'url': normalized_url,
            'shortened_url': short_url.encode_url(url_db[-1]['id'] + 1)
        }

    # append new shorted url to url_db
    url_db.append(new_url)

    return get_shortened_url_in_db(new_url['url'])

# define route /
@app.route("/", methods=['GET'])
def display_url_db():
    return jsonify(url_db) # return the url_db for viewing

# define GET route /<shortened_url>
@app.route('/<string:shortened_url>', methods=['GET'])
def get_url(shortened_url):
    
    # get the original url for the shortened url
    redirect_link = get_full_url_in_db(shortened_url) 

    # redirect to the original url
    return redirect(redirect_link, code=302)

# define POST route /shorten_url
@app.route('/shorten_url', methods=['POST'])
def create_shortened_url():

    # store json post request object in variable
    req_data = request.get_json()

    # error handling request object - if json post request object is empty or missing url key value pair
    if not req_data or not 'url' in req_data: 
        abort(400)

    # normalize/format the url
    normalized_url = url_normalizer(req_data['url'])

    # validate the new normalized/formatted url
    if not validators.url(normalized_url):
        abort(400)

    # check that the url does not exist in the url_db database
    if check_url_in_db(normalized_url) != True:
        return get_shortened_url_in_db(normalized_url) # return the shortened url from the url_db database
    else:
        # create new shortened url o be added to the url_db database
        return create_url(normalized_url)

# define 404 error handler route
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'url not found'}), 404)

# define 400 error handler route
@app.errorhandler(400)
def not_found400(error):
    return make_response(jsonify({'error': '400 - failed to decode json object'}), 400)

# this flask app will be run if app.py is run
if __name__ == '__main__':
    app.run(debug=True)