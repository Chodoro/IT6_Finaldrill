from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "company"

# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

def fetch_data(query, args=()):
    cur = mysql.connection.cursor()
    cur.execute(query, args)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/")
def welcome():
    return """<h1>Employee Database</h1>
    <p>Click <a href="http://127.0.0.1:5000/employees">here</a> to view all employees</p>"""

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
        return make_response(jsonify(data), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

@app.route("/employees", methods=["POST"])
def add_employee():
    try:
        cur = mysql.connection.cursor()
        info = request.get_json()
        fname = info["Fname"]
        minit = info["Minit"]
        lname = info["Lname"]
        bdate = info["Bdate"]
        address = info["Address"]
        sex = info["Sex"]
        salary = info["Salary"]
        super_ssn = info["Super_ssn"]
        DL_id = info["DL_id"]
        cur.execute("""INSERT INTO employee (Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, DL_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (fname, minit, lname, bdate, address, sex, salary, super_ssn, DL_id))
        mysql.connection.commit()

        affected_rows = cur.rowcount
        cur.close()

        return make_response(jsonify({"Message": "New Employee Added!", "Affected Rows": affected_rows}), 201)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

@app.route("/employees/<int:ssn>", methods=["PUT"])
def update_employee(ssn):
    try:
        cur = mysql.connection.cursor()
        info = request.get_json()
        fname = info["Fname"]
        minit = info["Minit"]
        lname = info["Lname"]
        bdate = info["Bdate"]
        address = info["Address"]
        sex = info["Sex"]
        salary = info["Salary"]
        super_ssn = info["Super_ssn"]
        DL_id = info["DL_id"]
        cur.execute("""UPDATE employee
                    SET Fname = %s, Minit = %s, Lname = %s, Bdate = %s, Address = %s, Sex = %s, Salary = %s, Super_ssn = %s, DL_id = %s 
                    WHERE ssn = %s""",
                    (fname, minit, lname, bdate, address, sex, salary, super_ssn, DL_id, ssn))
        mysql.connection.commit()

        affected_rows = cur.rowcount
        cur.close()

        return make_response(jsonify({"Message": "Employee Updated!", "Affected Rows": affected_rows}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

@app.route("/employees/<int:ssn>", methods=["DELETE"])
def delete_employee(ssn):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM employee WHERE ssn = %s", (ssn,))
        mysql.connection.commit()

        affected_rows = cur.rowcount
        cur.close()

        return make_response(jsonify({"Message": "Employee Deleted!", "Affected Rows": affected_rows}), 200)
    except Exception as e:
        return make_response(jsonify({"Error": str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)
