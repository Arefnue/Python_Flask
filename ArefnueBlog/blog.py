from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt


#Kullanici kayit formu
class RegisterForm(Form):
    
    name = StringField("Adınız:",validators=[validators.length(min= 4,max=20)])
    username = StringField("Kullanıcı adınız:",validators=[validators.length(min=4,max=30,message="Kullanıcı adınız fazla uzun.")])
    email = StringField("E-posta adresiniz:",validators=[validators.email("Lütfen geçerli bir e-posta adresi giriniz.")])
    password = PasswordField("Parolanız:",validators=[
        validators.DataRequired("Lütfen parolanizi giriniz."),
        validators.EqualTo(fieldname="confirmPassword",message="Parolanız uyuşmuyor...")
    ])
    confirmPassword = PasswordField("Parolanizi doğrulayiniz:")

#Kullanici giriş formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı:")    
    password = PasswordField("Parola:")

app = Flask(__name__)

#Secret Key
app.secret_key = "GizliAnahtar"

#App Config
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "arefnueblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#Ana Sayfa
@app.route("/")
def index():

    return render_template("index.html")
#Hakkimizda
@app.route("/about")
def about():

    return render_template("about.html")


#Kayıt Ol
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,username,email,password))

        mysql.connection.commit()

        cursor.close()
        flash("Tebrikler! Başarıyla kayıt oldunuz...", category = "success")

        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)

#Giriş Yap
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm(request.form)

    return render_template("login.html",form = form)

if __name__ == "__main__":

    app.run(debug=True)
