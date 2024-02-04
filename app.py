import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///myforest.db")


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show Index page """
    user_id = session["user_id"]
    folders = db.execute(
        "SELECT foldername FROM achievements WHERE user_id = ? GROUP BY foldername",
        user_id,
    )
    return render_template("index.html", folders=folders)


@app.route("/openfolder/<string:foldername>", methods=["GET", "POST"])
@login_required
def openfolder(foldername):
    """Display and change folder content"""
    user_id = session["user_id"]

    # query sentences with requested foldername and the remaining foldernames for the select menu
    sentences = db.execute(
        "SELECT sentence FROM achievements WHERE user_id = ? AND foldername = ?",
        user_id,
        foldername,
    )
    folders = db.execute(
        "SELECT foldername FROM achievements WHERE user_id = ? AND NOT foldername = ? GROUP BY foldername",
        user_id,
        foldername,
    )

    if request.method == "POST":
        error = None
        folder = request.form.get("folder")
        newfolder = request.form.get("newfolder")
        sentences_chosen = request.form.getlist("sentences_chosen")

        # if fields are being left blank
        if not sentences_chosen:
            error = "Please select sentence(s) to move"

        elif not folder and not newfolder:
            error = "Please select or create new folder"

        # if two different folders are chosen
        elif folder and newfolder:
            error = "Please decide on a folder"

        # if foldername is too long
        elif len(newfolder) > 40:
            error = "Max length of foldername: 40 characters"

        # if foldername exists already
        folders_existing = db.execute(
            "SELECT foldername FROM achievements WHERE user_id = ? AND foldername = ?",
            user_id,
            newfolder,
        )
        if len(folders_existing) != 0:
            error = "There is already a folder with this name. You can move sentences there!"

        if error != None:
            flash(error)
            return render_template(
                "openfolder.html",
                foldername=foldername,
                sentences=sentences,
                folders=folders,
            )

        else:
            # input based decision on value of foldername
            if folder:
                name = folder
            elif newfolder:
                name = newfolder

            # update foldername for every selected achievement
            for sentence in sentences_chosen:
                db.execute(
                    "UPDATE achievements SET foldername = ? WHERE user_id = ? AND sentence = ?",
                    name,
                    user_id,
                    sentence,
                )

                # update achievements in folder
                sentences_new = db.execute(
                    "SELECT sentence FROM achievements WHERE user_id = ? AND foldername = ?",
                    user_id,
                    foldername,
                )

                # update folders in select menu
                folders_new = db.execute(
                    "SELECT foldername FROM achievements WHERE user_id = ? GROUP BY foldername",
                    user_id,
                )

                # if folder is empty, return to index
                if not sentences_new:
                    return render_template("index.html", folders=folders_new)

            return render_template(
                "openfolder.html",
                foldername=foldername,
                sentences=sentences_new,
                folders=folders_new,
            )

    return render_template(
        "openfolder.html", foldername=foldername, sentences=sentences, folders=folders
    )


@app.route("/rename/<string:foldername>", methods=["POST"])
@login_required
def rename(foldername):
    """Rename folder"""
    user_id = session["user_id"]
    error = None

    # query sentences with requested foldername and the remaining foldernames for the select menu
    sentences = db.execute(
        "SELECT sentence FROM achievements WHERE user_id = ? AND foldername = ?",
        user_id,
        foldername,
    )
    folders = db.execute(
        "SELECT foldername FROM achievements WHERE user_id = ? AND NOT foldername = ? GROUP BY foldername",
        user_id,
        foldername,
    )
    newname = request.form.get("newname")

    # if fields are being left blank
    if not newname or newname == foldername:
        return render_template(
            "openfolder.html",
            foldername=foldername,
            sentences=sentences,
            folders=folders,
        )

    # if foldername is too long
    elif len(newname) > 40:
        error = "Max length of foldername: 40 characters"

    # if foldername exists already
    folders_existing = db.execute(
        "SELECT foldername FROM achievements WHERE user_id = ? AND foldername = ?",
        user_id,
        newname,
    )
    if len(folders_existing) != 0:
        error = (
            "There is already a folder with this name. You can move sentences there!"
        )

    if error != None:
        flash(error)
        return render_template(
            "openfolder.html",
            foldername=foldername,
            sentences=sentences,
            folders=folders,
        )
    else:
        # update foldername
        db.execute(
            "UPDATE achievements SET foldername = ? WHERE user_id = ? AND foldername = ?",
            newname,
            user_id,
            foldername,
        )
        return render_template(
            "openfolder.html",
            foldername=newname,
            sentences=sentences,
            folders=folders,
        )


@app.route("/achievements")
@login_required
def achievements():
    """Display user's achievements"""
    user_id = session["user_id"]
    achievements = db.execute(
        "SELECT * FROM achievements WHERE user_id = ? ORDER BY id DESC", user_id
    )
    return render_template("achievements.html", achievements=achievements)


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        error = None
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        question = request.form.get("question")
        answer = request.form.get("answer")

        # if fields are being left blank
        if not username:
            error = "Please choose a username"
        elif not password or not confirmation:
            error = "Please choose AND confirm password"
        elif not question:
            error = "Please choose a security question"
        elif not answer:
            error = "Please answer security question"

        # if passwords do not match
        if password != confirmation:
            error = "Passwords do not match"

        # if username is taken
        usernames = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )
        if len(usernames) != 0:
            error = "Username exists already"

        if error != None:
            flash(error)
            return render_template("register.html")
        else:
            # hash password and answer
            password_hash = generate_password_hash(password)
            answer_hash = generate_password_hash(answer)

            # create account and redirect to login page
            db.execute(
                "INSERT INTO users (username, hash, question, answer) VALUES (?, ?, ?, ?)",
                username,
                password_hash,
                question,
                answer_hash,
            )
            return redirect("/")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in user"""
    # Logout any user
    session.clear()

    if request.method == "POST":
        error = None

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            error = "Password and/or username not correct"
        if error != None:
            flash(error)
            return render_template("login.html")
        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")
    return render_template("login.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Let registered user change their password"""
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0][
        "username"
    ]

    if request.method == "POST":
        error = None
        oldpassword = request.form.get("oldpassword")
        newpassword = request.form.get("newpassword")
        newconfirmation = request.form.get("newconfirmation")

        # fields being left blank
        if not oldpassword:
            error = "Please provide old password"
        elif not newpassword or not newconfirmation:
            error = "Please choose AND confirm new password"

        # new passwords do not match
        elif newpassword != newconfirmation:
            error = "New passwords do not match"

        # if old/current password is not correct
        previous_password = db.execute(
            "SELECT hash FROM users WHERE username = ?", username
        )
        if not check_password_hash(previous_password[0]["hash"], oldpassword):
            error = "Old password is not correct"

        if error != None:
            flash(error)
            return render_template("changepassword.html", username=username)
        else:
            # hash password
            hash_new = generate_password_hash(newpassword)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hash_new, user_id)

            # log out and redirect to login page
            session.clear()
            return redirect("/")
    return render_template("changepassword.html", username=username)


