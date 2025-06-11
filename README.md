# DeepLearning_Final
煥勳的幻想世界

圖示說明四個程式的結構與 `GPT_app.py` 的工作流程。

---

## 程式結構圖

├── GPT_Angel.py
│   └── chat_as_mahiru(user_text) → str
│
├── GPT_Russian.py
│   └── chat_as_Ellie(user_text) → str
│
├── GPT_Loser.py
│   └── chat_as_Yanami(user_text) → str
│
└── GPT_app.py
    ├── print_menu()
    │     └─ 列出：
    │        ├─ 1. 椎名真晝
    │        ├─ 2. 九條艾琳
    │        ├─ 3. 八奈見杏菜
    │        └─ 0. 離開
    │
    └── main()
         ├─ 顯示歡迎訊息
         ├─ 外層迴圈
         │    ├─ 呼叫 print_menu()
         │    ├─ 讀取 choice
         │    ├─ 如果 choice == "0" → break（結束程式）
         │    ├─ 如果 choice 不在 {"1","2","3"} → 錯誤提示
         │    └─ 如果 choice 在 {"1","2","3"} → 進入角色對話
         │
         └─ 角色對話迴圈
              ├─ 讀取 user_input
              ├─ 如果 user_input in {"", "/bye", "exit", "quit", "back"} → break（回主選單）
              ├─ choice == "1" → 呼叫 chat_as_mahiru(user_input)
              ├─ choice == "2" → 呼叫 chat_as_Ellie(user_input)
              └─ choice == "3" → 呼叫 chat_as_Yanami(user_input)

> **來源**：
> `GPT_app.py`&#x20;
> `GPT_Angel.py`&#x20;
> `GPT_Loser.py`&#x20;
> `GPT_Russian.py`&#x20;

---

## GPT\_app.py 工作流程說明

1. **載入各角色模組**

   ```python
   from GPT_Angel import chat_as_mahiru      # 椎名真晝
   from GPT_Russian import chat_as_Ellie     # 九條艾琳
   from GPT_Loser import chat_as_Yanami      # 八奈見杏菜
   ```

   引入三個角色對話函式，供後續呼叫。&#x20;

2. **列印選單 (`print_menu`)**
   列出可選擇的角色編號與操作提示：

   ```python
   print("\n=== 角色聊天選擇 ===")
   print("1. 椎名真晝")
   print("2. 九條艾琳")
   print("3. 八奈見杏菜")
   print("0. 離開")
   ```

   使用者可輸入 `1/2/3` 選擇角色，或 `0` 結束程式。&#x20;

3. **主流程 (`main`)**

   * **歡迎訊息**
     顯示程式名稱與操作說明。
   * **外層迴圈**
     持續顯示選單並讀取使用者輸入：

     ```python
     while True:
         print_menu()
         choice = input("請選擇要對話的角色 (0-3): ").strip()
         ...
     ```

     * `choice == "0"` → `break`，結束程式
     * 非 `0,1,2,3` → 提示「請輸入有效的選項」，重新顯示選單

4. **角色對話迴圈**
   當使用者選擇 `1/2/3` 後，進入內層迴圈：

   ```python
   while True:
       user_input = input("\n你：").strip()
       if user_input.lower() in {"", "/bye", "exit", "quit", "back"}:
           print("返回主選單...\n")
           break
       # 根據 choice 呼叫對應函式
       if choice == "1":
           reply = chat_as_mahiru(user_input)
           print("椎名真晝：", reply)
       ...
   ```

   * 若輸入空字串或 `/bye`、`exit`、`quit`、`back` → 跳出內層迴圈，回到主選單
   * 否則呼叫對應的 `chat_as_*` 函式，並印出角色回覆

5. **角色聊天函式 (`chat_as_*`)**
   這些函式皆封裝了：

   * 建立 thread
   * 傳送使用者訊息
   * 觸發並輪詢 run 直到完成
   * 取得並回傳角色的回覆文字
     具體實作請參考各模組檔案

6. **結束程式**
   使用者於主選單輸入 `0` 或程式內部捕捉到終止指令後，列印「感謝使用，再見！」並結束。

