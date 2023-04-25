from flask import Flask, render_template, request
import os
import socket
import ssl
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# IRC server information
server = "irc.chat.twitch.tv"
port = 6697
channel = os.getenv("CHANNEL")
bot_nick = os.getenv("NICK")
oauth_token = os.getenv("TMI_TOKEN")

# Connect to Twitch IRC server using SSL
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_context = ssl.create_default_context()
irc = ssl_context.wrap_socket(irc, server_hostname=server)
irc.connect((server, port))

# Authenticate with Twitch using OAuth2
irc.send(f"PASS {oauth_token}\n".encode())
irc.send(f"USER {bot_nick} {bot_nick} {bot_nick} :Python IRC\n".encode())
irc.send(f"NICK {bot_nick}\n".encode())

# Join the Twitch channel
irc.send(f"JOIN #{channel}\n".encode())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message = request.form.get("message")
        irc.send(f"PRIVMSG #{channel} :{message}\n".encode())
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
