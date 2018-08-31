# modules
from flask import Flask, jsonify, abort, make_response, request, redirect
from urllib.parse import urlparse
import short_url
import json
import validators
import os
import sqlite3
from sqlite3 import Error, OperationalError

# create an instance of the web app
app = Flask(__name__)

# create SQLite database urls.db in application root folder
def create_sqlite_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        conn.close()

# check shortened_urls table has been created in the urls.db database
def check_table_exists_in_sqlite_db():
    create_table = """
        CREATE TABLE shortened_urls(
            ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            URL TEXT NOT NULL, 
            SHORTENED_URL TEXT NOT NULL);
            """
    try:
        run_query_db2(create_table, None, None, True)
    except OperationalError:
        pass # pass if table has already been created

#run sql query against the urls.db database
def run_query_db2(query, variable, fetch, commit):
    conn = sqlite3.connect('urls.db')
    cur = conn.cursor()
    if variable == None:
        query_result = cur.execute(query)
    elif len(variable) == 1:
        query_result = cur.execute(query, (variable[0],))
    elif len(variable) == 2:
        query_result = cur.execute(query, (variable[0],variable[1]))
    if fetch == 'one':
        query_result = query_result.fetchone()
    elif fetch == 'all':
        query_result = query_result.fetchall()
    elif fetch == None:
        pass
    if commit == True:
        conn.commit()
    elif commit == False:
        pass
    conn.close()
    return query_result

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
        # remove 'www.' from the start of urls and lowercase for consistency & avoid replication 
         netloc = netloc[4:].lower()
    p = p._replace(netloc=netloc, path=path)
    return p.geturl()

# check if url already exists in url_db
def check_url_in_db(normalized_url):
    select_row = "SELECT URL FROM SHORTENED_URLS WHERE URL=?"
    query = run_query_db2(select_row, [normalized_url], 'one', False)
    if query:
        return True
    else:
        return False

# get the shortened url from the url_db database
def get_shortened_url_in_db(normalized_url):
    select_row = "SELECT SHORTENED_URL FROM SHORTENED_URLS WHERE URL=?"
    query = run_query_db2(select_row, [normalized_url], 'one', False)[0]
    json_response = jsonify({'shortened_url': request.url_root + query})
    return json_response, 201
    
# get the full url from the url_db database
def get_full_url_in_db(shortened_url):
    # decode the shortened url
    try:
        url_key = short_url.decode_url(shortened_url)
    except:
        return abort(404)
    # define sql query
    select_row = "SELECT URL FROM SHORTENED_URLS WHERE ID=?"
    # find the url key in the url_db
    query = run_query_db2(select_row, [url_key], 'one', False)
    # check if query returns a value
    if query:
        full_url = query[0]
        return redirect(full_url)
    else:
        return abort(404)

# create a new shortened url
def create_url(normalized_url):
    # define sql query
    select_row = "SELECT MAX(ID) FROM shortened_urls"
    # get the max ID number for url shortening algorithm
    query = run_query_db2(select_row, None, 'one', False)
    max_id = query[0]
    # check url.db is not empty
    if max_id == None:
        max_id = 1
    else:
        max_id += 1
    # store full url and shortened url in variables to be inserted into database
    original_url = normalized_url
    shortened_url = short_url.encode_url(max_id)
    # define sql query to insert into db
    insert_row = "INSERT INTO shortened_urls (URL, SHORTENED_URL) VALUES (?, ?)"
    # run the query to insert into db
    query = run_query_db2(insert_row, [original_url, shortened_url], None, True)
    return get_shortened_url_in_db(original_url)

# define route /
@app.route("/", methods=['GET'])
def display_url_db():
    # sql query to get top 50 records from urls.db
    select_all = "SELECT * FROM shortened_urls LIMIT 100"
    # execute query
    query = run_query_db2(select_all, None, 'all', False)
    # return the url_db for viewing
    return jsonify(query), 200

# define GET route /<shortened_url>
@app.route('/<string:shortened_url>', methods=['GET'])
def get_url(shortened_url):
    # get the original url for the shortened url
    redirect_link = get_full_url_in_db(shortened_url) 
    # redirect to the original url
    return redirect_link, 302

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
    if check_url_in_db(normalized_url) == True:
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
    create_sqlite_db(os.path.join(os.getcwd(), 'urls.db'))
    check_table_exists_in_sqlite_db()
    app.run(debug=True)