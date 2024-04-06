import numpy as np
import pandas as pd

import pymysql
pymysql.install_as_MySQLdb()

gmail_list = []
pswd_list = []
gmail_list1 = []
pswd_list1 = []

from flask import Flask, request, jsonify, render_template
import joblib

model = joblib.load('/Users/sumanthraj/Downloads/Autism.pkl')



app = Flask(__name__, template_folder='template')
@app.route('/')
def home():
    return render_template('register.html', text = 'If you have already registered, click here')
@app.route('/register',methods = ['POST'])
def register():

    int_features2 = [str(x) for x in request.form.values()]
    #print(int_features2)
    #print(int_features2[0])
    #print(int_features2[1])
    r1 = int_features2[0]
    r2 = int_features2[1]
    login = int_features2[0]
    pass1 = int_features2[1]
    db = pymysql.connect(host = "localhost",user = "root",password = '',db = "ddbb")
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1 = cursor.fetchall()
    for row1 in result1:
        gmail_list1.append(str(row1[0]))
    #print(gmail_list1)
    if login in gmail_list1:
        return render_template('register.html', text = "This Username is already in use :(")
    else:
        sql = "INSERT INTO user_register(user, password) VALUES(%s,%s)"
        val = (r1,r2)
        try:
            cursor.execute(sql,val)
            db.commit()
        except:
            db.rollback()
        db.close()
        return render_template('register.html', text = "Successfully Registered!")
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login1', methods = ['POST'])
def login1():
    int_features3 = [str(x) for x in request.form.values()]
    #print(int_feature3)
    logu = int_features3[0]
    passw = int_features3[1]
    db = pymysql.connect(host = "localhost",user = "root",password = "",db = "ddbb")
    cursor = db.cursor()
    cursor.execute("SELECT user FROM user_register")
    result1 = cursor.fetchall()
    for row1 in result1:
        gmail_list.append(str(row1[0]))
    cursor1 = db.cursor()
    cursor1.execute("SELECT password FROM user_register")
    result2 = cursor1.fetchall()
    for row2 in result2:
        pswd_list.append(str(row2[0]))
    #print(gmail_list)
    #print(gmail_list)
    #print(gmail_list.index(logu))
    #print(pswd_list.index(passw))
    if logu not in gmail_list:
        return render_template('login.html', text = 'User does not exist')
    elif logu in gmail_list:
        index_of_pass = gmail_list.index(logu)
        if passw != pswd_list[index_of_pass]:
            return render_template('login.html', text = 'Password is Incorrect')
        elif index_of_pass == pswd_list.index(passw):
            return render_template('index 1.html', prediction_test = 'Click on predict to get results')
@app.route('/Autism_Disease_prediction')
def Autism_Disease_prediction():
    return render_template('index 1.html', prediction_text = 'Click on predict to get results')
@app.route('/Autism_Disease_prediction/predict', methods=['POST'])
def predict():
    int_features = [str(x) for x in request.form.values()]
    a = int_features
    print(a)
    data = a
    print(data)
    dictionary = {"Yes":1,"No":0,"Male":1,"Female":0,"Self":1,"Parent":2,"Health care professional":3,"Relative":4,"Others":5}


    data[0] = int(data[0])
    def get_key(val):
        for key, value in dictionary.items():
            if val == key:
                return value

    data[1] = get_key(data[1])
    data[2] = get_key(data[2])
    data[3] = get_key(data[3])
    data[4] = get_key(data[4])
    data[5] = get_key(data[5])
    data[6] = get_key(data[6])
    data[7] = get_key(data[7])
    data[8] = get_key(data[8])
    data[9] = get_key(data[9])
    data[10] = get_key(data[10])
    data[11] = get_key(data[11])
    data[12] = get_key(data[12])
    data[13] = get_key(data[13])
    data[14] = get_key(data[14])
    data[15] = get_key(data[15])
    data_array = np.array(data)
    data_array = data_array.reshape(1,-1)
    my_prediction = model.predict(data_array)
    my_prediction = int(my_prediction)
    print(my_prediction)

    if my_prediction == 1:
        print("The person has Autism Spectrum Disorder")
        return render_template('index 1.html',prediction_text="The person has Autism Spectrum Disorder")
    else:
        print("The person does not have Autism Spectrum Disorder")
        return render_template('index 1.html',prediction_text="The person does not have Autism Spectrum Disorder")

if __name__ == "__main__":
    app.run(debug = False)

            





    
