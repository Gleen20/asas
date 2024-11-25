from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'user': 'matthew',      
    'password': 'glenn123',  
    'host': 'localhost',
    'database': 'database_name' 
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM uang')
    uang = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', uang=uang)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO uang (nama, jumlah) VALUES (%s, %s)', (nama, jumlah))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        nama = request.form['nama']
        jumlah = request.form['jumlah']
        
        cursor.execute('UPDATE uang SET nama = %s, jumlah = %s WHERE id = %s', (nama, jumlah, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute('SELECT * FROM uang WHERE id = %s', (id,))
    uang = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', uang=uang)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM uang WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)