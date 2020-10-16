                                    #################################
                                    ### PROJECT RISK ASSESSMENT   ###
                                    ### CLIENTS : CITY AND POLICE ###
                                    ### THE GOAL OF THE APP IS TO ###
                                    ### EVALUATE THE RISK OF A    ###
                                    ### PROJECT BEFORE TO DO IT   ###
                                    ### AND TO COMPARE IT WITH    ###
                                    ### OTHERS                    ###
                                    #################################

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
#import matplotlib.pyplot as plt

from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///BDMisu.db")


@app.route("/general", methods=["GET", "POST"])
@login_required
def general():
    if request.method == "POST":
        # Query database for id
        rows = db.execute("SELECT analysis_id FROM General")
        if len(rows) != 0:
            last_id = (rows[-1]["analysis_id"])
            analysis_id = last_id + 1
        else:
            analysis_id = 1
        db.execute("INSERT INTO General (analysis_id, email, analysis_date, analysis_responsible, project_evaluated, team_members, other_unity, collaborative_unity, ref_unity, confirmation, user_id) VALUES(:analysis_id, :email, :date, :resp, :project, :members, :otherUnity, :collabo, :ref, :confirmation, :user_id)", analysis_id=analysis_id, email=request.form.get("email"), date=request.form.get("formDate"), resp=request.form.get("responsible"), project=request.form.get("projectEvaluated"), members=request.form.get("team"), otherUnity=request.form.get("otherUnity"), collabo=request.form.get("collaborativeUnity"), ref=request.form.get("refUnity"), confirmation=request.form.get("confirmation"), user_id = session["user_id"])
        confirmation = db.execute("SELECT confirmation FROM General WHERE user_id = :user_id",
                          user_id = session["user_id"])
        print(confirmation)
        
        return render_template("riskAnalysis.html")

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("general.html")

@app.route("/riskAnalysis", methods=["GET", "POST"])
@login_required
def riskAnalysis():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # Query database for id
        rows = db.execute("SELECT analysis_id FROM General")
        
        analysis_id = (rows[-1]["analysis_id"])
            
        db.execute("INSERT INTO riskAnalysis (analysis_id, legal_dispo, new_procedures, dang_subs, earth_move, m_roads, m_dang_subs, m_nuis, m_ecolo, publics_serv_compromised, pers_concentration, user_id) VALUES(:analysis_id, :legalDispo, :newProcedures, :dangSubs, :earthMove, :mRoads, :mDangSubs, :mNuis, :mEcolo, :publicsServCompromised, :concentration, :user_id)", analysis_id = analysis_id, legalDispo = request.form['specialPermit'], newProcedures = request.form['newProcedures'], dangSubs = request.form['subsDang'], earthMove = request.form['earthMouv'], mRoads = request.form['800mRaiway'], mDangSubs = request.form['distSubsDang'], mNuis = request.form['800mNuis'], mEcolo = request.form['500mEcolo'], publicsServCompromised = request.form['publicsServCompromised'], concentration = request.form['concentration'], user_id = session["user_id"])
        
        return render_template("index.html")

        # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("riskAnalysis.html")
        
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("the username already exists", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)        
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("the password and the confirmed password are different", 400)
        hash = generate_password_hash(request.form.get("password"))
        new_user_id = db.execute("INSERT INTO users (username, hash, email) VALUES (:username, :hash, :email)",
        username=request.form.get("username"), hash=hash, email=request.form.get("email"))
    
        # Remember the user log in
        session["user_id"] = new_user_id
        
        # Registered message
        flash("Registered!")

        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
        
 
@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change password of the user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("oldPassword"):
            return apology("must provide password", 400)
        if not request.form.get("newPassword"):
            return apology("must provide password", 400)        
        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)
        if request.form.get("newPassword") != request.form.get("confirmation"):
            return apology("the new password and the confirmed password are different", 400)
        
        # Verify Old password
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])
        oldHash = rows[0]["hash"]
        oldPassword = request.form.get("oldPassword")
        if not check_password_hash(oldHash, oldPassword):
            return apology("the old password is wrong", 400)
            
        # register new password and hash it
        hash = generate_password_hash(request.form.get("newPassword"))
        new_user_id = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)
        
        # Registered message
        flash("Password change!")

        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Take the username of the user
        rows = db.execute("SELECT username FROM users WHERE id = :user_id", user_id=session["user_id"])
        username = rows[0]["username"]
        
        return render_template("changePassword.html", username=username)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Query database for data for user_id
        rows = db.execute("SELECT * FROM riskAnalysis WHERE user_id = :user_id", user_id=session["user_id"])
        data = []
        # Query database for project --- passer par analysis_id et project_name
        
        for row in rows:
            count = 0
            analysis_id = row["analysis_id"]
            projects = db.execute("SELECT project_evaluated FROM General WHERE analysis_id = :analysis_id", analysis_id = analysis_id)
            project = projects[0]["project_evaluated"]
            for value in row.values():
                if value == "yes":
                    count += 1
            pourcent = round(count/12, 2) * 100
            id_data = (project, pourcent)
            data.append(id_data)
            print(data)
        return render_template("results.html", data=data)
    