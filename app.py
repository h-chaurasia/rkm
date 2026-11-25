from flask import Flask, render_template, url_for, request, redirect, session
import random
import csv
import pickle
import os
from os.path import exists
import pandas as pd
import azureml.automl.core

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.secret_key = "abc"

@app.route("/")
@app.route("/home")
def index():
    return render_template('home.html')

@app.route('/check_file')
def check_file():
    if 'uname' in session:
        session.clear()
        return render_template('check_file.html')
    return redirect(url_for('index'))

@app.route('/first_handler', methods=['POST'])
def first_handler():
    if request.method == "POST":
        rand = str(random.randrange(1, 1000))
        session["rand"] = rand
        dir_path = os.path.join('static/in_out', rand)
        if exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        uhml = request.form['uhml']
        ui = request.form['ui']
        mic = request.form['mic']
        strength = request.form['str']
        e = request.form['e']
        count = request.form['count']
        input_fname = os.path.join(dir_path, "input_file.csv")
        output_fname = os.path.join(dir_path, "output_file.csv")
        f = open(input_fname, 'w')
        writer = csv.writer(f)
        writer.writerow(['UHML', 'UI', 'Mic', 'Str', 'E', 'Count'])
        writer.writerow([uhml, ui, mic, strength, e, count])
        f.close()
        try:
            code(input_fname, output_fname)
        except:
            return render_template('check_file.html')
        return "successfully done"
    return redirect(url_for('index'))

@app.route('/output', methods=['GET', 'POST'])
def output():
    if 'rand' in session:
        rand = session['rand']
        fname = "in_out/" +rand +"/" + "output_file.csv"
        result_fname = os.path.join('static', fname)
        #while(True):
        if not exists(result_fname):
            session.clear()
            return render_template('check_file.html')
        elif(exists(result_fname)):
            result_f = open(result_fname, 'r')
            result_line = result_f.readline()
            a = True
            result = []
            while a:
                result_line = result_f.readline()
                if not result_line:
                    a=False
                    break
                result.append(result_line.split(","))
            result_f.close()
            session.clear()
            return render_template('output.html', result = result, fname = fname)
    return redirect(url_for('index'))

@app.route('/second_handler', methods=['POST'])
def second_handler():
    if request.method == "POST":
        rand = str(random.randrange(1, 1000))
        session["rand"] = rand
        dir_path = os.path.join('static/in_out', rand)
        if exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
        f= request.files['csv_file']
        input_fname = os.path.join(dir_path, "input_file.csv")
        output_fname = os.path.join(dir_path, "output_file.csv")
        if f.filename != '':
            f.save(input_fname)
        try:
            code(input_fname, output_fname)
        except:
            return render_template('check_file.html')
        return "successfully done"
    return redirect(url_for('index'))

def code(input_fname, output_fname):
    #print("code")
    with open('rkm_model.pkl', 'rb') as f:
        rkm_model = pickle.load(f, encoding='latin1')
        #print("rkm")
        data = pd.read_csv(input_fname)
        df = pd.DataFrame(data)
        tenacity = rkm_model.predict(df)
        data['Tenacity'] = tenacity
        data.to_csv(output_fname, index=False)


if __name__=="__main__":
    app.run()
