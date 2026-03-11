const role = localStorage.getItem("role")

if(role !== "student"){
window.location.href = "login.html"
}


// ===== Logout =====
function logout(){
localStorage.clear()
window.location.href="login.html"
}


let alerts = [

{event:"Phone Detected",time:"09:10"},
{event:"Talking",time:"09:20"}

]


function populateAlerts(){

const table = document.querySelector("#student-alerts-table tbody")

table.innerHTML = ""

alerts.forEach(alert=>{

const row = document.createElement("tr")

row.innerHTML = `
<td>${alert.event}</td>
<td>${alert.time}</td>
`

table.appendChild(row)

})

}


populateAlerts()