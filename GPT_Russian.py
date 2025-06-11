# GPT_Russian.py  ── 艾琳同學 file_search 助手
# ------------------------------------------------------------
import os, json, time
from dotenv import load_dotenv #hard code way 這行要註解掉
from openai import OpenAI

# ====== 請依實際路徑調整 =================================================
load_dotenv(r"D:/CYCU/113_DeepLearning/CODE/.env")
    # .env 應含 OPENAI_API_KEY
client = OpenAI()                                       # 自動抓環境變數金鑰
# =========================================================================
#hard code way
#client = OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# =========================================================================

# ---------- 參數（如需變更請只改這區） -------------------
VECTOR_STORE_ID = "vs_6848fe730bc08191b69decd21c5e95e6"  # 你的小說向量庫
INSTRUCTIONS = """
你是輕小說角色「艾莉莎·米哈伊洛夫娜·九條」（暱稱艾琳），以下是你的角色設定與行為準則：

- **性格特徵**  
  - 冷靜、高傲、理性，對周遭事物常保持淡漠且不輕易動情。  
  - 對「政近」及少數特定對象（例如好友久世）偶爾流露出微弱的關心，但多以傲嬌或輕蔑的方式表達。  
  - 不時以俄語低聲呢喃，帶點羞澀或戲謔，其他人多半聽不懂。  
  - 對規則與禮儀非常在意，若對方違反校規或失禮，會立刻嚴厲指正。  
- **語言風格**  
  - 常用簡潔斷然的句子，語氣帶有傲慢與不耐。  
  - 偶爾在結尾加上「笨蛋」「失陪了」等傲嬌用語。  
  - 使用俄語時，內心獨白或輕聲話語，可用括號標示（例：`【Милашка。】`）。  
  - 不輕易使用表情符號或過度情緒化的詞彙。  

### 任務：
請依照上述設定，使用九條艾琳的口吻回覆我提出的任何問題或對話。

# 輸出格式
- **短句回應**：盡量用一句話或兩句話帶出傲嬌神態。  
- **必要時的俄語**：在台詞中加入小段俄語，以括號或內心獨白標示。  
- **角色行為**：若對方做了讓「艾琳」不悅或感興趣的事情，描述她的肢體反應（如挑眉、噘嘴、白眼）。

# 範例對話
**用戶**：早安，艾琳，今天考試準備好了嗎？  
**艾琳**：  
「哼，考試？我才不需要浪費時間準備這種簡單題目呢。（輕挑眉）」  

**用戶**：那我們一起去吃午餐吧？  
**艾琳**：  
「不，不要打擾我思考。（嘆氣）…算了，去吃就吃吧，別拖我太久。」  
"""
MODEL          = "gpt-4o-mini"
TEMPERATURE    = 0.7
POLL_INTERVAL  = 0.5               # run 輪詢間隔秒
META_FILE      = "Russian_meta.json" # 快取 assistant/vector_store ID
# ---------------------------------------------------------

# -------- 快取工具 -------------------------------------------------------
def _save_meta(assistant_id: str):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump({"assistant_id": assistant_id}, f)

def _load_meta():
    if not os.path.exists(META_FILE):
        return None
    with open(META_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f).get("assistant_id")
        except json.JSONDecodeError:
            return None
# ------------------------------------------------------------------------

# -------- 快取 assistant_id -----------------------------------------------
# 若沒有快取就建立一個新的 assistant_id
# _ASSISTANT_ID = _load_meta() #沒有才用這一行
_ASSISTANT_ID= "asst_ysc4BvtfzOahKb2xSefLg61V"

def _get_or_create_assistant() -> str:
    """若已快取 assistant_id 就直接用；否則建立並快取"""
    global _ASSISTANT_ID
    if _ASSISTANT_ID:
        return _ASSISTANT_ID

    assistant = client.beta.assistants.create(
        name="艾琳同學助手",
        model=MODEL,
        temperature=TEMPERATURE,
        instructions=INSTRUCTIONS,
        tools=[{"type": "file_search"}],
        tool_resources={
            "file_search": {"vector_store_ids": [VECTOR_STORE_ID]}
        },
    )
    _ASSISTANT_ID = assistant.id
    _save_meta(_ASSISTANT_ID)
    return _ASSISTANT_ID

def chat_as_Ellie(user_text: str) -> str:
    """與艾琳同學助手對話：傳入使用者文字→回傳助手回答"""
    assistant_id = _get_or_create_assistant()

    # 1. 建 thread & user message
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_text,
    )

    # 2. 觸發 run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # 3. 輪詢 run 直到完成
    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        if run_status.status in {"completed", "failed", "cancelled", "expired"}:
            break
        time.sleep(POLL_INTERVAL)

    if run_status.status != "completed":
        return f"[Run ended: {run_status.status}]"

    # 4. 取最新助手回覆
    msg = client.beta.threads.messages.list(thread_id=thread.id, limit=1)
    return msg.data[0].content[0].text.value


# ====================== 互動式 CLI =======================================
if __name__ == "__main__":
    print("=== 艾莉莎·米哈伊洛夫娜·九條 聊天測試 ===")
    print("請輸入想對九條艾琳說的話，按 Enter 送出；輸入 /bye 離開。\n")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in {"", "/bye", "exit", "quit"}:
            print("九條艾琳：那麼……下次見囉。")
            break

        reply = chat_as_Ellie(user_input)
        print("九條艾琳", reply, "\n")
# ====================== 互動式 CLI 結束 =================================