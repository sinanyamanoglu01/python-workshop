from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST']='call-mysql-db-server.cbanmzptkrzf.us-east-1.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER']='admin'
app.config['MYSQL_DATABASE_PASSWORD']='Clarusway_1'
app.config['MYSQL_DATABASE_DB']='clarusway'
app.config['MYSQL_DATABASE_PORT']=3306

mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor=connection.cursor()

drop_table = 'DROP TABLE IF EXISTS clarusway.users;'
users_table = """
CREATE TABLE clarusway.users (
  username varchar(50) NOT NULL,
  email varchar(50),
  PRIMARY KEY (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
data ="""
INSERT INTO clarusway.users 
VALUES 
    ("Anvarjon", "buddy@clarusway.com" ),
    ("Can D", "candido@clarusway.com"),
    ("Hakan", "charlie.byrd@clarusway.com"),
    ("Valerie", "charlie.byrd@clarusway.com"),
    ("Muhabbat", "charlie.byrd@clarusway.com"),
    ("Sinan", "sinany@clarusway.com");
"""
cursor.execute(drop_table)
cursor.execute(users_table)
cursor.execute(data)

def find_emails(keyword):
    query = f"""
    SELECT * FROM users WHERE username like '%{keyword}%';
    """
    cursor.execute(query)
    result=cursor.fetchall()
    user_emails = [(row[0], row[1]) for row in result]
    if not any(user_emails):
        user_emails = [('Not Found.', 'Not Found.')]
    return user_emails
@app.route('/', methods=['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_name=request.form['username']
        user_emails=find_emails(user_name)
        return render_template('emails.html', show_result=True, keyword=user_name, name_emails=user_emails)
    else:
        return render_template('emails.html', show_result=False)
if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)