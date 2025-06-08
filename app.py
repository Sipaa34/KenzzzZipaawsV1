from flask import Flask, render_template, request
import socket, requests, re

app = Flask(__name__)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def check_username(username):
    platforms = {
        "Twitter": f"https://twitter.com/{username}",
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "TikTok": f"https://www.tiktok.com/@{username}"
    }
    results = {}
    for name, url in platforms.items():
        try:
            r = requests.get(url)
            results[name] = url if r.status_code == 200 else None
        except:
            results[name] = None
    return results

def ip_lookup(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res if res["status"] == "success" else {"error": "Invalid IP"}
    except:
        return {"error": "Failed to fetch data"}

def port_scan(host, ports):
    open_ports = []
    try:
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((host, port))
                if result == 0:
                    open_ports.append(port)
    except:
        return []
    return open_ports

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    if request.method == "POST":
        username = request.form.get("username")
        ip = request.form.get("ip")
        email = request.form.get("email")
        domain = request.form.get("domain")
        host = request.form.get("host")

        if username:
            results["username"] = check_username(username)
        if ip:
            results["ip"] = ip_lookup(ip)
        if email:
            results["email_valid"] = validate_email(email)
        if host:
            results["ports"] = port_scan(host, range(20, 1025))
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
