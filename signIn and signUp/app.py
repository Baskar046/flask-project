from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='Bas@2004'
app.config['MYSQL_DB']='login_page'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def home():
    msg=''
    if request.method=='POST':
        re_name=request.form['reg_name']
        re_mobile=request.form['reg_mobile']
        re_email=request.form['reg_email']
        re_password=request.form['reg_password']


        if re_name and re_mobile and re_email and re_password:
            conn=mysql.connection.cursor()

            check_query="SELECT 1 FROM user_account WHERE user_email=%s or user_mobile_no=%s LIMIT 1"
            conn.execute(check_query,(re_email,re_mobile))
            existing=conn.fetchone()

            if existing:
                msg="Email or password is already exist!"
                conn.close()
                return render_template('homepage.html',msg=msg)

            if re_name and re_mobile and re_email and re_password:
                conn=mysql.connection.cursor()
                query="INSERT INTO user_account(user_name, user_mobile_no, user_email, user_password) VALUES (%s,%s,%s,%s)"
                conn.execute(query,(re_name,re_mobile,re_email,re_password,))
                mysql.connection.commit()
                conn.close()
                return redirect(url_for('login'))
            else:
                msg="FILL ALL FIELDS"
    return render_template('homepage.html',msg=msg)

@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST':
        lo_email=request.form['log_email']
        lo_password=request.form['log_pass']
        conn=mysql.connection.cursor()
        conn.execute('SELECT * FROM user_account WHERE user_email=%s AND user_password=%s',(lo_email,lo_password))
        account=conn.fetchone()
        conn.close()
        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['email']=account['user_email']
            return redirect(url_for('view'))
        else:
            msg='INVALID EMAIL OR PASSWORD'
    return render_template('login.html',msg=msg)

@app.route('/view')
def view():
    if not session.get('loggedin'):
        return redirect(url_for('login'))
    return render_template('viewpage.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__=='__main__':
    app.secret_key="1234"
    app.run(debug=True)