import os,sqlite3
from flask import Flask, redirect, url_for, session, request, render_template,jsonify
from requests_oauthlib import OAuth1Session
from src.Profile import Profile
from src.Twitter import Twitter
from src.Agent import Agent
from src.Task import Task
from src.Action import Action
from src.Post import Post
from time import sleep
import threading
from werkzeug.security import check_password_hash



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure session storage

API_KEY = ""
API_SECRET = ""


ACCESS_TOKEN =""
ACCESS_TOKEN_SECRET = ""
CALLBACK_URL = "http://127.0.0.1:5000/callback"





REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
TWEET_URL = "https://api.twitter.com/2/tweets"



@app.route("/")
def index():
    db = sqlite3.connect('database.db')
    twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    agent = Agent(db,twitter)
    is_logged = False
    status = "unverified"
    try:
        is_logged = session["is_logged"]
        status = agent.is_verified(session["screen_name"])
    except:
        pass
    return render_template("index.html",is_logged=is_logged,status=status)
@app.route("/login")
def login():
    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri=CALLBACK_URL)
    fetch_response = oauth.fetch_request_token(REQUEST_TOKEN_URL)

    session["resource_owner_key"] = fetch_response.get("oauth_token")
    session["resource_owner_secret"] = fetch_response.get("oauth_token_secret")

    auth_url = oauth.authorization_url(AUTHORIZATION_URL)
    return redirect(auth_url)

@app.route("/admin", methods = ['GET','POST'])
def admin():
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("error.html", top=403, bottom="must provide old password",url=request.path),403 

        elif not request.form.get("password"):
            return render_template("error.html", top=403, bottom="must provide the new password",url=request.path),403 
        db = sqlite3.connect('database.db')
        password = request.form.get('password').strip()
        username = request.form.get('username').strip()
        cursor = db.execute("SELECT * FROM ADMINS WHERE username = (?) ",(username,))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0][1],password):
            db.close()
            return render_template("error.html", top=403, bottom="wrong password",url=request.path),403
        db.close()
        session["admin"] = True
        return redirect(url_for("panel"))
    elif request.method == "GET":
        try :
            is_logged = session["admin"]
        except:
            is_logged = False
        if is_logged  : 
            return redirect(url_for("panel"))
        else:
            return render_template("admin.html")
    else:
        return render_template("admin.html")
    
@app.route("/panel",methods = ['GET'])
def panel():
    try:
        is_logged = session["admin"]
    except:
        is_logged = False
    if is_logged:
        db = sqlite3.connect('database.db')
        twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        profile = Profile(db,twitter)
        agent = Agent(db,twitter)
        post = Post(db)
        return render_template("panel.html",
                               profiles=profile.getProfiles(),
                               unverified =agent.get_unverifed(),
                               verified= agent.get_verifed(),
                               posts=post.get_posts())
    else:
        return redirect(url_for("admin"))



@app.route("/callback")
def callback():
    db = sqlite3.connect('database.db')
    twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    oauth_response = request.args
    verifier = oauth_response.get("oauth_verifier")

    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["resource_owner_key"],
        resource_owner_secret=session["resource_owner_secret"],
        verifier=verifier
    )
    tokens = oauth.fetch_access_token(ACCESS_TOKEN_URL)
    session["oauth_token"] = tokens["oauth_token"]
    session["oauth_token_secret"] = tokens["oauth_token_secret"]
    username =  tokens["screen_name"]
    session["screen_name"] = username
    
    agent_id = twitter.get_id(username)
    session["screen_id"]= agent_id
    session["is_logged"] = True
    agent = Agent(db,oauth)
    if not agent.is_exist(agent_id):
        agent.create_agent(agent_id ,username)
    return redirect(url_for("index"))



@app.route("/tasks", methods=["GET"])
def actions():
    db = sqlite3.connect('database.db')
    task = Task(db)
    tasks = task.get_tasks()
    return jsonify({"data": tasks, "code": 200}), 200

@app.route("/add_profile", methods=["POST"])
def add_profile():
    db = sqlite3.connect('database.db')
    twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    profile_name = form.get("profile")
    tasks = form.get("tasks").split(",")

    profile = Profile(db,twitter)
    success = profile.create(profile_name,tasks)
    return jsonify({"success": success, "code": 200}), 200
