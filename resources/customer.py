from flask_restful import Resource, fields, marshal
from services.mysql import Database

customer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'address': fields.String
}


class CustomerResource(Resource):

    def get(self, customer_id=None):
        db = Database(db_host="127.0.0.1", db_user='root', db_password='root', db_name='crocosoft')
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return marshal(customer, customer_fields), 200
