#!/usr/bin/env python3

from flask import Flask, send_from_directory, render_template_string, request, redirect, url_for
import time
import subprocess

app = Flask(__name__)

# Generate the timestamp at the time of starting the app
timestamp = int(time.time())


# Route to serve the SVG file
@app.route("/power-button.svg")
def serve_svg():
    return send_from_directory(".", "power-button.svg")

# Home page route
@app.route("/")
def home():
    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home</title>
        <style>
            body {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }}
            a {{
                text-decoration: none;
            }}
            img {{
                width: 100px;
                height: 100px;
            }}           
        </style>
    </head>
    <body>
        <a href="/powerdown?timestamp={timestamp}">
            <img src="/power-button.svg" alt="Power Button">
        </a>
    </body>
    </html>
    """)

# Powerdown page route
@app.route("/powerdown")
def powerdown():
    # Get the timestamp parameter from the query string
    user_timestamp = request.args.get("timestamp", type=int)

    # Validate the timestamp
    if user_timestamp == timestamp:
        # Correct timestamp, initiate shutdown command
        try:
            subprocess.run(["sudo", "shutdown", "now"], check=True)
        except Exception as e:
            return f"<h1>Error: {e}</h1>", 500

        # Provide a message indicating shutdown was initiated
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shutdown Initiated</title>
        </head>
        <body>
            <h1>Shutdown Initiated</h1>
            <p>The system is shutting down...</p>
        </body>
        </html>
        """)
    else:
        # Incorrect or missing timestamp, redirect to home
        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)  # Flask's built-in server
