from flask import Flask, render_template, flash ,redirect, request, url_for, session , logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import stop_words
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from pathlib import Path
import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report,confusion_matrix
import pickle
import os
import shutil



app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'files/raw'


stop = stop_words.ENGLISH_STOP_WORDS
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
file = open('model', 'rb')
modelknn = pickle.load(file)
file = open('vector', 'rb')
vectorizer = pickle.load(file)
file_names = []

#init MYSQL

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    processed = re.sub(r"\d+","",normalized)
    y = processed.split()
    return y

class ArticleForm(Form):
    title = StringField('Title')#,[validators.Length(min=1,max=200)])
    body = TextAreaField('Body')#,[validators.Length(min=30)])
    
@app.route('/',methods=["POST","GET"])
def index():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        

        return redirect(url_for('article', body = body))

    return render_template('add_article.html', form=form)


@app.route('/article_catogerized')
def article():
    test_clean_sentences = []
    line = request.args['body']
    b = line
    print(b)
    line = line.strip()
    cleaned = clean(line)
    cleaned = ' '.join(cleaned)
    test_clean_sentences.append(cleaned)
    Test = vectorizer.transform(test_clean_sentences)
    groups = ["","world","politics","Business","sci-fi"]
    predicted_labels_knn = modelknn.predict(Test) 
    flash(groups[predicted_labels_knn[0]],'success')

    return render_template('article.html',  article = b,preditions = [groups[predicted_labels_knn[0]],2,3,4,1,2,3,4])


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles',methods=['POST','GET'])
def articles():
    if request.method == 'POST':
        global file_names
        file_names = []
        for f in request.files.getlist('files'):
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
            file_names.append(f.filename)
        sel_mod  = request.form.get("sel_mod")
        return redirect(url_for('classified',sel_mod=sel_mod))
    models = ['bag of words knn','bag of words SVM' , 'bag of words NB','n grams SVM' , 'n grams NB ','n grams KNN','CNN']
    return render_template('articles.html',models=models)
   
@app.route("/classified")
def classified():
    sel_mod = request.args['sel_mod']
    for file in file_names:
        print(file)
        f = open('files/raw/'+file)
        print(f.read())
    return " true"

@app.route('/delete',methods=['GET','POST'])
def delete():
    fol = Path('files/raw')
    if fol.exists():
        shutil.rmtree('files/raw')
        os.makedirs('files/raw')
    fol = Path('files/1')
    if fol.exists():
        shutil.rmtree('files/1')
        os.makedirs('files/1')
    fol = Path('files/2')
    if fol.exists():
        shutil.rmtree('files/2')
        os.makedirs('files/2')
    fol = Path('files/3')
    if fol.exists():
        shutil.rmtree('files/3')
        os.makedirs('files/3')
    fol = Path('files/4')
    if fol.exists():
        shutil.rmtree('files/4')
        os.makedirs('files/4')
    return redirect(url_for('articles'))

# @app.route("/upload", methods=["POST"])
# def upload():
#     for f in request.files.getlist('files'):
#         f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
#     return 'Upload completed.'


# class Registerform(Form):

#     name = StringField('Name',[validators.Length(min=1,max=30)])
#     username = StringField('Username',[validators.Length(min=1,max=30)])
#     email = StringField('Email',[validators.Length(min=6,max=50)])
#     password = PasswordField('Password',[
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='passwords do not match')
#     ])
#     confirm = PasswordField('confirm password')

# @app.route('/register',methods=['GET','POST'])
# def register():
#     form =Registerform(request.form)

#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email =form.email.data
#         username = form.username.data
#         password = sha256_crypt.encrypt(str(form.password.data))

#         #Create cursor
#         cur = mysql.connection.cursor()

#         #execute query
#         cur.execute("INSERT INTO users(name ,email_id ,user_name ,password ) VALUES(%s, %s, %s, %s)",(name,email,username,password))

#         #Commit to DB
#         mysql.connection.commit()

#         #close connection
#         cur.close()

#         flash('you are now registered and can log in', 'success')

