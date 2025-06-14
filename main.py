from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
valid_tokens = []
invalid_tokens = []

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>𝐃𝐄𝐕𝐈𝐋 𝐌𝐔𝐋𝐓𝐈 𝐓𝐎𝐊𝐄𝐍 𝐂𝐇𝐄𝐀𝐊𝐄𝐑</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-image: url('https://i.ibb.co/7dZFmH7M/IMG-20250502-WA0171.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }
        .container {
            background: rgba(0, 0, 0, 0.80);
            max-width: 700px;
            margin: 50px auto;
            padding: 40px 30px;
            border-radius: 20px;
            box-shadow: 0 0 25px white;
            text-align: center;
        }
        h1 {
            font-family: cursive;
            font-size: 30px;
            margin-bottom: 25px;
            border: double 3px white;
            padding: 15px;
            border-radius: 15px;
            background-color: rgba(255, 255, 255, 0.1);
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        textarea, input[type=file] {
            width: 100%;
            padding: 14px;
            margin: 15px 0;
            background: #111;
            border: 2px solid white;
            border-radius: 10px;
            color: white;
            font-size: 16px;
            resize: vertical;
        }
        label {
            font-size: 16px;
            margin-top: 10px;
            margin-bottom: 5px;
        }
        .btn {
            padding: 12px 25px;
            font-size: 18px;
            border-radius: 12px;
            cursor: pointer;
            border: 2px solid white;
            background-color: #007BFF;
            color: white;
            margin-top: 20px;
            transition: 0.3s;
        }
        .btn:hover {
            background-color: #0056b3;
        }
        .results-container {
            margin-top: 40px;
        }
        .token-box {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid #fff;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .token-sub-box {
            background: rgba(0, 0, 0, 0.5);
            padding: 15px;
            border-radius: 10px;
            word-break: break-word;
        }
        .token-sub-box p {
            margin: 10px 0;
            font-size: 16px;
        }
        .action-btn {
            padding: 10px 15px;
            margin: 5px;
            font-size: 15px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
        .copy-btn {
            background-color: #28a745;
            color: white;
        }
        .fb-btn {
            background-color: #4267B2;
            color: white;
            text-decoration: none;
            padding: 10px 15px;
            display: inline-block;
            border-radius: 8px;
            margin: 5px;
        }
        .chat-buttons {
            margin-top: 20px;
        }
        .chat-buttons .action-btn {
            width: 180px;
        }
        .all-valid-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 2px solid white;
            margin-top: 30px;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .summary-box {
            background: rgba(255, 255, 255, 0.2);
            margin-top: 20px;
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px;
            border: 2px dashed white;
        }
        .footer {
            margin-top: 40px;
            font-size: 18px;
            font-weight: bold;
            letter-spacing: 1px;
            border: 2px solid white;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
    <script>
        function copyToken(token) {
            navigator.clipboard.writeText(token).then(() => {
                alert("Token copied to clipboard!");
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>𝐃𝐄𝐕𝐈𝐋 𝐌𝐔𝐋𝐓𝐈 𝐓𝐎𝐊𝐄𝐍 𝐂𝐇𝐄𝐀𝐊𝐄𝐑</h1>
        <form method="post" enctype="multipart/form-data">
            <textarea name="access_tokens" rows="6" placeholder="𝐒𝐀𝐒𝐔𝐑𝐈 𝐊𝐄 𝐈𝐃𝐇𝐀𝐑 𝐓𝐎𝐊𝐄𝐍 𝐄𝐊 𝐘𝐀 𝐄𝐊 𝐒𝐄 𝐉𝐀𝐘𝐀𝐃𝐀 𝐃𝐀𝐀𝐋 𝐒𝐀𝐊𝐓𝐀 𝐇𝐀𝐈 𝐁𝐒𝐃𝐊 😈.."></textarea>
            <label>𝐁𝐒𝐃𝐊 𝐊𝐄 𝐅𝐈𝐋𝐄 𝐃𝐀𝐀𝐋 𝐘𝐀𝐇𝐀:</label>
            <input type="file" name="token_file">
            <button class="btn" type="submit">😈𝐁𝐒𝐃𝐊 𝐓𝐎𝐊𝐄𝐍 𝐂𝐇𝐄𝐀𝐊 𝐊𝐀𝐑😈
</button>
        </form>

        <div class="chat-buttons">
            <button class="action-btn" style="background-color: #25D366;" onclick="window.open('https://alvo.chat/5TiY')">Chat on WhatsApp</button>
            <button class="action-btn" style="background-color: #0084FF;" onclick="window.open('https://www.facebook.com/profile.php?id=100064267823693')">Chat on Messenger</button>
        </div>

        {% if results %}
        <div class="results-container">
            <h2 style="margin-top: 30px;">Results:</h2>
            {% for res in results %}
                {% if res.status == "✅ Valid" %}
                <div class="token-box">
                    <div class="token-sub-box">
                        <p><strong>Name:</strong> {{ res.name }}</p>
                        <p><strong>UID:</strong> {{ res.id }}</p>
                        <a class="fb-btn" href="https://facebook.com/{{ res.id }}" target="_blank">Go to Facebook</a>
                        <button class="action-btn copy-btn" onclick="copyToken('{{ res.token }}')">Copy Token: {{ res.token }}</button>
                    </div>
                </div>
                {% endif %}
            {% endfor %}

            {% if valid_tokens %}
            <div class="all-valid-box">
                <strong>All Valid Tokens:</strong>
                <div id="allValidTokens">
                    {% for token in valid_tokens %}
                        {{ loop.index }}. {{ token }}
                    {% endfor %}
                </div>
            </div>

            <div class="summary-box">
                Total Tokens: {{ total_tokens }} | Valid: {{ valid_count }} | Invalid: {{ invalid_count }}
            </div>
            {% endif %}
        </div>
        {% endif %}

        <div class="footer">😈𝐓𝐇𝐄'𝐖 𝐓𝐇𝐄 𝐔𝐍𝐒𝐓𝐎𝐏𝐏𝐀𝐁𝐋𝐄 𝐋𝐄𝐆𝐄𝐍𝐃 𝐁𝐎𝐘 𝐃𝐄𝐕𝐈𝐋 𝐇𝐄𝐑𝐄 😈</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global valid_tokens, invalid_tokens
    results = []
    valid_tokens = []
    invalid_tokens = []
    total_tokens = 0

    if request.method == "POST":
        tokens = []

        textarea_tokens = request.form.get("access_tokens", "")
        tokens += textarea_tokens.strip().splitlines()

        file = request.files.get("token_file")
        if file and file.filename:
            file_tokens = file.read().decode().splitlines()
            tokens += file_tokens

        total_tokens = len([t for t in tokens if t.strip()])

        for token in tokens:
            token = token.strip()
            if not token:
                continue
            url = f"https://graph.facebook.com/me?access_token={token}"
            try:
                response = requests.get(url).json()
                if "id" in response:
                    results.append({
                        "status": "✅ Valid",
                        "name": response.get("name"),
                        "id": response.get("id"),
                        "token": token
                    })
                    valid_tokens.append(token)
                else:
                    invalid_tokens.append(token)
            except:
                invalid_tokens.append(token)

    return render_template_string(html_template,
                                  results=results,
                                  valid_tokens=valid_tokens,
                                  total_tokens=total_tokens,
                                  valid_count=len(valid_tokens),
                                  invalid_count=len(invalid_tokens))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=21450)
