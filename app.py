from flask import Flask
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
import os

app = Flask(__name__)
app.secret_key="Queseria"
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_PORT'] = 3306 #No es necesario pero por las dudas
app.config['MYSQL_DATABASE_BD'] = 'usuarios'
mysql.init_app(app)


CARPETA = os.path.join('IMG')
app.config['CARPETA'] = CARPETA

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    sql = "SELECT * FROM `queseria`.`usuarios`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    usuarios = cursor.fetchall()
    conn.commit()

    return render_template('usuarios/admin.html', usuarios=usuarios)

@app.route('/register')
def register():
    return render_template('usuarios/register.html')


@app.route('/store', methods=['POST'])
def storage():
    nombre = request.form['txtNombre']
    mail = request.form['txtEmail']
    contra = request.form['txtContra']

    if nombre == '' or mail == '' or contra == '':
        flash("Recuerde llenar todos los campos")
        return redirect(url_for('register'))
    
    sql = "INSERT INTO `queseria`.`usuarios` (`id`, `nombre`, `mail`, `contraseña`) VALUES (NULL, %s, %s, %s);"
    datos = (nombre, mail, contra)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/destroy/<int:id>')
def destroy(id):
    sql = "DELETE FROM `queseria`.`usuarios` WHERE id=%s;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    conn.commit()
    return redirect('/admin')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `queseria`.`usuarios` WHERE id=%s;", id)
    usuarios = cursor.fetchall()
    conn.commit()
    return render_template('usuarios/edit.html', usuarios=usuarios)

@app.route('/update', methods=['POST'])
def update():
    nombre = request.form['txtNombre']
    mail = request.form['txtEmail']
    contra = request.form['txtContra']
    id = request.form['txtID']

    sql = "UPDATE `queseria`.`usuarios` SET `nombre`=%s, `mail`=%s, `contraseña`=%s WHERE id=%s;"
    datos=(nombre, mail, contra, id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')

@app.route('/IMG/<nombrefoto>')
def img(nombrefoto):
    return send_from_directory(app.config['CARPETA'],nombrefoto)

if __name__ == '__main__':
    app.run(debug=True)