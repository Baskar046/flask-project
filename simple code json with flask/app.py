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
    new_id=con.lastrowid
    con.close()
    return jsonify({"id":new_id,"name":name,"age":age,"city":city})

if __name__=='__main__':
    app.run(debug=True)