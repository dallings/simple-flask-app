from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="postgres",
                        user="username",
                        password="password",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()

#login my
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            
            username = request.form.get('username')
            password = request.form.get('password')

            #Исключение на пустые поля
            if len(username)==0 or len(password)==0:
                return render_template('error.html')

            cursor.execute("SELECT * FROM reg_data WHERE login=%s AND password=%s", (str(username), str(password)))
            records = cursor.fetchall()

            #Исключение на отсутствие пользователя
            if len(records)==0:
                return render_template('error.html')

            return render_template('account.html', full_name=records[0][1], login='login: '+str(username), password='password: '+str(password))

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

#Register
@app.route('/registration/', methods=['POST', 'GET'])
def registration():

    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        
        #Исключение на пустые поля
        cursor.execute("SELECT * FROM reg_data WHERE login='"+str(login)+"';")

        if len(name)==0 or len(login)==0 or len(password)==0:
            return render_template('error.html')

        #Исключение на пользователя с таким же логином
        elif len(cursor.fetchall()):
            return render_template('error.html')
        else:
            cursor.execute('INSERT INTO reg_data (name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))

            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')

if __name__ == "__main__":
    app.run()