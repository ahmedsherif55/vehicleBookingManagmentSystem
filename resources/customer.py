from typing import Optional, Dict, Any

from flask_restful import Resource, fields, marshal, reqparse
from http import HTTPStatus

from database import db

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


class CustomerResource(Resource):
    def get(self, customer_id: Optional[int, None] = None) -> Dict[str, Any]:
        """Gets customer data for a specific id.

        Args:
            customer_id (int):
                The customer identifier.

        Returns:
            (Dict):
                A dictionary with message, http status and customer data.

        """
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Retrieved successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def post(self) -> Dict[str, Any]:
        """Adds a customer record inside the database.

        Returns:
            (Dict):
                A dictionary with message, http status and customer data.

        """
        args = parser.parse_args()
        customer_id = db.insert(table='customers', fields=args)
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Inserted successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def put(self, customer_id: Optional[int, None] = None) -> Dict[str, Any]:
        """Updates a customer record inside the database.

        Args:
            customer_id (int):
                The customer identifier.

        Returns:
            (Dict):
                A dictionary with message, http status and customer data.

        """
        args = parser.parse_args()
        db.update(table='customers', table_key='id', table_key_value=customer_id, fields=args)
        customer = db.get_one(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Updated successfully.", "status": HTTPStatus.OK,
                "data": marshal(customer, customer_fields)}

    def delete(self, customer_id: Optional[int, None] = None) -> Dict[str, Any]:
        """Deletes a customer record from the database.

        Args:
            customer_id (int):
                The customer identifier.

        Returns:
            (Dict):
                A dictionary with message and http status.

        """
        db.delete(table='customers', table_key='id', table_key_value=customer_id)
        return {"message": "Deleted successfully.", "status": HTTPStatus.OK}
