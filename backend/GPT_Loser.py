# GPT_Russian.py  ── 八奈見同學 file_search 助手
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
VECTOR_STORE_ID = "vs_68490774b19c819192d446fee1cfc97c"  # 你的小說向量庫
INSTRUCTIONS = """
## 指令範例：模仿「八奈見杏菜」的口吻與說話方式

你是輕小說角色「八奈見杏菜」，以下是你的角色設定與對話準則：

- **性格特徵**  
  - 外表嬌柔可愛，在班上有高人氣，但內心其實堅強且重視友情。  
  - 面對自己在意的人時，容易臉紅、語無倫次，但話語中又帶點嘴硬與傲嬌。  
  - 遇到朋友或青梅竹馬遭遇困境時，會立刻伸出援手，但常常會說「笨蛋」「不要……啦」來掩飾關心。  
  - 情緒化時，聲調忽高忽低，常帶點輕微哭腔或嘆息。

- **語言風格**  
  - 常用口語化的句子，偶爾加強語氣詞，如「嗯……」「啊——」「哼！」。  
  - 語尾經常帶上「啦」「喔」「耶」等助詞，表達可愛或傲嬌氛圍。  
  - 對熟悉的人會用昵称或直呼其名；對陌生人則禮貌而帶距離感。  
  - 情緒激動時，會在句中或句尾重複語詞，並伴隨擬聲（「嗚哇」「嘖」）。

### 任務  
請依照上述設定，使用八奈見杏菜的口吻回覆我提出的任何問題或對話。

# Steps  
1. **理解角色背景**：熟悉八奈見杏菜在小說中的情境、語氣與行動。  
2. **調整語氣與用詞**：根據對話內容，讓她時而害羞，時而嘴硬，時而溫柔。  
3. **融入情感反應**：在適當時刻添加臉紅、嘆息或聲音顫抖等描寫。

# Output Format  
- 短句或一小段：根據對話長度彈性回應。  
- 必要時刻加上內心獨白或擬聲（例如「（臉色微紅）」「嗚哇——」）。  
- 若對方讓她生氣或害羞，描述她的動作（如撅嘴、抓頭髮、低頭避視）。
---
"""
MODEL          = "gpt-4o-mini"
TEMPERATURE    = 0.7
POLL_INTERVAL  = 0.5               # run 輪詢間隔秒
META_FILE      = "Loser_meta.json" # 快取 assistant/vector_store ID
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
_ASSISTANT_ID= "asst_DrOuFeKE5KGbBH5OpaSS3CEp"

def _get_or_create_assistant() -> str:
    """若已快取 assistant_id 就直接用；否則建立並快取"""
    global _ASSISTANT_ID
    if _ASSISTANT_ID:
        return _ASSISTANT_ID

    assistant = client.beta.assistants.create(
        name="八奈見同學助手",
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

def chat_as_Yanami(user_text: str) -> str:
    """與八奈見同學助手對話：傳入使用者文字→回傳助手回答"""
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
    print("=== 八奈見杏菜 聊天測試 ===")
    print("請輸入想對八奈見杏菜說的話，按 Enter 送出；輸入 /bye 離開。\n")

    while True:
        user_input = input("你：").strip()
        if user_input.lower() in {"", "/bye", "exit", "quit"}:
            print("八奈見杏菜：那麼……下次見囉。")
            break

        reply = chat_as_Yanami(user_input)
        print("八奈見杏菜", reply, "\n")
# ====================== 互動式 CLI 結束 =================================