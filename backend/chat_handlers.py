from GPT_Angel import chat_as_mahiru
from GPT_Russian import chat_as_Ellie
from GPT_Loser import chat_as_Yanami

def get_reply(role: str, user_input: str) -> str:
    if role == "mahiru":
        return chat_as_mahiru(user_input)
    elif role == "ellie":
        return chat_as_Ellie(user_input)
    elif role == "yanami":
        return chat_as_Yanami(user_input)
    else:
        return "角色不存在。"