@app.route("/edit_profile", methods=["POST"])
def edit_profile():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    profile_id = form.get("profile_id")
    tasks = form.get("tasks").split(",")

    action = Action(db)
    action.editTasks(profile_id,tasks)
    return jsonify({"success": True, "code": 200}), 200
@app.route("/remove_profile", methods=["POST"])
def remove_profile():
    db = sqlite3.connect('database.db')
    twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    profile_id = form.get("profile_id")

    profile = Profile(db,twitter)
    profile.remove(profile_id)
    return jsonify({"success": True, "code": 200}), 200

@app.route("/manage_user", methods=["POST"])
def manage_user():
    db = sqlite3.connect('database.db')
    twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    agent_id = form.get("agent_id")
    action = form.get("action")
    agent = Agent(db,twitter)
    agent.update(agent_id,action)
    return jsonify({"success": True, "code": 200}), 200

@app.route("/manage_post", methods=["POST"])
def manage_post():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    post_id = form.get("post_id")
    action = form.get("action")
    post = Post(db)
    post.update(post_id,action)
    return jsonify({"success": True, "code": 200}), 200

@app.route("/load_data", methods=["POST"])
def load_data():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    task_name = form["task_name"]
    post = Post(db)
    data = post.filterPosts(session["screen_id"],task_name)
    return jsonify({"data": data, "code": 200}), 200

@app.route("/comment", methods=["POST"])
def comment():
    if "oauth_token" not in session:
        return redirect("/login")
    form = request.get_json()
    tweet_id = form["tweet_id"]
    text  = form["text"]
    if not tweet_id and not text:
        return "Tweet content is required", 400

    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    db = sqlite3.connect('database.db')
    agent = Agent(db ,oauth)
    return jsonify(agent.reply(session["screen_id"],text,tweet_id))

@app.route("/like", methods=["POST"])
def like():
    if "oauth_token" not in session:
        return redirect("/login")
    form = request.get_json()
    tweet_id = form["tweet_id"]
    if not tweet_id:
        return "Tweet content is required", 400

    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    db = sqlite3.connect('database.db')
    agent = Agent(db ,oauth)
    return jsonify(agent.like(session["screen_id"],tweet_id))


@app.route("/tweet", methods=["POST"])
def tweet():
    if "oauth_token" not in session:
        return redirect("/login")
    form = request.get_json()
    tweet_text = form["tweet"]
    if not tweet_text:
        return "Tweet content is required", 400

    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    db = sqlite3.connect('database.db')
    agent = Agent(db ,oauth)
    
    return jsonify(agent.tweet(tweet_text))

@app.route("/retweet", methods=["POST"])
def retweet():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    
    tweet_id = form["tweet_id"]
    
    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    
    agent = Agent(db ,oauth)
    return jsonify(agent.retweet(session["screen_id"],tweet_id))

@app.route("/follow", methods=["POST"])
def follow():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    profile_id = form["profile_id"]
    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    agent = Agent(db,oauth)
    return jsonify(agent.follow(session["screen_id"],profile_id))

@app.route("/mute", methods=["POST"])
def mute():
    db = sqlite3.connect('database.db')
    form = request.get_json()
    if not form:
        return jsonify({"error": "Invalid JSON", "code": 400}), 400
    profile_id = form["profile_id"]
    oauth = OAuth1Session(
        API_KEY,
        client_secret=API_SECRET,
        resource_owner_key=session["oauth_token"],
        resource_owner_secret=session["oauth_token_secret"]
    )
    agent = Agent(db,oauth)
    return jsonify(agent.mute(session["screen_id"],profile_id))
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def start_server():
    app.run()
def main_loop():
    while True:
        db = sqlite3.connect('database.db')
        twitter = Twitter(db,OAuth1Session,API_KEY,API_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
        twitter.get_posts()
        sleep(30000)
if __name__ == "__main__":
   server = threading.Thread(target = start_server)
   loop = threading.Thread(target = main_loop)
   server.start()
   loop.start()
   loop.join()
   server.join()
    