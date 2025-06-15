import os
from flask import Flask, render_template, request, jsonify
from chat_handlers import get_reply

# ---------------------------------------------------------
# Flask 應用程式設定
# 先印出目前執行時的工作目錄
print("工作目錄:", os.getcwd())

# 如果你有用顯式設定 template_folder，就印出它
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(BASE_DIR, "templates")
print("預期的 templates 資料夾:", template_dir)

# 印出 templates 資料夾底下檔案列表
if os.path.isdir(template_dir):
    print("templates 內容:", os.listdir(template_dir))
else:
    print("templates 資料夾不存在！")
# ---------------------------------------------------------

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(BASE_DIR, "templates")
static_dir   = os.path.join(BASE_DIR, "static")

app = Flask(__name__,
            template_folder=template_dir,
            static_folder=static_dir)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.json
    return jsonify({"reply": get_reply(data["role"], data["message"])})

if __name__ == "__main__":
    app.run(debug=True)
