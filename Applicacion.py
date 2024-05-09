from flask import Flask, render_template, request 
import mysql.connector
import random
Questions=["What is your favorite color?",\
           "What is your favorite animal?",\
            "What is your favorite food?",\
            "What is your favorite movie?",\
            "What is your favorite book?",\
            "What is your favorite game?",\
            "What is your favorite sport?",\
            "What is your favorite TV show?",\
            "What is your favorite music?",\
            "What is your favorite song?"]

def CreatDataBase():
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="")
    cursor=connexion.cursor()
    query="CREATE DATABASE IF NOT EXISTS `Users`;"
    cursor.execute(query)
    connexion.commit()
    connexion.close()
    return True
CreatDataBase()
def ConsultarUser(Username,Password):
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
    cursor=connexion.cursor()
    query="SELECT * FROM `UserData` WHERE `username`=%s AND `password`=%s;"
    cursor.execute(query, (Username, Password))
    result=cursor.fetchall()
    connexion.close()
    return result
def ConsultarEmail(Username,Email):
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
    cursor=connexion.cursor()
    query="SELECT * FROM `UserData` WHERE `username`=%s AND `email`=%s;"
    cursor.execute(query, (Username, Email))
    result=cursor.fetchall()
    connexion.close()
    return result
def CreateTable():
    connexion = mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
    cursor=connexion.cursor()
    query="""CREATE TABLE IF NOT EXISTS `UserData` \
            (`id` int(11) NOT NULL AUTO_INCREMENT,\
            `name` varchar(255) NOT NULL, \
            `Lastname` varchar(255) NOT NULL,\
            `age` int(11) NOT NULL CHECK (`age` >= 18),\
            `password` varchar(255) NOT NULL,\
            `email` varchar(255) NOT NULL CHECK (`email` LIKE '%@%.%'),\
            `Datereg` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
            `Username` varchar(255) NOT NULL,\
            `Gender` varchar(255) NOT NULL CHECK (`Gender` = 'Male' OR `Gender` = 'Female'),\
            `Question` varchar(255) NOT NULL ,\
            `Answer` varchar(255) NOT NULL,\
            PRIMARY KEY (`id`)) ;"""
    cursor.execute(query)
    connexion.commit()
    connexion.close()
    return True
CreateTable()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
    message=""
    if request.method == "POST":
        username=request.form["Username"]
        password=request.form["password"]
        results=ConsultarUser(username,password)
        if len(results) ==0:
            message="Invalid username or password"
            return render_template("confirmationLogin.html", message=message)
        else:
            message="Login Successful"
            return render_template("confirmationLogin.html", message=message)
@app.route("/signUp", methods=["get"])
def signUp():
    Question=random.choice(Questions)
    return render_template("sign.html", Question=Question)
@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        name = request.form["Name"]
        lastname = request.form["Lastname"]
        age = request.form["age"]
        email = request.form["email"]
        username = request.form["Username"]
        gender = request.form["gender"]
        password = request.form["password"]
        question = request.form["Question"]
        answer = request.form["Answer"]

        connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
        cursor = connection.cursor()
        query = "INSERT INTO `UserData` (`name`, `Lastname`, `age`, `password`, `email`, `Username`, `Gender`, `Question`, `Answer`) \
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (name, lastname, age, password, email, username, gender, question, answer))
        connection.commit()
        connection.close()

    return render_template("login.html")

@app.route("/ForgotPassword")
def ForgotPassword():
    return render_template("forgetPassword.html")
Answer=""
@app.route("/ConfirmationForgetPassword", methods=["POST"])
def ConfirmationForgetPassword():
    message=""
    if request.method=="POST":
        email=request.form["email"]
        Username=request.form["Username"]
        result=ConsultarEmail(Username,email)
        if len(result) == 0:
            message="This email or username is not correct"
            return render_template("confirmationForgetPasswordStep1.html", message=message)
        else:
            message="We hope you can answer this question"
            global Answer
            Answer=result[0][10]
            return render_template("confirmationForgetPasswordStep2.html", Question=result[0][9], message=message)

@app.route("/AnswerForgetPassword", methods=["POST"])
def AnswerForgetPassword():
    if request.method == "POST":
        answer_user = request.form["AnswerUser"]
        answer_correct = Answer
        if answer_user == answer_correct:
            return render_template("restarPassword.html", AnswerCorrect=answer_correct)
        else:
            return render_template("confirmationForgetPasswordStep1.html", message="You have entered the wrong answer")
@app.route("/restarPassword", methods=["POST"])
def restarPassword():
    if request.method=="POST":
        password=request.form["password"]
        AnswerCorrect=request.form["AnswerCorrect"]
        connection=mysql.connector.connect(host="localhost", user="root", passwd="", database="Users")
        cursor = connection.cursor()
        query="UPDATE `UserData` SET `password`=%s WHERE `Answer`=%s;"
        cursor.execute(query, (password, AnswerCorrect))
        connection.commit()
        connection.close()
        message="Your password has been changed successfully"
        return render_template("PasswordChanged.html", message=message)
    


app.run(host="localhost", port=5000, debug=True)
