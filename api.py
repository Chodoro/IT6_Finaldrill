from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Database configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "company"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
# Fetch data from the database
def fetch_data(query, args=()):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    data = cur.fetchall()
    cur.close()
    return data
# Executes a query that modifies data
def execute_query(query, args=()):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows
# Welcome/Homepage
@app.route("/")
def welcome():
    return """<h1>Amazing, Creative, and Exceptional Employee DatabACE</h1>
    <p>Click <a href="/employees">here</a> to view ACE employees</p>"""
#
@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        data = fetch_data("SELECT * FROM employee")
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)
# read function 
@app.route("/employees/<int:ssn>", methods=["GET"])
def get_employee_by_ssn(ssn):
    try:
        data = fetch_data("SELECT * FROM employee WHERE ssn = %s", (ssn,))
        if data:
            return make_response(jsonify(data), 200)
        else:
            return make_response(jsonify({"Error": "Employee not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)
# add/create employee function
@app.route("/employees", methods=["POST"])
def add_employee():
    try:
        info = request.get_json()
        required_fields = ["Fname", "Minit", "Lname", "Bdate", "Address", "Sex", "Salary", "Super_ssn", "DL_id"]
        if not all(field in info for field in required_fields):
            return make_response(jsonify({"Error": "Missing required fields"}), 400)

        query = """INSERT INTO employee (Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, DL_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        args = (info["Fname"], info["Minit"], info["Lname"], info["Bdate"], info["Address"], info["Sex"], info["Salary"], info["Super_ssn"], info["DL_id"])
        affected_rows = execute_query(query, args)

        return make_response(jsonify({"Message": "New Employee Added!", "Affected Rows": affected_rows}), 201)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)
# update employee data function
@app.route("/employees/<int:ssn>", methods=["PUT"])
def update_employee(ssn):
    try:
        info = request.get_json()
        required_fields = ["Fname", "Minit", "Lname", "Bdate", "Address", "Sex", "Salary", "Super_ssn", "DL_id"]
        if not all(field in info for field in required_fields):
            return make_response(jsonify({"Error": "Missing required fields"}), 400)

        query = """UPDATE employee
                   SET Fname = %s, Minit = %s, Lname = %s, Bdate = %s, Address = %s, Sex = %s, Salary = %s, Super_ssn = %s, DL_id = %s 
                   WHERE ssn = %s"""
        args = (info["Fname"], info["Minit"], info["Lname"], info["Bdate"], info["Address"], info["Sex"], info["Salary"], info["Super_ssn"], info["DL_id"], ssn)
        affected_rows = execute_query(query, args)

        if affected_rows == 0:
            return make_response(jsonify({"Error": "Employee not found"}), 404)
        return make_response(jsonify({"Message": "Employee Updated!", "Affected Rows": affected_rows}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)
# delete employee function
@app.route("/employees/<int:ssn>", methods=["DELETE"])
def delete_employee(ssn):
    try:
        affected_rows = execute_query("DELETE FROM employee WHERE ssn = %s", (ssn,))
        if affected_rows == 0:
            return make_response(jsonify({"Error": "Employee not found"}), 404)
        return make_response(jsonify({"Message": "Employee Deleted!", "Affected Rows": affected_rows}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)
# search feature for postman
@app.route("/employees/search", methods=["GET"])
def search_employees():
    try:
        query_params = request.args
        query = "SELECT * FROM employee WHERE "
        conditions = []
        values = []

        if 'Fname' in query_params:
            conditions.append("Fname LIKE %s")
            values.append(f"%{query_params.get('Fname')}%")
        if 'Lname' in query_params:
            conditions.append("Lname LIKE %s")
            values.append(f"%{query_params.get('Lname')}%")
        if 'Address' in query_params:
            conditions.append("Address LIKE %s")
            values.append(f"%{query_params.get('Address')}%")
        if 'Sex' in query_params:
            conditions.append("Sex = %s")
            values.append(query_params.get('Sex'))
        if 'DL_id' in query_params:
            conditions.append("DL_id = %s")
            values.append(query_params.get('DL_id'))
        if 'Super_ssn' in query_params:
            conditions.append("Super_ssn = %s")
            values.append(query_params.get('Super_ssn'))

        if not conditions:
            return make_response(jsonify({"Error": "No valid search criteria provided."}), 400)

        query += " AND ".join(conditions)

        data = fetch_data(query, tuple(values))
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)
