#!/usr/bin/env
import json
import time
import datetime
import requests
from flask import Flask, jsonify, request, render_template

import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

@app.route('/')
def index():
    data = loadData()
    times = data[0]
    temps = data[1]
    values = data[2]
    return render_template('index.html', valType="hz",labels=times,temps=temps,values=values,legend="hz")

@app.route('/', methods=['POST'])
def load():
    form = request.form
    val = request.form['data']

    num = 2
    legend = 'MagFluxDens'
    if(val == "gzz"):
        num = 3
        legend = 'Gradient'

    data = loadData()
    times = data[0]
    temps = data[1]
    values = data[num]
    return render_template('index.html', valType=val,labels=times,temps=temps,values=values,legend=legend)

@app.route('/save', methods=['GET','POST'])
def saveData():
    #url will be like .../save?time=xxx&hz=xx&gzz=xx
    time = request.args.get('time')
    hz = request.args.get('hz')
    gzz = request.args.get('gzz')
    temp = loadTemp()
    #print([str(time),str(temp),str(hz),str(gzz)])
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("via").sheet1

    count = len(list(filter(bool,sheet.col_values(1))))
    #print("count of rows = "+str(count))
    if(count > 100):
        sheet.delete_row(1)
        count -= 1

    row = [str(time),str(temp),str(hz),str(gzz)]
    sheet.insert_row(row, count+1)

    out = "save successful"
    return out

@app.route('/getdata', methods=['GET'])
def getData():
    data = loadData()
    output = {"time":data[0],"temp":data[1],"flux_density":data[2],"gradient":data[3]}
    out = json.dumps(output, indent=4)
    return out

def loadTemp():
    url="http://api.openweathermap.org/data/2.5/weather?id=3067696&APPID=d07e3104dd9a21efc80fee413b862fc6"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    data = json.loads(content)["main"]

    temp = round(data["temp"]-273.15,1)
    #print("temp="+str(temp))
    return temp

def loadData():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("via").sheet1

    t = list(filter(bool,sheet.col_values(1)))
    temp = list(filter(bool,sheet.col_values(2)))
    hz = list(filter(bool,sheet.col_values(3)))
    gzz = list(filter(bool,sheet.col_values(4)))
    out = [t,temp,hz,gzz]
    return out

app.run(port=8080, debug=False, threaded=True, host="0.0.0.0")
