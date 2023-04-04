from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from services.mysql import Database
from resources.customer import CustomerResource

app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

api = Api(app)
api.prefix = '/api'

api.add_resource(CustomerResource, '/customers', '/customers/<int:customer_id>')


@app.route('/')
def index():
    print(db.get_one(table='brands', table_key='id', table_key_value=1))
    return 'Welcome to Flask !'


if __name__ == '__main__':
    app.run()
