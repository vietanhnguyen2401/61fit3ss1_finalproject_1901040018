from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM toDo")
    if result >0:
        toDo = cur.fetchall()
        return render_template('index.html', toDo=toDo)
    else:
        return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    toDo = request.form
    itemDescription = toDo['itemDescription']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO toDo(description, status) VALUES (%s, 'Doing')", [itemDescription])
    mysql.connection.commit()
    cur.close()
    return redirect('/') 

@app.route('/edit', methods=['POST'])
def edit():
    toDo = request.values
    id = int(toDo['itemID'])
    itemDescription = toDo['itemDescription']
    action = toDo['clickBtn']
    status = request.form.get('itemStatus')
    cur = mysql.connection.cursor()
    if action == 'delete':
        cur.execute("DELETE FROM toDo WHERE id = %s", [id])
    else:
        if status=='Doing':
            cur.execute("UPDATE toDo SET description = %s, status = 'Done' WHERE id = %s", (itemDescription, id))
        else:
            cur.execute("UPDATE toDo SET description = %s WHERE id = %s", (itemDescription, id))
    mysql.connection.commit()
    cur.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)