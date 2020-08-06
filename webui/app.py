#!/usr/bin/env python
import mysql.connector

from flask import Flask, render_template, request, send_from_directory
app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="besuchertracker"
)

cursor = db.cursor(prepared=True)

get_user_stmt = 'SELECT * FROM stammdaten WHERE besucher_id = %s LIMIT 1'
new_user_stmt = '''
                INSERT INTO stammdaten
                  (besucher_id, name, adresse1, plz, adresse2,
                   telefon, email, status, coronawarn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
update_user_stmt = '''
                UPDATE stammdaten
                SET name = %s, adresse1 = %s, plz = %s, adresse2 = %s,
                    telefon = %s, email = %s, status = %s,
                    coronawarn = %s
                WHERE besucher_id = %s
                '''

@app.route('/stammdaten',methods=['POST','GET'])
def stammdaten():
    besucher_id = request.form.get('besucher_id','0')

    print ('Executing database queries')
    cursor.execute(get_user_stmt, (besucher_id,))
    cursor.fetchall()

    if request.method == 'POST':
        # Update entry

        name = request.form.get('name')
        adresse1 = request.form.get('adresse1')
        plz = request.form.get('plz')
        adresse2 = request.form.get('adresse2')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        status = request.form.get('status')
        coronawarn = request.form.get('coronawarn', default=0, type=int)

        if cursor.rowcount == 0:
            print('Adding new user: {}'.format(besucher_id))
            cursor.execute(new_user_stmt, (besucher_id,
                                           name, adresse1, plz, adresse2,
                                           telefon,email,status,coronawarn))
        else:
            print('Updating user {}'.format(besucher_id))
            cursor.execute(update_user_stmt, (name, adresse1, plz, adresse2,
                                              telefon,email,status,coronawarn,
                                              besucher_id))
        db.commit()
    else:
        print('Loading values for user {}'.format(besucher_id))

    return render_template('index.html')

@app.route('/',methods=['GET'])
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
