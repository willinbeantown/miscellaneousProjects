from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)

class Employees(Resource):
	def get(self):
		conn = db_connect.connect() # connect to db
		query = conn.execute("SELECT * FROM employees") # perform query & return json
		return {'employees': [i[0] for i in query.cursor.fetchall()]} # fetch 1st col from Employee ID

class Tracks(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("SELECT trackid, name, composer, unitprice FROM tracks;") # the ';'?
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
		return jsonify(result)

class Employees_Name(Resource):
	def get(self, employee_id):
		conn = db_connect.connect()
		query = conn.execute("SELECT * FROM employees WHERE EmployeeId=%d" % int(employee_id))
		result = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
		return jsonify(result)


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
	app.run(port='5002')
