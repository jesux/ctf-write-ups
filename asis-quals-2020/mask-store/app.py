from flask import Flask,render_template,session,redirect,request,abort,url_for
from flask_csp.csp import csp_header
from flask_wtf.csrf import CSRFProtect
import mysql.connector as mysql
import uuid,secrets,hashlib,urllib.parse,random,os,validators,requests,base64,re,subprocess,math,time

ADMIN_ID =  os.getenv("admin_id")
ADMIN_USERNAME = os.getenv("admin_username")
DB_PW = os.getenv("db_pw")
DB_HOST = os.getenv("db_host")
DB_HOST = os.getenv("db_host")
SDB_PW = os.getenv("sandboxed_pw")
SESSION_PATH = os.getenv("session_path")


app = Flask(__name__,static_url_path="/static")
app.secret_key = os.getenv("session_secret")
CSRFProtect(app)

app.config["SESSION_COOKIE_SECURE"] = bool(int(os.getenv("cookies_secure")))
app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("cookies_same_site") 

db = mysql.connect(
    host = DB_HOST,
    user = "root",
    passwd = DB_PW,
    database = "maskstore"
)
db.autocommit = True
cursor = db.cursor(buffered=True)
cursor.execute("SET SESSION MAX_EXECUTION_TIME=%s" % os.getenv("mysql_timeout"))
db.commit()

sandboxed = mysql.connect(
    host = DB_HOST,
    user = "sandboxed",
    passwd = SDB_PW,
    database = "maskstore"
)
sandboxed.autocommit = True
sandboxedCursor = sandboxed.cursor(buffered=True)
sandboxedCursor.execute("SET SESSION MAX_EXECUTION_TIME=%s" % os.getenv("mysql_timeout"))
sandboxed.commit()

def chkip(ip):
    ip = hashlib.md5(ip.encode()).hexdigest()
    now = math.floor(time.time())
    filename = "./ip/%s" % ip

    if(os.path.isfile(filename)):
        rfile = open(filename,"r")
        lastrequest = int(rfile.read().strip())
        rfile.close()
    else:
        lastrequest = 0


    diff = now - lastrequest
    if(diff<60):
        return 60-diff
    else:
        wfile = open(filename,"w+")
        wfile.write(str(now))
        wfile.close()
        return "OK"

def getSessionVars():
    if("username" in session and "id" in session):
        loggedin = True
        userid = session["id"]
    else:
        userid = ""
        loggedin = False
    return loggedin,userid

def handlecsp(profile = False):
    nonce = base64.b64encode(''.join([str(random.randint(0, 9)) for i in range(20)]).encode()).decode()
    csp = """
    default-src 'none';
    connect-src 'none';
    style-src 'nonce-%s';
    script-src 'nonce-%s';
    base-uri 'none';
    form-action 'self';
    """ % (nonce,nonce)
    if(profile == True):
        csp += "img-src *;"
    csp = csp.replace('\n', '').replace("    ","")
    return {"Content-Security-Policy":csp},nonce

def is_authed(userid):
    q = "SELECT id FROM users where id = %s"
    cursor.execute(q,(userid,))
    users = cursor.fetchone()
    if(users != None):
        if(session["id"] == users[0]):
            return True
        else:
            abort(403)
    else:
        abort(404)
    return False
@app.after_request
def addref(r):
    r.headers["Referrer-Policy"] = "no-referrer"
    return r
@app.route("/",methods=["GET"])
def home():
    csp,nonce = handlecsp()
    loggedin,userid = getSessionVars()
    return render_template("home.html",loggedin=loggedin,userid=userid,nonce=nonce),200,csp

