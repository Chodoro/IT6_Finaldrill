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

def fetch_data(query, args=()):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    data = cur.fetchall()
    cur.close()
    return data

def execute_query(query, args=()):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    return affected_rows

@app.route("/")
def welcome():
    return """<h1>Employee Database</h1>
    <p>Click <a href="/employees">here</a> to view all employees</p>"""

@app.route("/employees", methods=["GET"])
def get_employees():
    try:
        data = fetch_data("SELECT * FROM employee")
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

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

@app.route("/employees/<int:ssn>", methods=["DELETE"])
def delete_employee(ssn):
    try:
        affected_rows = execute_query("DELETE FROM employee WHERE ssn = %s", (ssn,))
        if affected_rows == 0:
            return make_response(jsonify({"Error": "Employee not found"}), 404)
        return make_response(jsonify({"Message": "Employee Deleted!", "Affected Rows": affected_rows}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)
