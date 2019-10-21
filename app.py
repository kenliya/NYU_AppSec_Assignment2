import os
from flask import Flask, abort, request, jsonify, g, url_for, redirect, escape, render_template, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators, IntegerField, widgets, FileField
#from itsdangerous import (TimedJSONWebSignatureSerializer
#                          as Serializer, BadSignature, SignatureExpired)
                          
app = Flask(__name__)
SECRET_KEY = b'?\x03?w*\xd2\x84\xea\xc3\xc1\x8c\xe7\x80\x83\x9d\x8c=\xb1\x17\xe3Z\xf4|C'
credential_dictionary = {}

class RegistrationForm(Form):
    uname = StringField('Username', [validators.Length(min=4, max=25)], id='uname')
    pword = PasswordField('New Password', [validators.DataRequired()], id='pword')
    phone = StringField('Phone Number', [validators.Length(min=10, max=10), validators.DataRequired()], id='2fa')
    #phone = IntegerField('Phone', [validators.NumberRange(min=0, max=10), validators.DataRequired()], id='2fa', widget = widgets.Input(input_type="tel"))
    #confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class UploadForm(Form):
    file = FileField()
    
def reformat_phone(form, field):
    field.data = field.data.replace('-', '')
    return True

@app.route('/login', methods = ['GET', 'POST'])
def login():
    success = " "
    if request.method == 'POST':
        #session['username'] = request.form['username']
        #return redirect(url_for('index'))
        username = request.form.get('uname')
        password = request.form.get('pword')
        phone = request.form.get('2fa')
        print (username, password, phone)
        if username in credential_dictionary:
            if password == credential_dictionary[username][0]:
                if phone == credential_dictionary[username][1]:
                    print ("Login successful")
                    result = "success"
                    return '''
                        <form action = "" method = "post">
                            <li id = 'result' name='result' type='text'>{{result}}</li>
                        </form>
                    '''
                else :
                    print ("Login failed")
                    result = "two-factor failure"
                    return
                    '''
                        <form action = "" method = "post">
                            <li id = 'result' name='result' type='text'>{{result}}</li>
                        </form>
                    '''
            else:
                print ("Login failed")
                result = "Incorrect"
                return
                '''
                    <form action = "" method = "post">
                        <li id = 'result' name='result' type='text'>{{result}}</li>
                    </form>
                '''
   # if result=="success":
   #     return '''
   #     <h1 id='success'>
   #     <form action = "" method = "post">
   #         <p>UserName<input id = uname type = text name = uname></p>
   #         <p>Password<input id = pword type = password name = pword></p>
   #         <p>Phone<input id = 2fa type = text name = 2fa></p>
   #         <p><input type = submit value = Login/></p>
   #     </form>
        
    #    '''
    #else:
    return '''
    <form action = "" method = "post">
        <p>UserName<input id = uname type = text name = uname></p>
        <p>Password<input id = pword type = password name = pword></p>
        <p>Phone<input id = 2fa type = text name = 2fa></p>
        <p><input type = submit value = Login/></p>
    </form>
    
    '''

#@app.route('/register', methods = ['GET','POST'])
#def register():
#    if request.method == 'POST':
#        username = request.form.get("uname")
#        password = request.form.get("pword")
#        phone = request.form.get("phone")
#        #print("username: ", username, "\n")
#        #print("password: ", password, "\n")
#        #with open("test.txt","w+") as fo:
#        #    fo.write("username: %s\r\n" % username)
#        #    fo.write("password: %s\r\n" % password)    
#    return '''
#   <form method = "POST">
#      <p>UserName<input id = uname type = text name = uname></p>
#      <p>Password<input id = pword type = password name = pword></p>
#      <p>Password<input id = pword type = password name = pword></p>
#      <p><input type = submit value = Login></p>
#   </form>
#    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    success = None
    if request.method == 'POST' and form.validate():
        #user = User(form.uname.data, form.pword.data,
                    #form.phone.data)
        #db_session.add(user)
        credential_dictionary[form.uname.data] = [form.pword.data, form.phone.data]
        flash('Thanks for registering')
        print (credential_dictionary[form.uname.data][0], credential_dictionary[form.uname.data][1])
        success = 'success'
        return redirect(url_for('register', success=success))
        #return redirect(url_for('login'))
    return render_template('register.html', form=form, success = success) 
 
@app.route('/success')
def success():
    return '''
    <p id="success">Registered successfully</p>
    '''
 
@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    #upload file
    #POST check file
    form = UploadForm(request.form)
    if request.method == 'POST' and form.validate():
        #run spell_check C code
        #file = 
        return 
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