#         return redirect(url_for('login'))
#     return render_template('register.html',form=form)

# #user login
# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method =='POST':
#         #get form feilds
#         username = request.form['username']
#         password_candidate = request.form['password']

#         #craete cursor

#         cur =mysql.connection.cursor()

#         #get user by username
#         result = cur.execute("SELECT * FROM users WHERE user_name=%s",[username])
#         if result>0 :
#             #get hash
#             data = cur.fetchone()
#             password = data['password']

#             #campare passwords
#             if sha256_crypt.verify(password_candidate, password):
#                 #passed
#                 session['logged_in'] = True
#                 session['username'] = username

#                 flash('you are now logged in', 'success')
#                 return redirect(url_for('dashboard'))
#             else:
#                 error = 'Invalid login'
#                 return render_template('login.html', error = error)
#             # cur close
#             cur.close()
#         else:
#             error = 'Username not found'
#             return render_template('login.html', error = error)

#     return render_template('login.html')

# # check if user logged in
# def is_logged_in(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args, **kwargs)
#         else:
#             flash('Unauthorized, please login', 'danger')
#             return redirect(url_for('login'))
#     return wrap


# #logout
# @app.route('/logout')

# def logout():
#     session.clear()
#     flash('you are now logged out','success')
#     return redirect(url_for('login'))


# @app.route('/dashboard')

# def dashboard():
#     #create cursor
#     cur = mysql.connection.cursor()

#     #get articles
#     result=cur.execute("SELECT * FROM articles")

#     articles = cur.fetchall()

#     if result > 0:
#         return render_template('dashboard.html', articles=articles)
#     else:
#         msg= 'No Articles Found'
#         return render_template('dashboard.html',msg=msg)
    
#     #close connection
#     cur.close()

# #Article form class
# class ArticleForm(Form):
#     title = StringField('Title',[validators.Length(min=1,max=200)])
#     body = TextAreaField('Body',[validators.Length(min=30)])
    
# #Add article
# @app.route('/add_article', methods=['GET','POST'])

# def add_article():
#     form = ArticleForm(request.form)
#     if request.method == 'POST' and form.validate():
#         title = form.title.data
#         body = form.body.data
#         test_clean_sentences = []
#         line = body
#         line = line.strip()
#         cleaned = clean(line)
#         cleaned = ' '.join(cleaned)
#         test_clean_sentences.append(cleaned)
#         Test = vectorizer.transform(test_clean_sentences)
#         groups = ["","world","politics","sci-fi","business"]
#         predicted_labels_knn = modelknn.predict(Test)
        
#         flash(groups[predicted_labels_knn])

#         return render_template('add_article.html', form=form)

#     return render_template('add_article.html', form=form)

# #edit article
# @app.route('/edit_article/<string:id>', methods=['GET','POST'])

# def edit_article(id):
#     #create cursor
#     cur = mysql.connection.cursor()

#     # get article by id
#     cur.execute("SELECT * from articles WHERE id= %s",[id])
    
#     article = cur.fetchone()

#     form = ArticleForm(request.form)
    
#     form.title.data = article['title']
#     form.body.data = article['body']

#     #cur.close()

#     if request.method == 'POST' and form.validate():
#         title = request.form['title']
#         body = request.form['body']

#         #create cursor
#         cur =mysql.connection.cursor()

#         #execute
#         cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title,body,id))

#         #commit to DB
#         mysql.connection.commit()

#         #close connection
#         cur.close()

#         #flash msg 
#         flash('Article Updated', 'success')

#         return redirect(url_for('dashboard'))

#     return render_template('edit_article.html', form=form)

# # delete article
# @app.route('/delete_article/<string:id>', methods=['POST'])

# def delete_article(id):
#     # create cursor
#     cur = mysql.connection.cursor()

#     #execute

#     cur.execute("DELETE FROM articles WHERE id = %s ",[id])

#     mysql.connection.commit()

#     cur.close()

#     flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':

    app.secret_key='secret123'
    app.run(debug=True)
    app.run(host='0.0.0.0',port=5005)
