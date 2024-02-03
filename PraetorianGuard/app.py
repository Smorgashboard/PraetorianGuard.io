from flask import Flask, request, send_file, send_from_directory, render_template
import random
import string
import logging
import io
import base64
import time
import psycopg2
from configparser import ConfigParser
from datetime import datetime

logging.basicConfig(filename="PixelLog.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db ={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        logging.debug("Ya done messed up the SQL connection")

    return db

params = config ()
logging.debug("Connecting to Postgres")
conn = psycopg2.connect(**params)
cur = conn.cursor()
logging.debug(conn.get_dsn_parameters())

def id_gen(x):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(x))

app = Flask(__name__)

def gotYou(userid):
    ### add sanitization. Require exact chars and remove anything that not alphanumeric
    userIDUpdateSQL = """INSERT INTO tracking(user_id,email_time,email_clicked) VALUES(%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET (user_id,email_time,email_clicked) = (EXCLUDED.user_id,EXCLUDED.email_time,EXCLUDED.email_clicked);"""
    noCap = True
    capturedTime = datetime.now()
    cur.execute(userIDUpdateSQL, (userid,capturedTime,noCap))
    conn.commit() 
    
def gotYouLink(userid):
    linkclickedSQL = """INSERT INTO tracking(user_id,link_time,link_clicked) VALUES(%s,%s,%s) ON CONFLICT (user_id) DO UPDATE SET (user_id,link_time,link_clicked) = (EXCLUDED.user_id,EXCLUDED.link_time,EXCLUDED.link_clicked);"""
    noCap = True
    capturedTime = datetime.now()
    logging.debug(userid)
    cur.execute(linkclickedSQL, (userid,capturedTime,noCap))
    conn.commit()

@app.route("/linkclicked", methods=['GET'])

def fakeLogin():
    whoami = request.args
    userid = whoami['uid']
    gotYouLink(userid)
    return render_template('/emailforms/fakelogin.html')

@app.route("/pixel.gif", methods=['GET'])

def pacman():
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    headers = request.headers
    str_headers = str(headers)
    print(str_headers)
    whoami = request.args
    userid = whoami['uid']
    logging.debug(whoami)
    logging.debug(userid)
    gif_str = base64.b64decode(gif)
    logging.info("Action tracked")
    if "Referer" in headers:
        if headers["Referer"]  == 'http://mail.google.com/':
            print("ignore off google")
            return send_file(io.BytesIO(gif_str), mimetype='image/gif')
        else:
            gotYou(userid)
            return send_file(io.BytesIO(gif_str), mimetype='image/gif')
    else:
        gotYou(userid)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')