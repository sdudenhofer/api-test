import flask
from flask import request, jsonify
import pyodbc
import configparser
import pandas as pd
#from flask_cors import CORS

app = flask.Flask(__name__)
# app.config["DEBUG"] = True
#cors = CORS(app, resources={r"/api/centene/seq/1/*": {"origins": "*"}})

config = configparser.ConfigParser()
config.read('../config.ini')
server = config['AS400']['ODBC']
user = config['AS400']['USER']
pwd = config['AS400']['PASS']

conn = pyodbc.connect(DSN=server, UID=user, PWD=pwd)

#def dict_factory(cursor, row):
#    d = {}
#    for idx, col in enumerate(cursor.description):
#        d[col[0]] = row[idx]
#    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>TEST API</h1>
    <p>Test API For database reading</p>'''

@app.route('/api/centene/seq/1/all', methods = ['GET'])
def api_seq_1_all():
    data = []
    cur = conn.cursor()
    all_records = cur.execute('SELECT PATNO, SEQNO, INSCO, POLICY FROM HOSPF062.BENEFITS T01\
                            WHERE SEQNO = 1 AND INSCO IN (411, 901) ORDER BY  PATNO ASC LIMIT 50').fetchall()
    # query = "SELECT PATNO, SEQNO, INSCO, POLICY FROM HOSPF062.BENEFITS T01\
    #         WHERE SEQNO = 1 AND INSCO IN (411, 901) ORDER BY  PATNO ASC LIMIT 50"
    count = 0
    for row in all_records:
        output = [
            {
            'id': str(count),
            'patient_number' : str(row[0]),
            'sequence_number': str(row[1]),
            'insurance_company': str(row[2])
            },
        ]
        data.append(output)
        count += 1
    # data = pd.read_sql(query, conn)
    # df = pd.DataFrame(data)
    # data = df.to_json(orient='split')
    return jsonify(data)

@app.route('/api/centene/seq/2/all', methods = ['GET'])
def api_seq_2_all():
    data = []
    cur = conn.cursor()
    all_records = cur.execute('SELECT PATNO, SEQNO, INSCO, POLICY FROM HOSPF062.BENEFITS T01\
                             WHERE SEQNO = 2 AND INSCO IN (411, 901) ORDER BY  PATNO ASC LIMIT 50').fetchall()
    count = 0
    for row in all_records:
        output = {
            'id': str(count),
            'patient_number' : str(row[0]),
            'sequence_number': str(row[1]),
            'insurance_company': str(row[2])
            },
        
        data.append(output)
        count += 1
    return jsonify(data)
@app.route('/api/hr/<account>')
def hr(account):
    data = []
    cur = conn.cursor()
    all_records = cur.execute('SELECT iaacct, iadept, iapnam, iahst# FROM hospf062.indaccum where iaacct = ' + account)
    count = 0
    for row in all_records:
        output = {
            'account_number' : str(row[0]),
            'department': str(row[1]),
            'patient_name': str(row[2]),
            'hist_num': str(row[3])
        },
        data.append(output)
        count += 1
    return jsonify(data)

app.run()