#!/usr/bin/env python3

from flask import Flask, send_from_directory, render_template_string, request, redirect, url_for
import time
import subprocess

app = Flask(__name__)

# Generate the timestamp at the time of starting the app
timestamp = int(time.time())

# Function to get the IP address of the WiFi adapter
def get_ip_address(interface):
    try:
        # Use socket to get the IP address
        import netifaces
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            ip_info = netifaces.ifaddresses(interface)[netifaces.AF_INET]
            return ip_info[0]['addr'] if ip_info else "No IP assigned"
        return "No IP assigned"
    except Exception:
        return "IP address not available"

# Route to serve the SVG file
@app.route("/power-button.svg")
def serve_svg():
    return send_from_directory(".", "power-button.svg")

# Home page route
@app.route("/")
def home():
    # Get the current IP address of the WiFi adapter
    ip_address = get_ip_address("wlp0s20f3")
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
            .ip {{
                margin-top: 20px;
                font-size: 1.2em;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <a href="/powerdown?timestamp={timestamp}">
            <img src="/power-button.svg" alt="Power Button">
        </a>
        <div class="ip">Current IP Address: {ip_address}</div>
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
