# modules
from flask import Flask
#from flask_restful import Resource, Api

# create an instance of the web app
app = Flask(__name__)
api = Api(app)

class Quotes(Resource):
    def get(self):
        return {
            'ataturk': {
                'quote': ['Yurtta sulh, cihanda sulh.', 
                    'Egemenlik verilmez, alınır.', 
                    'Hayatta en hakiki mürşit ilimdir.']
            },
            'linus': {
                'quote': ['Talk is cheap. Show me the code.']
            }

        }

# define routes
@app.route("/")

# function that will be executed when route localhost:5000/ is accessed
def hello():
    return "Hello World"

# this flask app will be run if app.py is run
if __name__ == '__main__':
    app.run(debug=True)