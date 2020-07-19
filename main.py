from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/SignUp")
def signUp():
    return render_template("signUp.html")

@app.route("/Login")
def login():
    return render_template("login.html")

@app.route("/Dashboard")
def dash():
    return render_template("dash.html")

@app.route("/Reading_Library")
def library():
    return render_template("library.html")

@app.route("/Timeline")
def timeline():
    return render_template("timeline.html")

@app.route("/Item_Profile")
def profile():
    return render_template("profile.html")

@app.route("/Add_Entry")
def entry():
    return render_template("entry.html")

@app.route("/Settings")
def settings():
    return render_template("settings.html")

@app.route("/Help")
def help():
    return render_template("help.html")

@app.route("/Link_Account")
def link():
    return render_template("link.html")


if __name__=='__main__':
    app.run(debug=True)