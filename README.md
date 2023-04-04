# Vehicle Booking Managment System

This project manages bookings for vehicle rental system.

One model only is currently available: Customers.

Main libraries used:
1. Flask - for creating flask apps.
2. Flask-RESTful - for creating restful API.
3. PyMySQL - adds support for mysql database.
4. Pytest - adds support for testing the app.

Project structure:
```
├── resources
│   ├── customer.py
├── services
│   ├── mysql.py
├── tests
│   ├── unit
│       ├── test_customers.py
│   ├── conftest.py
├── app.py
├── database.py
├── requirements.txt
├── .env
└── README.md
```

* customer - holds customer resource.
* mysql - holds database manager functions.
* test_customers - holds customer unit tests.
* app.py - flask application init.
* database.py - database init.

## Running 

1. Clone repository.
2. pip install requirements.txt
3. Start server by running python app.py runserver

## Usage
### Customers endpoint
GET http://127.0.0.1:5000/api/customers/1

RESPONSE
```json
{
    "message": "Retrieved successfully.",
    "status": 200,
    "data": {
        "id": 1,
        "name": "John John",
        "phone": "112145",
        "email": "john@gmail.com",
        "address": "address",
     }
}
```
POST http://127.0.0.1:5000/api/customers/1

REQUEST
```json
{
    "name": "Hassan",
    "phone": "01115789524",
    "email": "hassan@gmail.com",
    "address": "test address"
}
```
RESPONSE
```json
{
    "message": "Inserted successfully.",
    "status": 200,
    "data": {
        "id": 3,
        "name": "Hassan",
        "phone": "01115789524",
        "email": "hassan@gmail.com",
        "address": "test address"
    }
}
```
```
PUT http://127.0.0.1:5000/api/customers/1

REQUEST
```json
{
    "name": "Hassan updated 2",
    "phone": "055575"
}
```
RESPONSE
```json
{
    "id": 2,
    "name": "Hassan updated 2",
    "phone": "055575",
    "email": "hassan@gmail.com",
    "address": "gassan aaddres"
}
```
DELETE http://127.0.0.1:5000/api/customers/1

RESPONSE
```json
{
    "message": "Deleted successfully.",
    "status": 200
}
```
