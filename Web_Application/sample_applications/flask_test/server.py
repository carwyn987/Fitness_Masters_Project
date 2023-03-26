'''
Source: https://www.linode.com/docs/guides/create-restful-api-using-python-and-flask/ 

Run via:
$ export FLASK_APP=server.py
$ flask run

http://127.0.0.1:5000/programming_languages?before_year=1967&after_year=0
'''

from flask import Flask, request
app = Flask(__name__)

in_memory_datastore = {
   "COBOL": {"name": "COBOL", "publication_year": 1960, "contribution": "record data"},
   "ALGOL": {"name": "ALGOL", "publication_year": 1958, "contribution": "scoping and nested functions"},
   "APL": {"name": "APL", "publication_year": 1962, "contribution": "array processing"},
   "BASIC": {"name": "BASIC", "publication_year": 1964, "contribution": "runtime interpretation, office tooling"},
   "PL": {"name": "PL", "publication_year": 1966, "contribution": "constants, function overloading, pointers"},
   "SIMULA67": {"name": "SIMULA67", "publication_year": 1967,
                "contribution": "class/object split, subclassing, protected attributes"},
   "Pascal": {"name": "Pascal", "publication_year": 1970,
              "contribution": "modern unary, binary, and assignment operator syntax expectations"},
   "CLU": {"name": "CLU", "publication_year": 1975,
           "contribution": "iterators, abstract data types, generics, checked exceptions"},
}

# This annotation is the event that occurs when a request comes to this address and path
# @app.get('/programming_languages')
# def list_programming_languages():
#    return {"programming_languages":list(in_memory_datastore.values())}

@app.get('/programming_languages')
def list_programming_languages():
   before_year = request.args.get('before_year') or '30000'
   after_year = request.args.get('after_year') or '0'
   qualifying_data = list(
       filter(
           lambda pl: int(before_year) > pl['publication_year'] > int(after_year),
           in_memory_datastore.values()
       )
   )

   return {"programming_languages": qualifying_data}

@app.route('/programming_languages/<programming_language_name>')
def get_programming_language(programming_language_name):
   return in_memory_datastore[programming_language_name]