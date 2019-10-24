import os
import subprocess
from flask import Flask, abort, request, jsonify, g, url_for, redirect, escape, render_template, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, widgets, FileField
#from itsdangerous import (TimedJSONWebSignatureSerializer
#                          as Serializer, BadSignature, SignatureExpired)
              
app = Flask(__name__)
SECRET_KEY = b'?\x03?w*\xd2\x84\xea\xc3\xc1\x8c\xe7\x80\x83\x9d\x8c=\xb1\x17\xe3Z\xf4|C'
credential_dictionary = {}
current_session = None

class RegistrationForm(Form):
    uname = StringField('Username', [validators.Length(min=4, max=25)], id='uname')
    pword = PasswordField('New Password', [validators.DataRequired()], id='pword')
    #phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()], id='2fa')
    phone = StringField('Phone Number', [validators.DataRequired()], id='2fa')
    #phone = IntegerField('Phone', [validators.NumberRange(min=0, max=10), validators.DataRequired()], id='2fa', widget = widgets.Input(input_type="tel"))
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class LoginForm(Form):
    uname = StringField('Username', [validators.Length(min=4, max=25)], id='uname')
    pword = PasswordField('New Password', [validators.DataRequired()], id='pword')
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()], id='2fa')
    
class UploadForm(Form):
    inputtext = StringField('Text', [validators.DataRequired()], id='inputtext')
    
def reformat_phone(form, field):
    field.data = field.data.replace('-', '')
    return True

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        #session['username'] = request.form['username']
        #return redirect(url_for('index'))
        #username = request.form.get('uname')
        #password = request.form.get('pword')
        #phone = request.form.get('2fa')
        username = form.uname.data
        password = form.pword.data
        phone = form.phone.data
        print (username, password, phone)
        if username in credential_dictionary:
            if password == credential_dictionary[username][0]:
                if phone == credential_dictionary[username][1]:
                    print ("Login successful")
                    result = "success"
                    return render_template('spell_check.html', form=form, result = result, credential=[username,password,phone]) 
                else :
                    print ("Login failed - two-factor")
                    result = "two-factor failed"
                    return render_template('login.html', form=form, result = result) 
            else:
                print ("Login failed - incorrect password")
                result = "Incorrect"
                return render_template('login.html', form=form, result = result) 
        else:
            print ("Login failed - incorrect username")
            result = "Incorrect"
            return render_template('login.html', form=form, result = result) 
    else:
        result = "Incorrect"
        return render_template('login.html', form=form, result = result) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        #user = User(form.uname.data, form.pword.data,
                    #form.phone.data)
        if form.uname.data not in credential_dictionary:
            credential_dictionary[form.uname.data] = [form.pword.data, form.phone.data]
            #flash('Thanks for registering')
            print (credential_dictionary[form.uname.data][0], credential_dictionary[form.uname.data][1])
            success = 'success'
            return render_template('register.html', form=form, success = success) 
        else:
            success = 'failure'
            return render_template('register.html', form=form, success = success) 
        #return redirect(url_for('login'))
        success = 'failure'
        return render_template('register.html', form=form, success = success)
    return render_template('register.html', form=form) 
 
#@app.route('/success')
#def success():
#    return '''
#    <p id="success">Registered successfully</p>
#    '''
 
@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    #upload file
    #POST check file
    #if result != 'success':
    #    return render_template('login.html', form=form, result=result)
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
        inputtext = form.inputtext.data   
        with open("test.txt","w+") as fo:
            fo.write("%s" % inputtext)
        proc = subprocess.run(["./a.out", "test.txt", "wordlist.txt"], capture_output = True, universal_newlines = True)
        misspelled = proc.stdout
        return render_template('spell_check.html', form=form, misspelled=misspelled, textout=inputtext)
    return render_template('spell_check.html', form=form)
    
 
@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, host='127.0.0.1', port="5001")