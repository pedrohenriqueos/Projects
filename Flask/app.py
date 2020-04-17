from flask import Flask, redirect, url_for,render_template, request, session #, flash
from datetime import timedelta
import pymysql.cursors

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes = 5)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/create",methods = ["POST","GET"])
def create():
	if request.method == "POST":
		user = request.form["nm"]
		senha = request.form["pass"]
		confirm = request.form["pass2"]
		if confirm == senha:
			sql = "SELECT `nome` FROM `users` WHERE `nome`=%s"
			cursor.execute(sql,(user,))
			result = cursor.fetchone()
			if result!=None:
				#flash("Nome existe escolha outro!")
				return render_template("create.html")
			sql = "INSERT INTO `users` (`nome`,`senha`) VALUES(%s,%s)"
			cursor.execute(sql,(user,senha))
			connection.commit()
			return redirect(url_for("login"))
		else:
			return render_template("create.html")
	else:
		if "user" in session:
			#flash("Already Logged In!")
			return redirect(url_for("user"))
		return render_template("create.html")

@app.route("/login",methods = ["POST","GET"])
def login():
	if request.method == "POST":
		user = request.form["nm"]
		senha = request.form["pass"]
		sql = "SELECT `nome`,`senha` FROM `users` WHERE `nome`=%s"
		cursor.execute(sql,(user,))
		result = cursor.fetchone()
		if result==None:
			return redirect(url_for("login"))
		if result["nome"]==user and result["senha"]==senha:
			session.permanent = True
			session["user"] = user
			#flash("Login Sucessful!")
			return redirect(url_for("user"))
		return redirect(url_for("login"))
	else:
		if "user" in session:
			#flash("Already Logged In!")
			return redirect(url_for("user"))

		return render_template("login.html")

@app.route("/user",methods = ["POST","GET"]	)
def user():
	if "user" in session:
		user = session["user"]
		sql = "SELECT link_prob AS 'Problem', ansOJ AS 'ans', IFNULL(link_sub,'Sem submissao') AS 'Submissao', referencia AS 'Ref' FROM quest INNER JOIN users ON id_users=IDUSERS WHERE nome=%s"
		cursor.execute(sql,(user,))
		result = cursor.fetchall()
		size = list(range(len(result)))
		return render_template("pageuser.html",name = user,dados = result,sz = size)
	else:
		#flash("You are not logged in!")
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
		#flash("You have been logged out!","info")
		session.pop("user",None)
		return redirect(url_for("login"))

if __name__ == "__main__":
	connection = pymysql.connect(host='localhost',
                            user='root',
                            password='password',#the MySQL
                            db='db',#name the database
                            charset='utf8',
                            cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	app.run(host='localhost',debug=True)#localhost or ipMachine
