from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Thư mục web & log
WEB_DIR = "data/web"
LOG_DIR = "data/logs"
os.makedirs(WEB_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# File index.html giả lập website
INDEX_FILE = os.path.join(WEB_DIR, "index.html")

if not os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "w") as f:
        f.write("<h1>Welcome</h1>")

# Hàm ghi access log kèm nhãn hành vi
def log_request(label):
    ts = datetime.now().isoformat()
    with open(os.path.join(LOG_DIR, "access.log"), "a") as f:
        f.write(f"{ts} {request.remote_addr} "
                f"{request.method} {request.path} {label}\n")

# Trang chủ (hành vi bình thường)
@app.route("/")
def index():
    log_request("normal")
    return open(INDEX_FILE).read()

# Endpoint search (hành vi nghi vấn)
@app.route("/danger")
def search():
    q = request.args.get("q", "")
    log_request("suspicious")
    return jsonify({"query": q})

# Endpoint upload (deface)
@app.route("/upload", methods=["POST"])
def upload():
    content = request.form.get("content", "")
    if content:
        with open(INDEX_FILE, "w") as f:
            f.write(content)
        log_request("deface")
        return "File updated"
    return "No content"

if __name__ == "__main__":
    app.run(port=5000)
