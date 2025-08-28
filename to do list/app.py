from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="Bas@2004"
app.config["MYSQL_DB"]="To_Do_list"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


@app.route('/')
def home():
    con=mysql.connection.cursor()
    query="SELECT * FROM to_do"
    con.execute(query)
    res=con.fetchall()
    return render_template('homepage.html',datas=res)

#add task
@app.route('/add',methods=['GET','POST'])
def add():
    con=mysql.connection.cursor()
    if request.method=='POST':
        add_task=request.form['add_task']
        query="INSERT INTO to_do (Tasks) VALUES (%s)"
        con.execute(query,(add_task,))
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))
    return render_template('homepage.html')


#update the task
@app.route('/update/<string:id>',methods=['GET','POST'])
def update(id):
    con=mysql.connection.cursor()

    if request.method=='POST':
        new_task=request.form['task']

        query="UPDATE to_do SET Tasks=%s WHERE ID=%s"
        con.execute(query,[new_task,id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for('home'))

    query="SELECT * FROM to_do WHERE ID=%s"
    con.execute(query,[id])
    res=con.fetchone()
    return render_template('update.html',datas=res)


#Delete task
@app.route('/delete/<string:id>',methods=['GET','POST'])    #<'string:id'> it's type cast of url before passing the view function. syntax <container:variable_name>
def delete(id):
    con=mysql.connection.cursor()
    query="DELETE FROM to_do WHERE ID=%s"
    con.execute(query,(int(id),))
    mysql.connection.commit()
    con.close()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)