@app.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    """Prompt user who forgot password for username"""
    if request.method == "POST":
        username = request.form.get("username")

        # check if username exists
        usernames = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )
        if not username or len(usernames) != 1:
            flash("Username not found")
            return render_template("forgotpassword.html")
        else:
            # query the user's security question and send them to the answering form
            question = db.execute(
                "SELECT question FROM users WHERE username = ?", username
            )[0]["question"]
            return render_template(
                "question.html", username=username, question=question
            )
    return render_template("forgotpassword.html")


@app.route("/question/<username>", methods=["GET", "POST"])
def question(username):
    """Get answer of security question from user"""
    question = db.execute("SELECT question FROM users WHERE username = ?", username)[0][
        "question"
    ]

    if request.method == "POST":
        answer = request.form.get("answer")
        correct_answer = db.execute(
            "SELECT answer FROM users WHERE username = ?", username
        )

        # if answer is not correct
        if not answer or not check_password_hash(correct_answer[0]["answer"], answer):
            flash("Incorrect answer")
            return render_template(
                "question.html", username=username, question=question
            )

        # if answer is correct, direct user to password change form
        return render_template("newpassword.html", username=username)
    return render_template("question.html", question=question)


@app.route("/newpassword/<username>", methods=["GET", "POST"])
def newpassword(username):
    """Let user change their password"""
    if request.method == "POST":
        newpassword = request.form.get("newpassword")
        newconfirmation = request.form.get("newconfirmation")

        # fields being left blank or new passwords do not match
        if not newpassword or not newconfirmation or newpassword != newconfirmation:
            flash("New passwords do not match")
            return render_template("newpassword.html", username=username)

        # create new password hash
        hash_new = generate_password_hash(newpassword)
        db.execute("UPDATE users SET hash = ? WHERE username = ?", hash_new, username)
        return redirect("/")
    return render_template("newpassword.html")


