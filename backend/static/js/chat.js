const chatWindow       = document.getElementById("chat-window");
const roleSelect       = document.getElementById("role-select");
const userInput        = document.getElementById("user-input");
const sendBtn          = document.getElementById("send-btn");
const typingIndicator  = document.getElementById("typing-indicator");

const avatars = {
  user:    "/static/images/user.png",
  mahiru:  "/static/images/mahiru.png",
  ellie:   "/static/images/ellie.png",
  yanami:  "/static/images/yanami.png"
};

/**
 * 將訊息附加到聊天視窗
 * @param {string} text   要顯示的訊息文字
 * @param {string} sender 訊息發送者 ('user' 或 其他角色 key)
**/
function appendMessage(text, sender) {
  // 建立最外層訊息容器
  const msgEl = document.createElement("div");
  msgEl.classList.add("message", sender);

  if (sender === "user") {
    // 使用者訊息：先插入文字泡泡，再插入頭像於右側
    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;
    msgEl.appendChild(bubble);

    const avatarImg = document.createElement("img");
    avatarImg.src = avatars.user;            // 使用者頭像
    avatarImg.classList.add("avatar");
    msgEl.appendChild(avatarImg);
  } else {
    // 其他角色訊息：先插入頭像於左側，再插入文字泡泡
    const avatarImg = document.createElement("img");
    avatarImg.src = avatars[sender] || avatars.user;  // 角色頭像（若無則顯示預設 user 頭像）
    avatarImg.classList.add("avatar");
    msgEl.appendChild(avatarImg);

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.textContent = text;
    msgEl.appendChild(bubble);
  }

  // 將訊息元素加入聊天視窗，並自動滾動到底
  chatWindow.appendChild(msgEl);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}


sendBtn.addEventListener("click", async () => {
  const text = userInput.value.trim();
  if (!text) return;

  // 顯示使用者訊息
  appendMessage(text, "user");
  userInput.value = "";

  // 顯示輸入中狀態
  typingIndicator.classList.remove("hidden");

  // 呼叫後端 API
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      role: roleSelect.value,
      message: text
    })
  });
  const data = await res.json();

  // 隱藏輸入中
  typingIndicator.classList.add("hidden");

  // 顯示機器人回覆
  appendMessage(data.reply, roleSelect.value);
});

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendBtn.click();
});
