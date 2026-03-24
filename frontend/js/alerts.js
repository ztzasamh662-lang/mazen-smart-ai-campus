// ===== Admin Protection =====
const role = localStorage.getItem("role")

if(role !== "admin"){
    window.location.href = "login.html"
}


// ===== Logout =====
function logout(){
    localStorage.clear()
    window.location.href = "login.html"
}


// ===== Fake Alerts =====
let alertsData = [

{ name:"Ahmed", event:"Phone Detected", time:"09:10 AM", status:"New" },
{ name:"Sara", event:"Multiple Faces", time:"09:15 AM", status:"Seen" },
{ name:"Mona", event:"Late Entry", time:"09:20 AM", status:"New" },
{ name:"Mazen", event:"Absent", time:"09:25 AM", status:"Seen" }

];


// ===== Populate Alerts Table =====
function populateAlertsTable(){

const tableBody = document.querySelector("#alerts-table tbody")

if(!tableBody) return

tableBody.innerHTML = ""

alertsData.forEach(alert => {

const row = document.createElement("tr")

// Highlight new alert
if(alert.status === "New"){
row.style.backgroundColor = "#2b1b1b"
}


// ===== Name =====
const nameCell = document.createElement("td")
nameCell.textContent = alert.name


// ===== Event =====
const eventCell = document.createElement("td")
eventCell.textContent = alert.event


// ===== Time =====
const timeCell = document.createElement("td")
timeCell.textContent = alert.time


// ===== Status =====
const statusCell = document.createElement("td")
statusCell.textContent = alert.status

if(alert.status === "New"){
statusCell.style.color = "#ff5252"
}else{
statusCell.style.color = "#00e676"
}


// ===== Append =====
row.appendChild(nameCell)
row.appendChild(eventCell)
row.appendChild(timeCell)
row.appendChild(statusCell)

tableBody.appendChild(row)

})

}


// ===== Fake Live Alerts Update =====
function simulateNewAlert(){

const students = ["Ahmed","Sara","Mona","Mazen"]

const events = [
"Phone Detected",
"Talking",
"Late Entry",
"Multiple Faces"
]

const randomStudent = students[Math.floor(Math.random()*students.length)]
const randomEvent = events[Math.floor(Math.random()*events.length)]

const now = new Date()

const time =
now.getHours().toString().padStart(2,"0")+":"+
now.getMinutes().toString().padStart(2,"0")+":"+
now.getSeconds().toString().padStart(2,"0")

alertsData.unshift({

name:randomStudent,
event:randomEvent,
time:time,
status:"New"

})

// نخلي آخر alert يتحول Seen
if(alertsData.length > 6){
alertsData.pop()
}

populateAlertsTable()

}


// ===== Page Load =====
window.onload = ()=>{

populateAlertsTable()

// كل 8 ثواني يظهر Alert جديد
setInterval(()=>{

simulateNewAlert()

},8000)

}