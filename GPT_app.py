from GPT_Angel import chat_as_mahiru
from GPT_Russian import chat_as_Ellie
from GPT_Loser import chat_as_Yanami

def print_menu():
    print("\n=== 角色聊天選擇 ===")
    print("1. 椎名真晝")
    print("2. 九條艾琳")
    print("3. 八奈見杏菜")
    print("0. 離開")
    print("================\n")

def main():
    print("歡迎使用角色聊天系統！")
    print("可以隨時輸入 /bye, exit, quit 或 back 來返回主選單")
    
    while True:
        print_menu()
        choice = input("請選擇要對話的角色 (0-3): ").strip()

        if choice == "0":
            print("感謝使用，再見！")
            break

        if choice not in ["1", "2", "3"]:
            print("請輸入有效的選項 (0-3)")
            continue

        # 選擇角色對話
        while True:
            user_input = input("\n你：").strip()
            
            if user_input.lower() in {"", "/bye", "exit", "quit", "back"}:
                print("返回主選單...\n")
                break

            # 根據選擇呼叫不同的聊天函數
            if choice == "1":
                reply = chat_as_mahiru(user_input)
                print("椎名真晝：", reply)
            elif choice == "2":
                reply = chat_as_Ellie(user_input)
                print("九條艾琳：", reply)
            elif choice == "3":
                reply = chat_as_Yanami(user_input)
                print("八奈見杏菜：", reply)

if __name__ == "__main__":
    main()
