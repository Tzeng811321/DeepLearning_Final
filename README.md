倉庫語言
Python

檔案皆位於 backend/，例如 app.py 開頭即使用 Flask。

HTML

前端模板為 templates/index.html。

JavaScript

前端互動邏輯位於 static/js/chat.js。

CSS

樣式定義於 static/css/style.css。

主要函式庫 (requirements.txt)
Flask（後端 Web Framework）

openai（與 OpenAI API 溝通）

httpx（HTTP 客戶端，雖未直接在程式中使用但列入需求）

requests（HTTP 請求函式庫）

dotenv（讀取 .env 檔設定）

程式碼結構
backend/
├── app.py              # 啟動 Flask 伺服器，提供聊天 API 與前端頁面
├── chat_handlers.py    # 根據角色呼叫對應聊天函式
├── GPT_app.py          # 終端介面，可選擇角色進行對話(除錯用)
├── GPT_Angel.py        # 椎名真晝角色對話邏輯
├── GPT_Russian.py      # 九條艾琳角色對話邏輯
├── GPT_Loser.py        # 八奈見杏菜角色對話邏輯
├── requirements.txt    # 依賴套件列表
├── templates/
│   └── index.html      # 前端頁面
└── static/
    ├── css/style.css   # 頁面樣式
    ├── js/chat.js      # 前端互動程式
    └── images/         # 角色頭像等資源
整體而言，這個倉庫是一個以 Python/Flask 為後端、搭配 HTML/CSS/JavaScript 前端的簡易聊天應用程式。使用者可在網頁或終端選擇三個預設角色（由 GPT_Angel.py、GPT_Russian.py、GPT_Loser.py 分別實作）進行對話，各角色檔中透過 OpenAI API 取得回應，並使用 .env 檔設定相關參數與向量庫。
