#!/usr/bin/env python

from datetime import datetime
import evdev
from evdev import ecodes
import mysql.connector
import sys

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

scanner = evdev.InputDevice('/dev/input/{}'.format(sys.argv[1]))
scanner.grab()

def init_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="besuchertracker")

db = init_db()

def get_cursor():
    global db
    try:
        db.ping(reconnect=True, attempts=2, delay=1)
    except mysql.connector.Error as err:
        db = init_db()
    return db.cursor(prepared=True)

ID_LENGTH = 5


track_user_stmt = 'INSERT INTO verlaufsdaten (zeitstempel, besucher_id, aktion) VALUES (%s, %s, %s)'
check_id_stmt = 'SELECT zustand FROM zustandsdaten WHERE besucher_id = %s LIMIT 1'
insert_status_stmt = 'INSERT INTO zustandsdaten (besucher_id, zustand) VALUES (%s, %s)'
update_status_stmt = 'UPDATE zustandsdaten SET zustand = %s WHERE besucher_id = %s'

STATUS_MESSAGE=('KOMMT','GEHT','RESERVIERT')
status = 'kommt'

def handle(scan):
    global status

    if scan in STATUS_MESSAGE:
        status = scan.lower()
        print('Register status "{}"'.format(status))
    elif len(scan) == ID_LENGTH:
        try:
            id = int(scan)
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            cursor = get_cursor()
            cursor.execute(track_user_stmt, (now, id, status))
            cursor.execute(check_id_stmt, (id,))
            z = cursor.fetchall()
            if len(z) == 0:
                cursor.execute(insert_status_stmt, (id, status))
            else:
                cursor.execute(update_status_stmt, (status, id))

            db.commit()
            cursor.close()
            print('{} ID {} {}'.format(now, id, status))
        except mysql.connector.Error as e:
            print('Warning: Database Error - we are losing data! (Scan: {} / Status: {}) ({})'.format(scan, status, e))
        except Exception as e:
            print('Not a valid ID or other exception: {} ({})'.format(scan, e))
    else:
        print(scan)

def scan():
    result = ''
    for event in scanner.read_loop():
        if event.type == ecodes.EV_KEY:
            key = evdev.categorize(event)
            if key.keystate == 1: # Key DOWN
                if key.scancode == 28:
                    handle(result)
                    result = ''
                else:
                    chr=scancodes.get(key.scancode)
                    if chr == None:
                        chr='<{}>'.format(key.scancode)
                    result += chr

if __name__ == '__main__':
    scan()

