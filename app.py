from flask import Flask, render_template,redirect,request,url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "flash-message"

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskcrud'

mysql = MySQL(app)

@app.route('/')

def index():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    data = cur.fetchall()
    cur.close()

    return render_template ('base.html',student = data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method=="POST":
        flash("Data inserted successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (name,email,phone) VALUES (%s,%s,%s)",(name,email,phone))
        mysql.connection.commit()

        return redirect(url_for('index'))

@app.route('/update',methods =['POST','GET'])

def update():

    if request.method=="POST":

        id_data =request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE student SET name=%s, email=%s, phone=%s WHERE id=%s",(name,email,phone,id_data))
        flash("data updated succesfuly")
        mysql.connection.commit()

        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>',methods=['POST','GET'])
def delete(id_data):
    cur= mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE id=%s",(id_data))
    flash("student deleted")
    mysql.connection.commit()
    return redirect(url_for('index'))


if __name__=="__main__":

    app.run(debug=True)