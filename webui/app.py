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

count_user_status_stmt='''
SELECT
  COUNT(DISTINCT(b.besucher_id)) AS anzahl
  ,IFNULL(z.zustand,"nicht gesehen") AS zustand
  ,IFNULL(s.status,"nicht registriert") AS status
FROM
(SELECT DISTINCT(besucher_id)
 FROM zustandsdaten
 UNION
 SELECT DISTINCT(besucher_id)
 FROM stammdaten) AS b
LEFT JOIN zustandsdaten AS z
ON z.besucher_id = b.besucher_id
LEFT JOIN
  (SELECT besucher_id, status FROM stammdaten) AS s
ON s.besucher_id = b.besucher_id
GROUP BY z.zustand, s.status
ORDER BY s.status, z.zustand
'''


@app.route('/stammdaten',methods=['POST','GET'])
def stammdaten():

    if request.method == 'POST':
        # Update entry from form
        besucher_id = request.form.get('besucher_id', default=0, type=int)
        cursor.execute(get_user_stmt, (besucher_id,))
        besucher = cursor.fetchall()

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
        besucher_id = request.args.get('besucher_id', default=0, type=int)
        cursor.execute(get_user_stmt, (besucher_id,))
        besucher = cursor.fetchall()
        if cursor.rowcount == 0:
            print('Besucher ID {} existiert nicht.'.format(besucher_id))
            if besucher_id == 0:
                besucher_id = ''
            return render_template('stammdaten.html', id = besucher_id)
        else:
            for b in besucher:
                name = b[1].decode()
                adresse1 = b[2].decode()
                plz = b[3].decode()
                adresse2 = b[4].decode()
                telefon = b[5].decode()
                email = b[6].decode()
                status = b[7].decode()
                coronawarn = b[8]

                if besucher_id != b[0]:
                    print('Warning: unexpected ID {} in query for {}'.format(
                        b[0], besucher_id))

                print("""
                ID:      {}
                Name:    {}
                Adresse: {}
                         {} {}
                Telefon: {}
                Email:   {}
                Status:  {}
                CoronaWarn: {}
                """.format(besucher_id, name, adresse1, plz, adresse2, telefon,
                           email, status, coronawarn))

    return render_template('stammdaten.html',
                           id = besucher_id,
                           name = name,
                           adresse1 = adresse1,
                           plz = plz,
                           adresse2 = adresse2,
                           telefon=telefon,
                           email = email,
                           status = status,
                           coronawarn = coronawarn)


@app.route('/verlaufsdaten',methods=['GET'])
def verlaufsdaten():
    return render_template('verlaufsdaten.html')


@app.route('/',methods=['GET'])
def main():
    cursor.execute(count_user_status_stmt)
    counts = cursor.fetchall()
    anwesend = sum((0,anzahl)[zustand.decode() == 'kommt'] for anzahl, zustand, status in counts)
    anwesend_gast = sum((0,anzahl)[status.decode() == 'gast' and zustand.decode() == 'kommt'] for anzahl, zustand, status in counts)
    abwesend = sum((0,anzahl)[zustand.decode() == 'geht' or zustand.decode() == 'reserviert'] for anzahl, zustand, status in counts)
    reserviert = sum((0,anzahl)[zustand.decode() == 'reserviert' and (status.decode() == 'gast' or status.decode() == 'nicht registriert') ] for anzahl, zustand, status in counts)
    registriert = sum((0,anzahl)[status.decode() != 'nicht registriert'] for anzahl, zustand, status in counts)

    return render_template('index.html',
                           counts = counts,
                           anwesend = anwesend,
                           reserviert = reserviert,
                           abwesend = abwesend,
                           registriert = registriert,
                           anwesend_gast = anwesend_gast)

if __name__ == '__main__':
    app.run()
