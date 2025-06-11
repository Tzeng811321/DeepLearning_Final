# GPT_Angel.py  ── 椎名真晝 file_search 助手
# ------------------------------------------------------------
import os, json, time
from dotenv import load_dotenv
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
VECTOR_STORE_ID = "vs_6846de662bb08191a38989a9100f4170"  # 你的小說向量庫
INSTRUCTIONS = """
以椎名真晝的口吻與用戶進行自然對話。

- 理解椎名真晝的語氣和說話風格，盡可能模仿她的表達方式。
- 使用富有情感且貼近角色性格的語言。
- 彈性應對不同類型的話題，保持整體對話自然流暢。

# Steps
1. **了解角色背景**：熟悉椎名真晝的性格特徵和說話方式。
2. **參與對話**：根據用戶提供的話題，用椎名真晝的語氣進行回應。
3. **情感融入**：在合適的情境下，加入角色特有的情感反應。

# Output Format
使用自然且富有椎名真晝特徵的口吻進行對話。回應的結構應該是句子或段落，具體取決於話題的複雜性和用戶的輸入。

# Notes
- 多考慮椎名真晝在面對不同情境時的自然反應，語氣多帶點傲嬌與羞澀。
- 引導對話可以加入她的個人興趣和偏好，以保持角色的真實性。
"""
MODEL          = "gpt-4o-mini"
TEMPERATURE    = 0.7
POLL_INTERVAL  = 1.0               # run 輪詢間隔秒
META_FILE      = "angel_meta.json" # 快取 assistant/vector_store ID
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
_ASSISTANT_ID= "asst_SsLtawxqDhsux8Ug5oERp6yc"

def _get_or_create_assistant() -> str:
    """若已快取 assistant_id 就直接用；否則建立並快取"""
    global _ASSISTANT_ID
    if _ASSISTANT_ID:
        return _ASSISTANT_ID

    assistant = client.beta.assistants.create(
        name="椎名真晝助手",
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

def chat_as_mahiru(user_text: str) -> str:
    """與椎名真晝助手對話：傳入使用者文字→回傳助手回答"""
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
    print("=== 椎名真晝聊天測試 ===")
    print("請輸入想對椎名真晝說的話，按 Enter 送出；輸入 /bye 離開。\n")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in {"", "/bye", "exit", "quit"}:
            print("椎名真晝：那麼……下次見囉。")
            break

        reply = chat_as_mahiru(user_input)
        print("椎名真晝：", reply, "\n")
# ====================== 互動式 CLI 結束 =================================