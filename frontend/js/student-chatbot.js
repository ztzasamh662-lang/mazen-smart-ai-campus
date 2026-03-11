// ===== Role Protection =====
const role = localStorage.getItem("role")

if(role !== "student"){
window.location.href = "login.html"
}


// ===== Logout =====
function logout(){
localStorage.clear()
window.location.href="login.html"
}


// ===== Student Name =====
const username = localStorage.getItem("username") || "Student"

document.getElementById("student-name").textContent = username



// ===== Chatbot =====
const chatInput = document.getElementById("chat-input")
const chatSend = document.getElementById("chat-send")
const chatWindow = document.getElementById("chat-window")


const responses = {

"attendance":"Your attendance is 92%",
"alerts":"You have 1 alert",
"help":"You can ask about attendance, alerts or system status.",
"system":"System is running normally"

}


function sendMessage(){

const msg = chatInput.value.trim()

if(!msg) return


chatWindow.innerHTML += `
<div class="user-msg">
You: ${msg}
</div>
`


let reply = "I didn't understand that."

for(let key in responses){

if(msg.toLowerCase().includes(key)){
reply = responses[key]
}

}


chatWindow.innerHTML += `
<div class="bot-msg">
AI: ${reply}
</div>
`

chatInput.value=""

chatWindow.scrollTop = chatWindow.scrollHeight

}


chatSend.onclick = sendMessage

chatInput.addEventListener("keypress",(e)=>{

if(e.key==="Enter") sendMessage()

})