from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Function to establish a database connection
def get_db_connection():
    conn = psycopg2.connect(
        database="test",
        user="postgres",
        password="123",
        host="localhost",  # Change this to your PostgreSQL server's hostname or IP address
        port="5432",        # Change this to your PostgreSQL server's port
    )
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_data")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("main.html", data=data)

# Add Data
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        height = request.form['height']
        age = int(request.form['age'])
        address = request.form['address']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_data (firstname, lastname, height, age, address) VALUES (%s, %s, %s, %s, %s)",
                       (firstname, lastname, height, age, address))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add.html")

# Update Data
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_data WHERE id = %s", (id,))
    data = cursor.fetchone()
    
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        height = request.form['height']
        age = int(request.form['age'])
        address = request.form['address']
        cursor.execute("UPDATE tbl_data SET firstname=%s, lastname=%s, height=%s, age=%s, address=%s WHERE id=%s",
                     (firstname, lastname, height, age, address, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.close()
    conn.close()
    return render_template("update.html", data=data)

# Delete Data
@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_data WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("index"))
    return render_template("delete.html")

if __name__ == "__main__":
    app.run(debug=True)
