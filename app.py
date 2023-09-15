from flask import Flask, request, render_template, session
import ibm_db

app = Flask(__name__)
app.secret_key = "_ab+d=5"
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32459;UID=wht62776;PWD=co8PwsATacwX8hJl; SECURITY=SSL;SSLCERTIFICATE=DigiCertGlobalRootCA.crt",'','')
print(conn)
print(ibm_db.active(conn))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global uname
        uname = request.form['username']
        pword = request.form['password']
        print(uname, pword)
        sql = "SELECT * FROM REGISTER_GITAM WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.bind_param(stmt,2,pword)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            session['username'] = uname
            session['emailid'] = out['EMAILID']
            
            if out['ROLE'] == 0:
                return render_template("adminprofile.html",username = uname, emailid = out['EMAILID'] )
            elif out['ROLE'] == 1:
                return render_template("studentprofile.html",username = uname, emailid = out['EMAILID'])
            else: 
                return render_template("facultyprofile.html",username = uname, emailid = out['EMAILID'])
        else: 
            msg = "Invalid Credentials"
            return render_template("login.html",message1= msg)
    return render_template("login.html")

@app.route("/register", methods=['GET', 'POST'])
def regsiter():
    if request.method == "POST":
        uname = request.form['name']
        email = request.form['email']
        uname = request.form['uname']
        pword = request.form['password']
        role = request.form['role']
        print(uname,email,pword,role)
        sql = "SELECT * FROM REGISTER_GITAM WHERE USERNAME=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, uname)
        ibm_db.execute(stmt)
        out = ibm_db.fetch_assoc(stmt)
        print(out)
        if out != False:
            msg = "Already Registered"
            return render_template("register.html",msg = msg)
        else:
            sql = "INSERT INTO REGISTER_KLU VALUES(?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, uname)
            ibm_db.bind_param(stmt, 2,email)
            ibm_db.bind_param(stmt, 3, pword)
            ibm_db.bind_param(stmt, 4, role)
            ibm_db.execute(stmt)
            msg = "Registered"
            return render_template("register.html", msg =msg)

    return render_template("register.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
