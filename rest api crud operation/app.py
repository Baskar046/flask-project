from flask import Flask, request,render_template
from flask_mysqldb import MySQL
from flask import jsonify

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Bas@2004'
app.config['MYSQL_DB']='flask_db'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/')
def home():
    return render_template("file.html")

@app.route('/users',methods=['POST'])
def user():
    data=request.get_json()
    name=data.get("name")
    age=data.get("age")
    city=data.get("city")

    con=mysql.connection.cursor()
    query="INSERT INTO users (Student_name, Age, city) VALUES (%s,%s,%s)"
    con.execute(query,(name,age,city))
    mysql.connection.commit()
    con.close()
    return jsonify({"status":"success"})

@app.route('/users',methods=['GET'])
def get_user():
    con=mysql.connection.cursor()
    query="SELECT * FROM users"
    con.execute(query)
    rows=con.fetchall()
    con.close()
    return jsonify(rows)

@app.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    con=mysql.connection.cursor()
    con.execute("DELETE FROM users WHERE ID=%s",(user_id,))
    mysql.connection.commit()
    con.close()
    return jsonify({"message": f"user{user_id} deleted successfully"})

@app.route('/view')
def view():
    return render_template('view.html')


@app.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data=request.get_json()
    name=data.get("name")
    age=data.get("age")
    city=data.get("city")

    con=mysql.connection.cursor()
    query="UPDATE users SET Student_name=%s ,Age=%s,city=%s WHERE ID=%s"
    con.execute(query,(name,age,city,user_id))
    mysql.connection.commit()
    con.close()

    return jsonify({"message":f"user{user_id} updated successfully"})


if __name__=='__main__':
    app.run(debug=True)