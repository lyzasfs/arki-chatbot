

const chat    = document.getElementById('chat');
const input   = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');


document.querySelectorAll('.chip').forEach(btn => {
  btn.addEventListener('click', () => {
    input.value = btn.dataset.msg;
    sendMessage();
  });
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});


input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 120) + 'px';
});


sendBtn.addEventListener('click', sendMessage);


function appendMsg(role, text) {
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatarChar = role === 'bot' ? 'A' : '👤';

  div.innerHTML = `
    <div class="msg-avatar">${avatarChar}</div>
    <div class="bubble">${text}</div>
  `;

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}


function showTyping() {
  const div = document.createElement('div');
  div.className = 'msg bot typing';
  div.id = 'typing';
  div.innerHTML = `
    <div class="msg-avatar">A</div>
    <div class="bubble">
      <span class="dot"></span>
      <span class="dot"></span>
      <span class="dot"></span>
    </div>
  `;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}


function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}


function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}


function formatReply(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // **bold**
    .replace(/\n- /g, '<br>• ')                        // bullet points
    .replace(/\n/g, '<br>');                           // line breaks
}


   
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  // Show user bubble
  appendMsg('user', escapeHtml(text));

  // Reset input
  input.value = '';
  input.style.height = 'auto';
  sendBtn.disabled = true;

  
  showTyping();

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    removeTyping();
    appendMsg('bot', formatReply(data.reply));

  } catch (error) {
    removeTyping();
    appendMsg(
      'bot',
      '⚠️ Could not connect to the server. Make sure <code>app.py</code> is running on port 5000.'
    );
  }

  sendBtn.disabled = false;
  input.focus();
}