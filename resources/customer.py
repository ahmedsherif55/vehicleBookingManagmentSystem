from flask_restful import Resource, fields, marshal, reqparse
from services.mysql import Database
from http import HTTPStatus

customer_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'address': fields.String
}

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help='name parameter is required')
parser.add_argument('phone', type=str, help='phone parameter is required')
parser.add_argument('email', type=str, help='email parameter is required')
parser.add_argument('address', type=str, help='name parameter is required')

db = Database(db_host="127.0.0.1", db_user='root', db_password='root', db_name='crocosoft')


class CustomerResource(Resource):

    def get(self, customer_id=None):
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Retrieved successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def post(self):
        args = parser.parse_args()
        customer_id = db.insert(table='customers', fields=args)
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Inserted successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def put(self, customer_id=None):
        args = parser.parse_args()
        db.update(table='customers', table_key='id', table_key_value=customer_id, fields=args)
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Updated successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def delete(self, customer_id=None):
        db.delete(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Deleted successfully.", "status": HTTPStatus.OK}