@app.route('/register',methods=["GET","POST"])
def register():
    csp,nonce = handlecsp()
    if("username" in session or "id" in session):
        return redirect(url_for("home",_scheme="https",_external=True))

    if(request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        if(username == None or username == "" or password == None or password == ""):
            return redirect(url_for("register",_scheme="https",_external=True))
        username = username.lower()
        q = "SELECT * FROM users where username = %s"
        cursor.execute(q,(username,))
        users = cursor.fetchall()
        if(len(users) != 0):
            return render_template("register.html",error="Username existed",loggedin=False,nonce=nonce),200,csp

        password = hashlib.md5(password.encode()).hexdigest()
        userid = str(uuid.uuid4())
        q = "INSERT INTO users (id,username,password,image,description,masksize) VALUES (%s,%s,%s,'https://i.pinimg.com/1200x/f4/4b/96/f44b968e1981f48a3cadba22351150c0.jpg','Maybe blue ones?','Unknown');"

        try:
            cursor.execute(q,(userid,username,password))
            db.commit()
        except:
            return render_template("register.html",error="Something bad happened",loggedin=False,nonce=nonce),200,csp

        return redirect(url_for("login",_scheme="https",_external=True))
    else:
        return render_template("register.html",error=None,loggedin=False,nonce=nonce),200,csp

@app.route('/edit/<userid>',methods=["GET","POST"])
def edit_user(userid):
    csp,nonce = handlecsp()

    if("username" not in session or "id" not in session):
        return redirect(url_for("home",_scheme="https",_external=True))

    if(is_authed(userid) != True):
        abort(403)
    
    if(request.method == "GET"):
        return render_template("edit.html",loggedin=True,userid=userid,nonce=nonce),200,csp
    elif(request.method == "POST"):
        imgurl = request.form.get("img")
        masksize = request.form.get("masksize")
        desc = request.form.get("description")

        if("ref" in imgurl.lower() or "ref" in desc.lower()):
            return render_template("edit.html",loggedin=True,userid=userid,error="I don't like REFs",nonce=nonce),200,csp
        if any(re.match(".*<.*(>|=..+)",inp) for inp in [imgurl,masksize,desc]):
            return render_template("edit.html",loggedin=True,userid=userid,error="/.*<.*(>|=..+)/ doesnt like your input",nonce=nonce),200,csp
        masksize = "Unknown" if masksize not in ["XL","L","M","SM"] else masksize
        q = "UPDATE users SET image=%s,description=%s,masksize=%s where id=%s"

        try:
            cursor.execute(q,(imgurl,desc,masksize,userid))
            db.commit()
        except:
            return render_template("edit.html",loggedin=True,userid=userid,nonce=nonce),200,csp

        return render_template("edit.html",loggedin=True,userid=userid,success="Updated successfully",nonce=nonce),200,csp
    else:
        abort(405)

@app.route('/login',methods=["GET","POST"])
def login():
    csp,nonce = handlecsp()

    if("username" in session or "id" in session):
        return redirect(url_for("home",_scheme="https",_external=True))

    if(request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")
        if(username == None or username == "" or password == None or password == ""):
            return redirect(url_for("login",_scheme="https",_external=True))
        username = username.lower()
        password = hashlib.md5(password.encode()).hexdigest()
        q = "SELECT * FROM users where username = %s and password = %s"
        cursor.execute(q,(username,password))
        user = cursor.fetchone()
        if(user != None):
            session["id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home",_scheme="https",_external=True))
        else:
            return render_template("login.html",error="Username/password is wrong",loggedin=False,nonce=nonce),200,csp
    else:
        return render_template("login.html",error=None,loggedin=False,nonce=nonce),200,csp
    
@app.route("/logout",methods=["GET"])
def logout():
    if("username" in session):
        del session["username"]
    if("id" in session):
        del session["id"]
    return redirect(url_for("home",_scheme="https",_external=True))

@app.route("/profile/<userid>",methods=["GET"])
def profile(userid):
    csp,nonce = handlecsp(True)
    q = "SELECT * FROM users where id = %s"
    cursor.execute(q,(userid,))
    user = cursor.fetchone()
    if(user != None):
        username = user[1]
        img =user[3]
        desc = user[4]
        ms = user[5]
        loggedin,userid = getSessionVars()
        return render_template("profile.html",username=username,img=img,desc=desc,masksize=ms,loggedin=loggedin,userid=userid,nonce=nonce),200,csp
    else:
        abort(404)

@app.route("/panel",methods=["GET","POST"])
def testpanel():
    csp,nonce = handlecsp()
    loggedin,userid = getSessionVars()
    if(request.method=="POST"):
        status = request.form.get("status")
        if(status == "late"):
            return render_template("panel.html",userid=userid,loggedin=loggedin,message="Your order has problem, we are working on it.",nonce=nonce),200,csp
        elif(status == "shipped"):
            return render_template("panel.html",userid=userid,loggedin=loggedin,message="Your order has been arrived",nonce=nonce),200,csp
        else:
            return render_template("panel.html",userid=userid,loggedin=loggedin,error="Your order has fatal problem",nonce=nonce),200,csp


    orderid = request.args.get("orderid")
    if(orderid == None):
        return render_template("panel.html",loggedin=loggedin,userid=userid,nonce=nonce),200,csp
    else:
        q = "SELECT * FROM maskstore.orders where id = '%s' " % orderid 
        
        qlower = q.lower()        
        blacklist = ["information_schema","users","processlist","load","insert","into","mysql","innodb","benchmark","sleep","md5","sha","password"]
        if(any(word in qlower for word in blacklist) ):
            return render_template("panel.html",loggedin=loggedin,userid=userid,error="WHAT????",nonce=nonce,querySuccess=False),400,csp
        
        if("username" in session and "id" in session and session["username"] == ADMIN_USERNAME and session["id"] == ADMIN_ID):
            cur = cursor
        else:
            cur = sandboxedCursor
        try:
            cur.execute(q)
            results = cur.fetchone()
        except:
            return render_template("panel.html",loggedin=loggedin,userid=userid,error="Something bad happened",nonce=nonce,querySuccess=False),200,csp
        
        if(results == None or not isinstance(results[1], str)):
            return render_template("panel.html",loggedin=loggedin,userid=userid,error="Could not find order",nonce=nonce,querySuccess=False),200,csp

        rlower = results[1].lower()        
        blacklist = ["meta","http","src","rel","frame","link","embed","object"]
        if(any(word in rlower for word in blacklist) ):
            return render_template("panel.html",loggedin=loggedin,userid=userid,error="WHAT????",nonce=nonce,querySuccess=False),400,csp
        
        return render_template("order.html",loggedin=loggedin,userid=userid,orderid=results[0],orderhtml=results[1],nonce=nonce,querySuccess=True),200,csp

@app.route("/report",methods=["GET","POST"])
def report():
    csp,nonce = handlecsp()
    loggedin,userid = getSessionVars()
    if(request.method == "GET"):
        return render_template("report.html",error=None,message=None,loggedin=loggedin,userid=userid,nonce=nonce),200,csp
    else:
        ck = request.headers.get('x-i-want-the-real-ip')
        ck = chkip(ck)
        if(ck != "OK"):
            return render_template("./report.html",error="Too fast, Please wait for %s seconds" % ck,message=None,loggedin=loggedin,nonce=nonce),200,csp
        url = request.form.get("url")
        if(url != None):
            valid = validators.url(url) and url[0:4] == "http"
            if(valid == True):
                subprocess.Popen(["python3","bot.py",base64.b64encode(url.encode()).decode()])
                return render_template("report.html",error=None,message="Admin will visit your URL",loggedin=loggedin,userid=userid,nonce=nonce),200,csp
            else:
                return render_template("report.html",error="URL is not valid",message=None,loggedin=loggedin,userid=userid,nonce=nonce),200,csp
        else:
            return render_template("report.html",loggedin=loggedin,userid=userid,nonce=nonce),200,csp

@app.route(SESSION_PATH,methods=["GET"])
def admin_session():
    session["id"] = ADMIN_ID
    session["username"] = ADMIN_USERNAME
    return "OK"
    