@app.route("/newachievement", methods=["GET", "POST"])
@login_required
def newachievement():
    """Write down achievements and store them in folders"""
    user_id = session["user_id"]

    # foldernames for select menu
    foldernames = db.execute(
        "SELECT foldername FROM achievements WHERE user_id = ? GROUP BY foldername",
        user_id,
    )

    if request.method == "POST":
        error = None
        folder = request.form.get("folder")
        newfolder = request.form.get("newfolder")
        newachievement = request.form.get("newachievement")

        # if fields being left blank
        if not folder and not newfolder:
            error = "Please choose or create a folder"
        elif not newachievement:
            error = "Please write an achievement"

        # if two different folders were chosen
        elif folder and newfolder:
            error = "Please decide on a folder"

        # if foldername is too long
        elif len(newfolder) > 40:
            error = "Max length of foldername: 40 characters"

        # if foldername already exists
        folders_existing = db.execute(
            "SELECT foldername FROM achievements WHERE user_id = ? AND foldername = ?",
            user_id,
            newfolder,
        )
        if len(folders_existing) != 0:
            error = "There is already a folder with this name."

        if error != None:
            flash(error)
            return render_template("newachievement.html", foldernames=foldernames)
        else:
            # input based decision on value of foldername
            if folder:
                foldername = folder
            elif newfolder:
                foldername = newfolder

            # update rewards and counters
            reward = count_reward(user_id)

            db.execute(
                "INSERT INTO achievements (user_id, foldername, sentence, reward) VALUES (?, ?, ?, ?)",
                user_id,
                foldername,
                newachievement,
                reward,
            )

            # update foldernames for select menu
            new_foldernames = db.execute(
                "SELECT foldername FROM achievements WHERE user_id = ? GROUP BY foldername",
                user_id,
            )
            return render_template("newachievement.html", foldernames=new_foldernames)
    return render_template("newachievement.html", foldernames=foldernames)


def count_reward(user_id):
    """Define reward and update counter for forest"""
    counters = db.execute("SELECT trees, birds, foxes FROM users WHERE id = ?", user_id)
    trees = counters[0]["trees"]
    birds = counters[0]["birds"]
    foxes = counters[0]["foxes"]

    if trees == 9:
        # make every hundredth reward a fox
        if birds == 9:
            reward = "fox"
            foxes += 1
            birds = 0
            trees = 0
        else:
            # make every tenth reward a bird
            reward = "bird"
            birds += 1
            trees = 0
    else:
        # make all other rewards trees
        reward = "tree"
        trees += 1

    db.execute(
        "UPDATE users SET trees = ?, birds = ?, foxes = ? WHERE id = ?",
        trees,
        birds,
        foxes,
        user_id,
    )
    return reward


@app.route("/forest")
@login_required
def forest():
    """Display forest"""
    user_id = session["user_id"]
    rewards = db.execute("SELECT reward FROM achievements WHERE user_id = ?", user_id)
    return render_template("forest.html", rewards=rewards)


@app.route("/edit/<string:sentence>", methods=["GET", "POST"])
@login_required
def edit(sentence):
    """Edit achievements"""
    user_id = session["user_id"]
    id = db.execute(
        "SELECT id FROM achievements WHERE user_id = ? AND sentence = ?",
        user_id,
        sentence,
    )[0]["id"]
    if request.method == "POST":
        edit = request.form.get("edit")

        # if field is being left blank
        if not edit:
            flash("Please provide an achievement")
            return render_template("edit.html", sentence=sentence)

        # edit achievement
        db.execute(
            "UPDATE achievements SET sentence = ? WHERE user_id = ? AND id = ? AND sentence = ?",
            edit,
            user_id,
            id,
            sentence,
        )

        # update edited achievements and direct to my achievements
        achievements = db.execute(
            "SELECT * FROM achievements WHERE user_id = ? ORDER BY id DESC", user_id
        )
        return render_template("achievements.html", achievements=achievements)
    return render_template("edit.html", sentence=sentence)
